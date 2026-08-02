from pathlib import Path
import json
from datetime import date, datetime, timezone, timedelta
ROOT=Path('/root/Projects/daily-ingest-pages')
coverage_path=ROOT/'topic-coverage.json'
ledger=json.loads(Path('/root/Projects/artifact-library/artifacts/daily-ingest/daily-ingest-20260801.json').read_text())
coverage=json.loads(coverage_path.read_text())
today=date.fromisoformat(ledger['date'])
summary=coverage.setdefault('rolling_theme_summary',{})
history=coverage.setdefault('item_history',[])
# Preserve any existing current-date detail; only add URLs not already recorded.
existing={(x.get('date'),x.get('url')) for x in history if isinstance(x,dict)}
for group in ledger['topic_groups']:
    slug=group['slug']
    prior=summary.get(slug,{})
    summary[slug]={
        'title':group['title'],
        'times_covered':int(prior.get('times_covered',0))+ (0 if prior.get('last_covered')==ledger['date'] else 1),
        'last_covered':ledger['date']
    }
    for source in group['sources']:
        key=(ledger['date'],source['url'])
        if key not in existing:
            history.append({'date':ledger['date'],'lane':slug,'title':source['title'],'url':source['url'],'source_type':source['source_type'],'selection_rationale':source['why_selected']})
            existing.add(key)
cutoff=(today-timedelta(days=45)).isoformat()
coverage['item_history']=[x for x in history if isinstance(x,dict) and x.get('date','')>=cutoff]
coverage['updated_at']=datetime.now(timezone.utc).isoformat()
coverage['last_editorial_thesis']=ledger['editorial_thesis']
coverage_path.write_text(json.dumps(coverage,indent=2)+"\n")
print('coverage updated:',len(coverage['item_history']),'items retained')
