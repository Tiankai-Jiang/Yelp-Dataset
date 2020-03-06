import json

hours = []

days = {"Monday": "Mon", "Tuesday": "Tue", "Wednesday": "Wed", "Thursday": "Thu", "Friday": "Fri", "Saturday": "Sat", "Sunday": "Sun"}

data = [json.loads(line) for line in open('../raw.nosync/yelp_dataset/business.json', 'r')]
for d in data:
    if d['hours']:
        for k, v in d['hours'].items():
            hours.append((d['business_id'], days[k], v))

with open('../raw.nosync/hours.txt', 'w') as f:
    for h in hours:
        f.write(h[0] + ' ' + h[1] + ' ' + h[2] + '\n')