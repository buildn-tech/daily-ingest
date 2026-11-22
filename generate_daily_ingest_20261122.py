#!/usr/bin/env python3
"""Generate 2026-11-22 daily-ingest artifacts (ledger, lane dossiers, overview index)."""
import json, os, datetime

OUT = os.path.expanduser("~/Projects/artifact-library/artifacts/daily-ingest/2026-11-22")
os.makedirs(OUT, exist_ok=True)
DATE = "2026-11-22"
TS = datetime.datetime.now(datetime.timezone.utc).isoformat()

CSS = """      :root {
        --brand: #01dc82; --deep: #033330; --lime: #cfe66a; --red: #b3261e; --amber: #9a6700;
        --ink: #0f172a; --muted: #475569; --line: #e2e8f0; --bg: #fafaf9; --card: #ffffff;
        --serif: "Newsreader", Georgia, serif; --sans: "Plus Jakarta Sans", ui-sans-serif, system-ui, sans-serif;
      }
      * { box-sizing: border-box; }
      body { margin: 0; background: var(--bg); color: var(--ink); font-family: var(--sans); line-height: 1.55; }
      main { max-width: 64rem; margin: 0 auto; padding: 3rem 1.5rem; }
      h1 { font-family: var(--serif); color: var(--deep); font-size: 2rem; font-weight: 600; margin: 0; }
      h2 { font-family: var(--serif); color: var(--deep); font-size: 1.35rem; font-weight: 600; margin: 0 0 .5rem; }
      h3 { font-family: var(--serif); color: var(--deep); font-size: 1.05rem; font-weight: 600; margin: 0 0 .25rem; }
      a { color: var(--deep); }
      .wordmark { display: flex; align-items: center; gap: .6rem; font-weight: 700; color: var(--deep); letter-spacing: -0.01em; }
      header { display: flex; flex-direction: column; gap: 1.25rem; margin-bottom: 2.5rem; }
      section { display: flex; flex-direction: column; gap: 2rem; }
      .card { background: var(--card); border: 1px solid var(--line); border-radius: .75rem; padding: 1.5rem; }
      .badges { display: flex; flex-wrap: wrap; gap: .5rem; margin: .25rem 0 1rem; }
      .badge { font-size: .7rem; text-transform: uppercase; letter-spacing: .06em; font-weight: 600;
               padding: .15rem .5rem; border-radius: .35rem; background: #f1f5f9; color: var(--muted); }
      .badge.good { background: #dcfce7; color: #166534; }
      .badge.warn { background: #fef3c7; color: var(--amber); }
      .badge.spec { background: #e2e8f0; color: #334155; }
      .facts { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: .8rem; color: var(--muted);
               margin: 0 0 1rem; padding: 0; list-style: none; }
      .facts li { padding: .1rem 0; }
      .diagram { border: 1px solid var(--line); border-radius: .5rem; background: #fff; padding: 1rem; margin: 1rem 0; }
      .diagram svg { display: block; max-width: 100%; height: auto; }
      .label { font-size: .7rem; text-transform: uppercase; letter-spacing: .08em; fill: var(--muted); color: var(--muted); }
      .wins { margin: .5rem 0 0; padding-left: 1.1rem; }
      .wins li { margin: .15rem 0; }
      .callout { border-left: 3px solid var(--amber); background: #fffbeb; color: #713f12;
                 padding: .6rem .9rem; border-radius: .25rem; font-size: .9rem; }
      .hl { background: rgba(207,230,106,.6); padding: 0 .15em; }
      .seam { stroke-dasharray: 4 4; } .accent { stroke: var(--red); }
      .exec { font-size: 1.05rem; color: var(--ink); }
      .lede { color: var(--muted); font-size: .95rem; margin: .25rem 0 0; }
      dl { margin: .5rem 0 0; display: grid; grid-template-columns: 8.5rem 1fr; gap: .35rem .75rem; font-size: .92rem; }
      dt { font-weight: 700; color: var(--deep); }
      dd { margin: 0; }
      table { width: 100%; border-collapse: collapse; font-size: .85rem; }
      th, td { text-align: left; padding: .5rem .6rem; border-bottom: 1px solid var(--line); }
      th { font-size: .7rem; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); }
      td.ok { color: #166534; font-weight: 600; }
      td.mid { color: var(--amber); font-weight: 600; }
      .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr)); gap: 1rem; }
      .minicard { border: 1px solid var(--line); border-radius: .5rem; padding: .75rem .9rem; background: #fff; }
      .node { rx: 6; }
"""

LOGO = """<svg viewBox="0 0 164 195" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" width="22">
<path d="M117 194.5H0L12 73C17.47 66.63 21.30 65.46 28.5 64.5L34.5 0H151.5C158.44 4.40 161.28 7.18 163.5 13L153 119.5C148.80 127.15 144.97 129.55 135.5 130.5L131 184.5C127.71 190.35 125.13 192.98 117 194.5Z" fill="#01dc82"/>
<path d="M64 33L61 64.5H93.5L91 97H123L127.5 46.5C125.53 37.94 122.01 35.19 112.5 33H64Z" fill="#033330"/>
<path d="M37 147.5L41.5 98H74.5L71.5 129.5L104 130.5L100.5 162H49.5C41.82 159.35 39.68 155.53 37 147.5Z" fill="#033330"/></svg>"""

ARROW = """<defs><marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#94a3b8"/></marker></defs>"""

