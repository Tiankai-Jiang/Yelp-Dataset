import json

s = set()

data = [json.loads(line) for line in open('../raw.nosync/yelp_dataset/business.json', 'r')]

# for d in data:
#     if d['attributes'] is not None:
#         for k, v in d['attributes'].items():
#             s.add(k)

# print(s)

for d in data:
    s.add(d['business_id'])

with open('../raw.nosync/business.txt', 'w') as f:
    for a in s:
        f.write(a + '\n')
