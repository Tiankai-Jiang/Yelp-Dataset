import json

users = set()
business = set()

data = [json.loads(line) for line in open('../raw.nosync/yelp_dataset/tip.json', 'r')]
for d in data:
    users.add(d['user_id'])
    business.add(d['business_id'])

with open('../raw.nosync/usersInTips.txt', 'w') as f:
    for a in users:
        f.write(a + '\n')

with open('../raw.nosync/businessInTips.txt', 'w') as f:
    for a in business:
        f.write(a + '\n')