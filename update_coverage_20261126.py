#!/usr/bin/env python3
"""Update topic-coverage.json and seen-sources.json for the 2026-11-26 run."""
import json, hashlib, urllib.request
from datetime import datetime, timezone

PAGES = '/root/Projects/daily-ingest-pages'
ledger = json.load(open(f'{PAGES}/2026-11-26/ledger.json'))
cov = json.load(open(f'{PAGES}/topic-coverage.json'))
seen = json.load(open(f'{PAGES}/seen-sources.json'))

today = '2026-11-26'

# ---- rolling theme summary -------------------------------------------------
for g in ledger['topic_groups']:
    slug = g['slug']
    entry = cov['rolling_theme_summary'].setdefault(slug, {'title': g['title'], 'times_covered': 0})
    entry['title'] = g['title']
    entry['times_covered'] = entry.get('times_covered', 0) + 1
    entry['last_covered'] = today
    entry['last_selection_rationale'] = g['selection_rationale'][:300]

# ---- item history (keep 45 days) ------------------------------------------
CUTOFF = '2026-10-12'
new_items = []
for g in ledger['topic_groups']:
    for s in g['sources']:
        new_items.append({
            'date': today,
            'topic': g['slug'],
            'topic_title': g['title'],
            'title': s['title'],
            'url': s['url'],
            'source_type': s['source_type'],
            'published_or_updated': s['published_or_updated'],
            'selection_rationale': g['selection_rationale'][:300],
            'usefulness': s['usefulness'],
        })
hist = [h for h in cov['item_history'] if h.get('date', '') >= CUTOFF]
hist.extend(new_items)
cov['item_history'] = hist

# ---- seen-sources ----------------------------------------------------------
srcs = seen['sources']
for item in new_items:
    url = item['url']
    if isinstance(srcs, dict) and url not in srcs:
        srcs[url] = {'title': item['title'], 'first_seen': today,
                     'source_type': item['source_type']}
seen['updated_at'] = datetime.now(timezone.utc).isoformat()

json.dump(cov, open(f'{PAGES}/topic-coverage.json', 'w'), indent=2, ensure_ascii=False)
json.dump(seen, open(f'{PAGES}/seen-sources.json', 'w'), indent=2, ensure_ascii=False)
print(f'coverage: themes={len(cov["rolling_theme_summary"])} items={len(hist)} seen_urls={len(srcs)} new_items={len(new_items)}')