def arrow(x1,x2,y,label=None):
    t = f'<text x="{(x1+x2)/2}" y="{y-8}" text-anchor="middle" class="label">{label}</text>' if label else ""
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#94a3b8" marker-end="url(#ar)"/>{t}'

def box(x,y,w,h,txt,stroke="#cbd5e1"):
    return (f'<rect class="node" x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#fff" stroke="{stroke}"/>'
            f'<text x="{x+w/2}" y="{y+h/2+4}" text-anchor="middle" class="label">{txt}</text>')

def page(title, header_h1, exec_readout, body):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet"/>
<style>
{CSS}</style></head><body><main>
<header>
  <div class="wordmark">{LOGO}<span>Buildn</span></div>
  <h1>{header_h1}</h1>
  <p class="lede">{DATE} · Daily Ingest Dossier</p>
  <p class="exec">{exec_readout}</p>
</header>
{body}
</main></body></html>"""

# ---------- Lanes data ----------
lanes = []

# Lane 1: open web + self-hosting
lane1_body = f"""
<article class="card"><h2>Signal map</h2>
<div class="diagram"><svg viewBox="0 0 640 150" role="img" aria-label="Agents pressure the open web; self-hosters respond">
{ARROW}
{box(10,30,150,40,"AI scraping pressure")}
{box(210,10,130,34,"Reddit kills RSS", "var(--red)")}
{box(210,60,130,34,"Last.fm API paywall", "var(--red)")}
{box(210,110,130,34,"Infisical paywalls roles","var(--amber)")}
<line x1="160" y1="50" x2="206" y2="27" stroke="#94a3b8" marker-end="url(#ar)"/>
<line x1="160" y1="50" x2="206" y2="77" stroke="#94a3b8" marker-end="url(#ar)"/>
<line x1="160" y1="50" x2="206" y2="127" class="accent seam" marker-end="url(#ar)"/>
{box(410,35,120,40,"Self-host stack")}
<line x1="344" y1="77" x2="406" y2="57" stroke="#94a3b8" marker-end="url(#ar)"/>
{box(560,35,70,40,"Yours")}
<line x1="534" y1="55" x2="556" y2="55" stroke="#94a3b8" marker-end="url(#ar)"/>
</svg></div>
<p class="lede">Access closures cluster on the left (red), and each pushes users one step toward owned infrastructure on the right.</p>
</article>

<article class="card"><h2>The open web closes for agents</h2>
<div class="badges"><span class="badge warn">Structural shift</span><span class="badge">News</span></div>
<ul class="facts"><li>Reddit RSS feeds stopped working 2026-11-16</li><li>Last.fm API keys require Pro from 2026-12-01</li><li>OpenCloud restricts community users to rolling releases</li></ul>
<p><strong>What it is:</strong> Reddit ended public RSS/API access citing AI bots, and Last.fm starts charging for API keys used to scrobble from self-hosted music servers. OpenCloud joined the enterprise-repo pattern.</p>
<p><strong>Why it matters:</strong> Integrations you take for granted can lapse with a week of notice. Anything Buildn or a client depends on via someone else's free feed needs a fallback or a mirror.</p>
<dl><dt>Use cases</dt><dd>Audit every RSS/API dependency in automation and pipelines; pin mirrors or paid tiers.</dd></dl>
<ul class="wins"><li>Free integrations are now rentable</li><li>Plan before December 1</li><li>Mirror what you need</li></ul>
<div class="callout">Watch the ethical line too: closures target AI scraping, and your agent workflows will inherit the friction.</div>
</article>

<article class="card"><h2>PostgreSQL 19 released</h2>
<div class="badges"><span class="badge good">Major release</span><span class="badge">Database</span></div>
<ul class="facts"><li>https://www.postgresql.org/about/news/postgresql-19-released-3449/</li><li>Released 2026-11-19</li></ul>
<p><strong>What it is:</strong> The annual major release of the default database behind most Buildn v1 stacks.</p>
<p><strong>Why it matters:</strong> Major versions carry planner, replication, and management changes that both new projects and client migrations should plan around. Env Vault's Next.js + Postgres baseline should standardize on it.</p>
<dl><dt>Use cases</dt><dd>Default to 19 for new projects; read the release notes before any client upgrade.</dd></dl>
<ul class="wins"><li>New default for greenfield work</li><li>Check upgrade path per client</li><li>PgBouncer and extensions lag</li></ul>
<div class="callout">Extensions (pgvector etc.) usually trail major releases; verify compatibility before staging upgrades.</div>
</article>

<article class="card"><h2>Critical NGINX HTTP/2 RCE</h2>
<div class="badges"><span class="badge warn">Security</span><span class="badge">CVE</span></div>
<ul class="facts"><li>CVE-2026-123633, CVE-2026-123007</li><li>Unauthenticated remote code execution</li></ul>
<p><strong>What it is:</strong> Two critical HTTP/2 flaws in NGINX allow unauthenticated attackers to compromise servers, disclosed via Wiz's bulletin.</p>
<p><strong>Why it matters:</strong> NGINX fronts a huge share of self-hosted and client deployments. This is a patch-now item for every reverse proxy in your or your clients' infrastructure.</p>
<dl><dt>Use cases</dt><dd>Sweep homelab and client servers today; document NGINX versions in infra inventories.</dd></dl>
<ul class="wins"><li>Patch within the day</li><li>Unauthenticated means internet-facing first</li><li>Check ingress controllers too</li></ul>
</article>

