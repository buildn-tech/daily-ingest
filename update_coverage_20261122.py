import json, datetime
d = json.load(open("topic-coverage.json"))
ledger = json.load(open("2026-11-22/ledger.json"))
today = "2026-11-22"
themes = d["rolling_theme_summary"]
history = d.get("item_history", [])
for g in ledger["topic_groups"]:
    slug = g["slug"]
    t = themes.setdefault(slug, {"title": g["title"], "times_covered": 0, "last_covered": None})
    t["times_covered"] = t.get("times_covered", 0) + 1
    t["last_covered"] = today
    for s in g["sources"]:
        history.append({
            "date": today, "topic": slug, "title": s["title"],
            "url": s["url"], "source_type": s["source_type"],
            "rationale": s["why_selected"],
        })
d["item_history"] = history[-260:]  # prune, folds into rolling summary
d["last_run"] = today
json.dump(d, open("topic-coverage.json", "w"), indent=2)
# also update seen-sources in repo copy
seen = json.load(open("seen-sources.json"))
for g in ledger["topic_groups"]:
    for s in g["sources"]:
        seen["sources"].setdefault(s["url"], {"first_seen": today})
        seen["sources"][s["url"]]["last_seen"] = today
        seen["sources"][s["url"]]["title"] = s["title"]
seen["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(seen, open("seen-sources.json", "w"), indent=2)
print("coverage updated:", len(history), "items,", len(themes), "themes")
