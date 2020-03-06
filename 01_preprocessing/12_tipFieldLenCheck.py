import json

maxLen = 0

s = set()
data = [json.loads(line) for line in open('../raw.nosync/yelp_dataset/tip.json', 'r')]
for d in data:
    s.add((d['user_id'], d['business_id']))
    if len(d['text']) > maxLen:
        maxLen = len(d['text'])

print(maxLen) # 64
print(len(data))
print(len(s))