<article class="card"><h2>Redict deprecated, converge on Valkey</h2>
<div class="badges"><span class="badge spec">Ecosystem</span><span class="badge">Cache</span></div>
<ul class="facts"><li>https://redict.io/posts/2026-11-17-redict-deprecated/</li><li>Maintainers recommend Valkey</li></ul>
<p><strong>What it is:</strong> The Redis fork built over licensing concerns is deprecated; maintainers point users to Valkey.</p>
<p><strong>Why it matters:</strong> The open-source cache ecosystem is consolidating on Valkey. New deployments should skip Redis-fork indecision and just use Valkey.</p>
<dl><dt>Use cases</dt><dd>Pick Valkey for new caches; plan a swap for any Redict instances.</dd></dl>
<ul class="wins"><li>Decision simplifies: Valkey</li><li>BSD-licensed, permissive</li><li>Mature multi-vendor backing</li></ul>
</article>

<article class="card"><h2>Infisical Agent Vault: brokers secrets to agents</h2>
<div class="badges"><span class="badge good">Directly relevant</span><span class="badge">Product</span></div>
<ul class="facts"><li>https://infisical.com/platform/agent-vault</li><li>Secrets never land in prompts or logs</li></ul>
<p><strong>What it is:</strong> A credential broker that gives AI agents scoped access at request time instead of handing over raw API keys.</p>
<p><strong>Why it matters:</strong> This validates and pressures the Env Vault thesis: device-scoped keys plus request-time brokering rather than long-lived shared secrets. Watch its model, then differentiate.</p>
<dl><dt>Use cases</dt><dd>Compare brokering model against Env Vault's device-key design; study what enterprises ask for.</dd></dl>
<ul class="wins"><li>Validates agent-secret gap</li><li>Free competitor pressure is good</li><li>Study, don't ignore</li></ul>
<div class="callout">Infisical also paywalled custom roles in a patch release — monitor their open-core balance as a market signal.</div>
</article>
"""
lanes.append(dict(slug="open-web-selfhosting", title="Open Web + Self-Hosting",
    rationale="Coverage gap since July; this week had exceptional signal: two open-web closures, Postgres 19, a critical NGINX RCE, and an agent-secrets product that touches Env Vault.",
    sources=[
      dict(title="Self-Host Weekly — 20 November 2026", url="https://selfh.st/weekly/2026-11-20/", source_type="blog", published_or_updated="2026-11-20", why_selected="Primary weekly source for self-hosting signal, not covered since July.", usefulness="One-stop scan of closures, releases, and security items."),
      dict(title="Reddit discontinues RSS feeds", url="https://techcrunch.com/2026/09/30/reddit-is-killing-rss-feeds-ending-public-api-access-because-of-ai-bots/", source_type="news", published_or_updated="2026-11-16", why_selected="Effective outage date this week; downstream tooling broke.", usefulness="Inventory free-API dependencies before they lapse."),
      dict(title="Last.fm API keys will require Pro from 1st December", url="https://support.last.fm/t/api-keys-will-require-pro-from-1st-december/121030", source_type="product", published_or_updated="2026-11", why_selected="Hard deadline in ten days affecting scrobbling integrations.", usefulness="Concrete date to act against."),
      dict(title="PostgreSQL 19 released", url="https://www.postgresql.org/about/news/postgresql-19-released-3449/", source_type="release", published_or_updated="2026-11-19", why_selected="Default database baseline for Buildn v1 stacks.", usefulness="Standardization target for new projects."),
      dict(title="Unauthenticated RCE in NGINX", url="https://wiz.io/blog/nginx-cve-2026-123633-123007", source_type="news", published_or_updated="2026-11-20", why_selected="Critical, unauthenticated, extremely widely deployed.", usefulness="Patch-now sweep of proxies and ingress."),
      dict(title="Redict deprecated", url="https://redict.io/posts/2026-11-17-redict-deprecated/", source_type="blog", published_or_updated="2026-11-17", why_selected="Ends the Redis-fork debate; consolidates on Valkey.", usefulness="Simplifies future cache decisions."),
      dict(title="Infisical Agent Vault", url="https://infisical.com/platform/agent-vault", source_type="product", published_or_updated="2026-11", why_selected="Direct competitor-signal for Env Vault's agent-secret thesis.", usefulness="Study their brokering model for differentiation."),
    ], body=lane1_body))

# Lane 2: design tooling
lane2_body = f"""
<article class="card"><h2>Signal map</h2>
<div class="diagram"><svg viewBox="0 0 640 140" role="img" aria-label="Figma designs flow through agent to code, under admin allowlist">
{ARROW}
{box(10,45,130,40,"Figma design")}
{arrow(144,196,65)}
{box(200,45,130,40,"Figma agent (Dev Mode)", "#01dc82")}
{arrow(334,386,65)}
{box(390,45,120,40,"Coding agent")}
{arrow(514,560,65)}
{box(564,45,66,40,"Code")}
<line x1="265" y1="45" x2="265" y2="18" stroke="#94a3b8" marker-end="url(#ar)"/>
{box(200,0,130,20,"OAuth allowlist")}
</svg></div>
<p class="lede">The design-to-code path now runs through an agent, and the admin console is the gatekeeper for which agents are allowed.</p>
</article>

