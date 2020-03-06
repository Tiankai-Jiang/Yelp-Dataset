import json

users = set()
business = set()

for i in range(1, 15):
    data = [json.loads(line) for line in open('../raw.nosync/yelp_dataset/review/review' + str(i) + '.json', 'r')]
    for d in data:
        users.add(d['user_id'])
        business.add(d['business_id'])

with open('../raw.nosync/usersInReviews.txt', 'w') as f:
    for a in users:
        f.write(a + '\n')

with open('../raw.nosync/businessInReviews.txt', 'w') as f:
    for a in business:
        f.write(a + '\n')