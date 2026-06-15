import urllib.request
import urllib.parse
import json
import os
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))
now = datetime.now(JST)
ymd = now.strftime('%Y%m%d')

API_KEY = os.environ['CONNPASS_API_KEY']

prefectures = ['tokyo', 'kanagawa', 'saitama', 'chiba']
all_events = []

for pref in prefectures:
    params = urllib.parse.urlencode({
        'prefecture': pref,
        'ymd': ymd,
        'count': 100,
        'order': 2
    })
    url = f'https://connpass.com/api/v2/events/?{params}'
    req = urllib.request.Request(url, headers={'X-API-Key': API_KEY})
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            data = json.loads(res.read())
            evs = data.get('events', [])
            all_events.extend(evs)
            print(f"{pref}: {len(evs)}件")
    except Exception as e:
        print(f"Error {pref}: {e}")

seen = set()
unique = []
for ev in all_events:
    if ev['id'] not in seen:
        seen.add(ev['id'])
        unique.append(ev)

output = {
    'fetched_at': now.isoformat(),
    'date': ymd,
    'count': len(unique),
    'events': unique
}

os.makedirs('data', exist_ok=True)
with open('data/connpass_events.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"合計: {len(unique)}件 → data/connpass_events.json")