<article class="card"><h2>Figma agent lands in Dev Mode</h2>
<div class="badges"><span class="badge good">High leverage</span><span class="badge">AI</span></div>
<ul class="facts"><li>Released 2026-11-19</li><li>Inspect, compare versions, bulk asset links</li></ul>
<p><strong>What it is:</strong> Prompt the Figma agent inside Dev Mode to explain designs, diff versions, request code snippets, and get bulk download links.</p>
<p><strong>Why it matters:</strong> The design-to-code handoff, the seam most client work stalls on, now has an in-tool agent. It directly affects Buildn's design-delivery workflow: fewer handoff documents, more interrogating the artifact.</p>
<dl><dt>Use cases</dt><dd>Use in next client design review; ask it for code snippets before writing components.</dd></dl>
<ul class="wins"><li>Handoff becomes a dialogue</li><li>Version diffs on demand</li><li>Bulk asset retrieval</li></ul>
</article>

<article class="card"><h2>3D transform, shipped straight to code</h2>
<div class="badges"><span class="badge good">New capability</span><span class="badge">Design</span></div>
<ul class="facts"><li>Released 2026-11-12</li><li>On-canvas x/y/z rotation; pairs with Figma Motion</li></ul>
<p><strong>What it is:</strong> Native 3D rotation with live previews, composable by the agent, exportable as CSS via Dev Mode or pushed through Figma MCP to a coding agent.</p>
<p><strong>Why it matters:</strong> Perspective and depth used to be a developer task. Now a designer can author a real 3D scene and the code path is one MCP call away — a small but real client-differentiator for marketing pages.</p>
<dl><dt>Use cases</dt><dd>Hero sections and product pages; hand motion specs to Figma Motion instead of custom JS.</dd></dl>
<ul class="wins"><li>3D without a 3D tool</li><li>CSS export, no plugin</li><li>MCP path for agents</li></ul>
</article>

<article class="card"><h2>Admin allowlist for OAuth apps and MCP clients</h2>
<div class="badges"><span class="badge good">Governance</span><span class="badge">Enterprise</span></div>
<ul class="facts"><li>Released 2026-11-17</li><li>Covers Cursor, Claude Code as MCP clients</li><li>Org/Enterprise rollout</li></ul>
<p><strong>What it is:</strong> Admins get an allowlist of approved OAuth apps including MCP clients, plus an Extensions tab to review requests.</p>
<p><strong>Why it matters:</strong> The same agent-identity governance theme seen in Buildn OS work, arriving in a design tool. Client orgs will ask who can connect which agents to their files; Buildn can answer first.</p>
<dl><dt>Use cases</dt><dd>Set client org policies before rollout; mirror the allowlist pattern in Env Vault sharing.</dd></dl>
<ul class="wins"><li>Agents get explicit grants</li><li>Requests reviewed, not surprised</li><li>Precedent for Buildn policies</li></ul>
</article>

<article class="card"><h2>Multi-model image generation in one prompt</h2>
<div class="badges"><span class="badge warn">Worth trying</span><span class="badge">AI</span></div>
<ul class="facts"><li>Released 2026-11-18</li><li>2/4/6 images per model, or 3 models in parallel</li></ul>
<p><strong>What it is:</strong> Make Image and Edit Image can fan out one prompt across counts or models, presenting options side by side.</p>
<p><strong>Why it matters:</strong> It turns image production into an option-selection workflow — the same fan-out-then-select pattern agents use everywhere. Faster to acceptable assets for client work.</p>
<dl><dt>Use cases</dt><dd>Client moodboards and hero art; compare models' house styles once, then pin one.</dd></dl>
<ul class="wins"><li>Fewer re-prompts</li><li>Model comparison in tool</li><li>Select, don't settle</li></ul>
</article>
"""
lanes.append(dict(slug="design-tooling", title="Design Tooling + Design-to-Code",
    rationale="Design-delivery lane last covered 2026-07-15; Figma shipped five agent-era releases in the past ten days, including MCP-client governance that mirrors Buildn's identity work.",
    sources=[
      dict(title="Work with the Figma agent in dev mode", url="https://www.figma.com/release-notes/", source_type="release", published_or_updated="2026-11-19", why_selected="Agent arrives at the design-code seam.", usefulness="Replace static handoff docs with in-tool queries."),
      dict(title="Design in 3D natively in Figma", url="https://help.figma.com/hc/en-us/articles/44568893374999", source_type="release", published_or_updated="2026-11-12", why_selected="New native capability with a code export path.", usefulness="Client marketing-page differentiator."),
      dict(title="Allowlist of approved OAuth apps including MCP clients", url="https://help.figma.com/hc/en-us/articles/44716871463319", source_type="release", published_or_updated="2026-11-17", why_selected="Enterprise agent-governance in a design tool.", usefulness="Mirror the pattern in Buildn client policies."),
      dict(title="Generate multiple images from a single prompt", url="https://help.figma.com/hc/en-us/articles/24004542669463", source_type="release", published_or_updated="2026-11-18", why_selected="Fan-out-select production pattern for assets.", usefulness="Faster acceptable assets for client work."),
      dict(title="Figma Motion: physics springs and Lottie previews", url="https://help.figma.com/hc/en-us/articles/41414048690839", source_type="release", published_or_updated="2026-11-10", why_selected="Motion specs become design-system artifacts.", usefulness="Preserve springs in design systems at scale."),
    ], body=lane2_body))

# Lane 3: OSS from Show HN
lane3_body = f"""
<article class="card"><h2>Signal map</h2>
<div class="diagram"><svg viewBox="0 0 640 140" role="img" aria-label="Agent session traces become rules; computer-use agents self-host">
{ARROW}
{box(10,40,150,44,"Agent session logs")}
{box(210,40,140,44,"trace2rules mining", "#01dc82")}
{arrow(354,404,62)}
{box(408,40,120,44,"AGENTS.md rules")}
{arrow(532,576,62)}
{box(580,40,50,44,"CI")}
<line x1="85" y1="40" x2="120" y2="10" class="accent seam" marker-end="url(#ar)"/>
{box(120,0,160,20,"OpenComputer: self-host computer agents")}
</svg></div>
<p class="lede">Two clusters: evidence pipelines that turn what agents did into what agents should do, and self-hosted alternatives to hosted agents.</p>
</article>

