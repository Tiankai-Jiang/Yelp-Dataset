import json

maxLen = 0

data = [json.loads(line) for line in open('../raw.nosync/yelp_dataset/photo.json', 'r')]
for d in data:
    if len(d['caption']) > maxLen:
        maxLen = len(d['caption'])

print(maxLen) # 64