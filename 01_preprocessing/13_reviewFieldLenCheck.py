import json

maxLen = 0
for i in range(1, 15):
    data = [json.loads(line) for line in open('../raw.nosync/yelp_dataset/review/review' + str(i) + '.json', 'r')]
    for d in data:
        if len(d['text']) > maxLen:
            maxLen = len(d['text'])

print(maxLen) # 32