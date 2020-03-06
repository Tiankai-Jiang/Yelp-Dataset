import json

maxLen = 0

data = [json.loads(line) for line in open('../raw.nosync/yelp_dataset/business.json', 'r')]
for d in data:
    if len(d['postal_code']) > maxLen:
        maxLen = len(d['postal_code'])

print(maxLen) # 64