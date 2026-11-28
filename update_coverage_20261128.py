import json
from datetime import datetime, timezone

path = "/root/Projects/daily-ingest-pages/topic-coverage.json"
with open(path) as f:
    cov = json.load(f)

date = "2026-11-28"
now = datetime.now(timezone.utc).isoformat()

lanes = {
    "platform-trust-incidents": {
        "title": "Platform Trust Incidents",
        "rationale": "1Password breach entered through an employee GitHub account and CI/CD, not vaults; the WebRTC Black Friday skimmer and RansomwareHelp fraud indictment share the trusted-intermediary failure shape. No overlap with Nov 25-26 supply-chain lanes.",
    },
    "agent-behavior-assurance": {
        "title": "Agent Behavior Assurance",
        "rationale": "Claude-sabotage thread (HN 694 pts) makes agent-assurance a material update: intent unproven but the multi-variable-edit failure and one-change-at-a-time harness fix are concrete; paired with DJB's false computer-checked proofs.",
    },
    "agent-dev-tooling": {
        "title": "Agent Dev Tooling Wave",
        "rationale": "GitHub trending snapshot: obra/superpowers, HKUDS CLI-Anything, OpenSRE, cursor/plugins, unkernel. All new projects; the skills/interfaces theme last ran Nov 17.",
    },
    "local-inference-boosts": {
        "title": "Local Inference Boosts",
        "rationale": "Extends Nov 23 local-models lane with hardware leverage instead of weights: AMD RDNA llama.cpp patches (~2x prefill), Rayshader 1.0, chiller-free datacenter economics.",
    },
}

summary = cov.setdefault("rolling_theme_summary", {})
for slug, meta in lanes.items():
    entry = summary.get(slug, {})
    entry["title"] = meta["title"]
    entry["times_covered"] = entry.get("times_covered", 0) + 1
    entry["last_covered"] = date
    entry["last_selection_rationale"] = meta["rationale"]
    summary[slug] = entry

# Append item-level history, then prune old items beyond 60 days.
items = cov.setdefault("items", [])
ledger = json.load(open("/root/Projects/artifact-library/artifacts/daily-ingest/daily-ingest-20261128.json"))
for group in ledger["topic_groups"]:
    for s in group["sources"]:
        items.append({
            "date": date,
            "lane": group["slug"],
            "title": s["title"],
            "url": s["url"],
            "source_type": s["source_type"],
            "published_or_updated": s.get("published_or_updated", "unknown"),
        })

cutoff = "2026-09-29"
kept = [i for i in items if i.get("date", "") >= cutoff]
cov["items"] = kept
cov["items_pruned_before"] = cutoff
cov["last_updated"] = now

with open(path, "w") as f:
    json.dump(cov, f, indent=2, ensure_ascii=False)
print("updated:", len(kept), "items retained;", len(items) - len(kept), "pruned")