<article class="card"><h2>trace2rules: evidence-backed AGENTS.md</h2>
<div class="badges"><span class="badge good">Try today</span><span class="badge">OSS</span></div>
<ul class="facts"><li>https://github.com/rkkautsar/trace2rules</li><li>MIT · Python · v0.2.3 (2026-11-21)</li><li>Ingests Claude Code, Codex, Pi, OpenCode logs</li></ul>
<p><strong>What it is:</strong> A local CLI that mines your coding-agent session logs, audits existing AGENTS.md/CLAUDE.md rules against real sessions, and marks each rule observed, violated, unobserved, or already CI-enforced. Output is a proposal, never an auto-apply.</p>
<p><strong>Why it matters:</strong> Most AGENTS.md files are folklore. This replaces vibes with verdicts — and it reads the exact session stores this machine already has (Claude Code, Pi, OpenCode). It can generate Hermes-side evidence for the PR-review skill too.</p>
<dl><dt>Use cases</dt><dd>Audit the main buildn repo's AGENTS.md; mine repeat friction into enforced rules.</dd></dl>
<ul class="wins"><li>Rules with receipts</li><li>Local-only, privacy-safe</li><li>DuckDB-backed, fast</li></ul>
<div class="callout">Needs ~10+ local sessions for meaningful audits; detectors are heuristics — review every proposal.</div>
</article>

<article class="card"><h2>OpenComputer: open-source Devin alternative</h2>
<div class="badges"><span class="badge warn">Watch</span><span class="badge">OSS</span></div>
<ul class="facts"><li>https://github.com/diggerhq/opencomputer</li><li>Apache 2.0 · TypeScript · 1.3k stars · 218 releases</li><li>2.6x faster first push than hosted cloud agents</li></ul>
<p><strong>What it is:</strong> An open, self-hostable platform for running computer-use coding agents in isolated sessions, from the Digger team. Active daily commits; production configs kept in a private deploy repo.</p>
<p><strong>Why it matters:</strong> The "hosted agent vs owned agent" trade is becoming a real choice. For client work with confidentiality constraints, an owned computer-agent platform may beat sending repos to a hosted runner.</p>
<dl><dt>Use cases</dt><dd>Pilot for private-repo client tasks where hosted agents are a non-starter.</dd></dl>
<ul class="wins"><li>Owned infrastructure option</li><li>Bring-your-own model keys</li><li>Very active development</li></ul>
<div class="callout">Young project; benchmark claims come from the vendor's own tests.</div>
</article>

<article class="card"><h2>Straum: live Postgres aggregates, no triggers</h2>
<div class="badges"><span class="badge warn">Worth exploring</span><span class="badge">OSS</span></div>
<ul class="facts"><li>https://github.com/janbjorge/straum</li><li>Show HN, 2026-11-21</li></ul>
<p><strong>What it is:</strong> Real-time aggregates over Postgres without triggers or extensions.</p>
<p><strong>Why it matters:</strong> Dashboards and activity feeds are the first thing every client asks for and the first thing triggers/extensions complicate. A plain-python drop-in could simplify the v1 stack.</p>
<dl><dt>Use cases</dt><dd>Live task dashboards; real-time client reporting without ETL.</dd></dl>
<ul class="wins"><li>No schema surgery</li><li>Fits Next.js + Postgres v1</li><li>Early-stage, small surface</li></ul>
</article>

