import json

dates = set()

data = [json.loads(line) for line in open('../raw.nosync/yelp_dataset/checkin.json', 'r')]
for d in data:
    for i in d['date'].split(', '):
        dates.add((d['business_id'], i))

res = sorted(list(dates))
with open('../raw.nosync/checkin.txt', 'w') as f:
    for d in res:
        f.write(d[0] + ',' + d[1] + '\n')