<article class="card"><h2>agent-mcts: tree search on top of Claude Code</h2>
<div class="badges"><span class="badge spec">Speculative</span><span class="badge">OSS</span></div>
<ul class="facts"><li>https://github.com/natsu0529/agent-mcts</li><li>Show HN, 2026-11-21</li></ul>
<p><strong>What it is:</strong> Monte Carlo tree search orchestration over a coding agent, exploring multiple solution branches before committing.</p>
<p><strong>Why it matters:</strong> An orchestration pattern, not a product: search-and-select applied to coding sessions. Even a skim of the architecture informs how Buildn workflows could branch-and-merge agent attempts.</p>
<dl><dt>Use cases</dt><dd>Compare against linear per-repo event histories; borrow for workflow branching design.</dd></dl>
<ul class="wins"><li>Search beats single attempts</li><li>Maps to Buildn branching plans</li><li>Cheap to study</li></ul>
</article>
"""
lanes.append(dict(slug="oss-showhn", title="OSS + Coding Agent Experiments",
    rationale="Fresh, un-duplicated Show HN signal this week: three projects map directly onto Buildn's agent-evidence and infra plans, and none have appeared in the coverage ledger.",
    sources=[
      dict(title="trace2rules", url="https://github.com/rkkautsar/trace2rules", source_type="repo", published_or_updated="2026-11-21", why_selected="Audits agent rules against real sessions using stores this machine already has.", usefulness="Immediate AGENTS.md hygiene tool."),
      dict(title="OpenComputer", url="https://github.com/diggerhq/opencomputer", source_type="repo", published_or_updated="2026-11-22", why_selected="Open, self-hostable computer-use agent platform with an active community.", usefulness="Owned-agent option for confidential client work."),
      dict(title="Straum", url="https://github.com/janbjorge/straum", source_type="repo", published_or_updated="2026-11-21", why_selected="Live Postgres aggregates without triggers or extensions.", usefulness="Simplifies dashboards in the v1 stack."),
      dict(title="agent-mcts", url="https://github.com/natsu0529/agent-mcts", source_type="repo", published_or_updated="2026-11-21", why_selected="Tree-search orchestration over coding agents.", usefulness="Pattern study for workflow branching."),
      dict(title="Ripcloc — cloc every agent edit", url="https://github.com/alfredjeanlab/ripcloc", source_type="repo", published_or_updated="2026-11-21", why_selected="Cheap per-edit accounting of agent churn.", usefulness="Feeds cost-and-scale reporting in reports."),
    ], body=lane3_body))

# Lane 4: marketing analytics
lane4_body = f"""
<article class="card"><h2>Signal map</h2>
<div class="diagram"><svg viewBox="0 0 640 140" role="img" aria-label="Agents become a traffic and scoring channel marketers can finally observe">
{ARROW}
{box(10,45,140,40,"AI agents visit sites")}
{arrow(154,204,65)}
{box(208,45,140,40,"Clarity Agent Activity", "#01dc82")}
{arrow(352,402,65)}
{box(406,45,120,40,"Friction report")}
{arrow(530,576,65)}
{box(580,45,50,40,"Fix")}
<line x1="278" y1="85" x2="278" y2="115" stroke="#94a3b8" marker-end="url(#ar)"/>
{box(200,115,160,22,"Simulation: can an agent check out?")}
</svg></div>
<p class="lede">Analytics vendors are racing to make agent traffic observable, testable, and scoreable — turning AI referrals from a mystery line into an optimization surface.</p>
</article>

<article class="card"><h2>Microsoft Clarity adds agentic analytics</h2>
<div class="badges"><span class="badge good">Free to try</span><span class="badge">Product</span></div>
<ul class="facts"><li>Announced 2026-11-04</li><li>Agent Activity dashboard + simulations + Ask Clarity</li><li>Free tool</li></ul>
<p><strong>What it is:</strong> Clarity can now show which AI agents visit a site and what they do, run simulations testing whether an agent can complete checkout or booking, and answer natural-language questions backed by session evidence.</p>
<p><strong>Why it matters:</strong> Egypt fitout lead-gen work lives or dies on form and funnel friction. Agent traffic is small but growing, and Microsoft claims ~2M agents, double in three weeks. The simulation output is a literal fix list.</p>
<dl><dt>Use cases</dt><dd>Enable Clarity on client sites; run one simulation per key journey; fix popups and form walls.</dd></dl>
<ul class="wins"><li>Zero-cost first look</li><li>Simulation gives a fix list</li><li>Session-evidence answers</li></ul>
<div class="callout">Simulations reflect Microsoft's test agent, not every real agent; detection accuracy is unproven.</div>
</article>

<article class="card"><h2>GA4 release cadence worth tracking</h2>
<div class="badges"><span class="badge warn">Maintenance</span><span class="badge">Analytics</span></div>
<ul class="facts"><li>Releases 2026-11-18, 11-11, 11-06</li><li>https://support.google.com/analytics/answer/9164320</li></ul>
<p><strong>What it is:</strong> Three GA4 releases in under two weeks; the "What's new" changelog is the canonical list.</p>
<p><strong>Why it matters:</strong> Every client audit this month should diff against the newest GA4 behaviour before recommending anything stale.</p>
<dl><dt>Use cases</dt><dd>Read the November entries before the next client GA4 setup.</dd></dl>
<ul class="wins"><li>Fresh releases, recent dates</li><li>Baseline for audits</li><li>Five-minute read</li></ul>
</article>

<article class="card"><h2>ChatGPT starts keeping score</h2>
<div class="badges"><span class="badge good">Signal</span><span class="badge">Research</span></div>
<ul class="facts"><li>https://www.getlooploop.com/news/marketing-analytics-first-half-of-november-2026-chatgpt-starts-keeping-score</li><li>First half of November 2026</li></ul>
<p><strong>What it is:</strong> Roundup of analytics changes centered on ChatGPT surfacing its own scoring/visibility data, with a warning not to read the AI referral line as the size of AI's effect.</p>
<p><strong>Why it matters:</strong> Attribution for AI discovery is becoming a first-class metric. For marketing clients, "visibility in answer engines" will soon be a deliverable with a number attached.</p>
<dl><dt>Use cases</dt><dd>Add an AI-visibility line to client monthly reports; measure before promising GEO work.</dd></dl>
<ul class="wins"><li>Attribution gets quantified</li><li>Referral ≠ total effect</li><li>Reportable metric arriving</li></ul>
</article>

<article class="card"><h2>96% of B2B firms invisible in early AI discovery</h2>
<div class="badges"><span class="badge good">Positioning</span><span class="badge">Research</span></div>
<ul class="facts"><li>https://martech.org/7-b2b-marketing-shifts-that-will-define-2027/</li><li>2026 2X AI Visibility Index</li></ul>
<p><strong>What it is:</strong> The 2026 2X AI Visibility Index found 96% of studied B2B companies invisible in early-stage AI discovery, and martech's 2027 trends piece builds the playbook around it.</p>
<p><strong>Why it matters:</strong> That is a service gap waiting for a productized offer: AI-visibility audits. It's also a pitch hook — most client sites sit in the 96%.</p>
<dl><dt>Use cases</dt><dd>Productize an AI-visibility audit; use the 96% stat in outreach copy (no em dashes).</dd></dl>
<ul class="wins"><li>Quantified market gap</li><li>Audits are sellable</li><li>2027 playbook framing</li></ul>
</article>
"""
lanes.append(dict(slug="marketing-analytics", title="Marketing, Growth + Analytics",
    rationale="Marketing lane last covered 2026-07-14; November delivered an unusual analytics story: agent traffic becoming observable and scoreable, which is directly sellable to lead-gen clients.",
    sources=[
      dict(title="Microsoft Clarity agentic analytics", url="https://nowoka.com/blog/microsoft-clarity-agentic-analytics-ai-agents/", source_type="blog", published_or_updated="2026-11-07", why_selected="Detailed practical walkthrough of the November 4 Clarity launch.", usefulness="How-to plan for agent-funnel auditing."),
      dict(title="What's new in Google Analytics (Nov releases)", url="https://support.google.com/analytics/answer/9164320?hl=en", source_type="docs", published_or_updated="2026-11-18", why_selected="Primary changelog for GA4 audit baselines.", usefulness="Keep client setups current."),
      dict(title="Marketing analytics 1–18 Nov 2026: ChatGPT starts keeping score", url="https://www.getlooploop.com/news/marketing-analytics-first-half-of-november-2026-chatgpt-starts-keeping-score", source_type="news", published_or_updated="2026-11-18", why_selected="Timely roundup on AI attribution scoring.", usefulness="Frames referral-vs-effect measurement."),
      dict(title="7 B2B marketing shifts that will define 2027", url="https://martech.org/7-b2b-marketing-shifts-that-will-define-2027/", source_type="blog", published_or_updated="2026-11", why_selected="Carries the 96%-invisible finding and the 2027 playbook.", usefulness="Positioning stat for a productized audit."),
    ], body=lane4_body))

lane_data = {
 "open-web-selfhosting": dict(
   exec="The open web is being repriced under agents' feet. This week alone Reddit shut RSS, Last.fm paywalled API keys, and a critical NGINX RCE forced a patch sweep, while PostgreSQL 19 and Valkey quietly became the safer defaults for owned infrastructure.",
   matrix=[
     ("Open-web closures",("mid","Fallback plans"),("warn","Integrations at risk"),("ok","Direct"),("mid","Mirrors")),
     ("PostgreSQL 19",("ok","Default stack"),("ok","Migration target"),("mid","Agent DBs"),("ok","Homelab")),
     ("NGINX RCE",("mid","Infra hygiene"),("ok","Patch now"),("mid","Ingress"),("ok","Patch now")),
     ("Valkey convergence",("mid","Cache choice"),("mid","Simpler stacks"),("mid","Cache"),("ok","Homelab")),
     ("Infisical Agent Vault",("ok","Env Vault signal"),("mid","Secret posture"),("ok","Direct"),("mid","Study")),
   ],
   top_actions=["Inventory every free RSS/API dependency in automation and pipelines","Patch internet-facing NGINX and client proxies for the HTTP/2 CVEs","Read the Infisical Agent Vault model and note Env Vault deltas","Adopt PostgreSQL 19 as the greenfield default"]),
 "design-tooling": dict(
   exec="Figma shipped five agent-era releases in ten days: an agent inside Dev Mode, native 3D with a code path, and an admin allowlist for MCP clients. The design-to-code seam is turning into a governed agent conversation.",
   matrix=[
     ("Figma agent in Dev Mode",("ok","Design docs"),("ok","Handoff"),("ok","Direct"),("ok","Daily use")),
     ("3D transform + CSS/MCP",("mid","Future"),("ok","Marketing pages"),("ok","MCP push"),("mid","Experiment")),
     ("OAuth/MCP allowlist",("ok","Policy mirror"),("ok","Org rollout"),("ok","Direct"),("mid","Study")),
     ("Multi-image generation",("mid","Assets"),("ok","Moodboards"),("mid","Fan-out"),("ok","Quick win")),
     ("Motion springs/Lottie",("mid","Design system"),("mid","Prototypes"),("mid","Spec source"),("ok","Try")),
   ],
   top_actions=["Use the Figma agent in Dev Mode in the next client design review","Try 3D transform on one hero section and push CSS to a coding agent","Draft an MCP-client allowlist policy template for client orgs"]),
 "oss-showhn": dict(
   exec="This week's Show HN crop leans toward evidence: trace2rules turns your agent session logs into audited AGENTS.md rules, OpenComputer offers a self-hosted Devin alternative, and Straum gives Postgres live aggregates with zero schema surgery.",
   matrix=[
     ("trace2rules",("ok","AGENTS.md audit"),("mid","Client rules"),("ok","Direct"),("ok","Today")),
     ("OpenComputer",("mid","Future host"),("ok","Private repos"),("ok","Direct"),("mid","Pilot")),
     ("Straum",("mid","Dashboards"),("ok","v1 stack"),("mid","Feeds"),("mid","Explore")),
     ("agent-mcts",("ok","Branching study"),("mid","Experiment"),("ok","Pattern"),("mid","Read")),
     ("Ripcloc",("mid","Churn metrics"),("mid","Reporting"),("ok","Direct"),("ok","Install")),
   ],
   top_actions=["Run trace2rules audit on the main buildn repo today","Skim OpenComputer's architecture for the owned-agent option","Compare agent-mcts branching against Buildn workflow branching plans"]),
 "marketing-analytics": dict(
   exec="Agent traffic is becoming an observable channel: Clarity now shows which AI agents visit a site and simulates whether they can check out, ChatGPT is quantifying its own attribution, and 96% of B2B firms are still invisible in AI discovery. That combination is a productized offer waiting to be made.",
   matrix=[
     ("Clarity agentic analytics",("mid","Telemetry"),("ok","Lead-gen sites"),("ok","Direct"),("ok","Enable")),
     ("GA4 November releases",("mid","Reporting"),("ok","Audits"),("mid","Data"),("ok","Read")),
     ("ChatGPT scoring",("mid","Metrics"),("ok","Attribution"),("mid","Watch"),("mid","Study")),
     ("96% AI-visibility gap",("ok","Content angle"),("ok","Service offer"),("mid","Research"),("ok","Pitch")),
   ],
   top_actions=["Enable Clarity and run one agent simulation per client key journey","Productize an AI-visibility audit using the 96% stat in outreach","Diff GA4 changes against every client setup before the next audit"]),
}
for lane in lanes:
    lane.update(lane_data[lane["slug"]])

# regenerate with data-filled pages
for lane in lanes:
    html = page(
        f"Daily Ingest Dossier — {lane['title']} — {DATE}",
        f"Daily Ingest Dossier — {lane['title']}",
        lane["exec"],
        lane["body"] +
        f"""
<article class="card"><h2>Use-case matrix</h2>
<table><thead><tr><th>Item</th><th>Buildn OS</th><th>Client work</th><th>Agent workflows</th><th>Personal leverage</th></tr></thead><tbody>
{''.join(f"<tr><td>{a}</td><td class='{b[0]}'>{b[1]}</td><td class='{c[0]}'>{c[1]}</td><td class='{d[0]}'>{d[1]}</td><td class='{e[0]}'>{e[1]}</td></tr>" for a,b,c,d,e in lane["matrix"])}</tbody></table>
</article>

<article class="card"><h2>Top actions</h2>
<ol class="wins">{''.join(f'<li>{x}</li>' for x in lane["top_actions"])}</ol>
</article>

<article class="card"><h2>Source trail</h2>
<ul class="facts">{''.join(f'<li><a href="{s["url"]}">{s["url"]}</a></li>' for s in lane["sources"])}</ul>
</article>""",
    )
    fname = f"daily-ingest-{lane['slug']}-20261122.html"
    open(os.path.join(OUT, fname), "w").write(html)
    lane["file"] = fname

# ---------- ledger ----------
ledger = {
  "date": DATE,
  "generated_at": TS,
  "editorial_thesis": "The open web is being repriced under agents' feet while everyday tooling absorbs agents silently, so the leverage is in adopting agent-aware versions of infrastructure and analytics you already run.",
  "topic_groups": [
    {"slug": l["slug"], "title": l["title"], "selection_rationale": l["rationale"], "sources": l["sources"]} for l in lanes
  ],
}
json.dump(ledger, open(os.path.join(OUT, "ledger.json"), "w"), indent=2)
json.dump(ledger, open(os.path.join(OUT, "ledger-20261122.json"), "w"), indent=2)

# ---------- overview index ----------
lane_links = "\n".join(
  f'''<a class="minicard" href="{l['file']}" style="text-decoration:none"><h3>{l['title']}</h3><p class="lede">{l['rationale']}</p></a>'''
  for l in lanes)
top3 = """<ul class="wins">
<li><span class="hl">trace2rules</span> — audit this machine's real agent sessions into evidence-backed AGENTS.md rules (works with Pi, Claude Code, OpenCode logs).</li>
<li><span class="hl">Microsoft Clarity agentic analytics</span> — free agent-traffic dashboard and checkout simulations; an immediate add-on for lead-gen client sites.</li>
<li><span class="hl">Figma agent in Dev Mode</span> — the design-to-code handoff becomes a dialogue; try it in the next client review, plus 3D transform with one-call CSS export.</li>
</ul>"""
overview = page(
  f"Daily Ingest Dossier — {DATE}",
  f"Daily Ingest Dossier",
  "Today's edition rotates to coverage gaps: the open web's access closures, Figma's agent-era design tooling, an unusually evidence-heavy Show HN crop, and analytics vendors making agent traffic observable. Across all four lanes, agents are being made governable: scoped access, audited rules, allowlisted clients, and measurable traffic.",
  f"""
<article class="card"><h2>Lane selection</h2>
<div class="grid">{lane_links}</div>
</article>
<article class="card"><h2>All-lanes top three</h2>{top3}</article>
<article class="card"><h2>Editorial thesis</h2>
<p>Self-hosting absorbs what the open web closes; design and analytics tools are quietly becoming agent platforms; and the OSS community is building the evidence layer for agent behaviour. Every lane points the same way: adopt agent-aware versions of the tools already in use, and keep credentials, rules, and policy in owned, auditable places.</p>
</article>
<article class="card"><h2>Archive</h2>
<ul class="facts"><li><a href="https://buildn-tech.github.io/daily-ingest/">https://buildn-tech.github.io/daily-ingest/</a></li><li><a href="https://buildn-tech.github.io/daily-ingest/2026-11-22/">https://buildn-tech.github.io/daily-ingest/2026-11-22/</a></li></ul>
</article>""")
open(os.path.join(OUT, "index.html"), "w").write(overview)

print("written:", sorted(os.listdir(OUT)))
