import json

maxLen = 0
for i in range(1, 8):
    data = [json.loads(line) for line in open('../raw.nosync/cleanUsers/user' + str(i) + '.json', 'r')]
    for d in data:
        if len(d['name']) > maxLen:
            maxLen = len(d['name'])

print(maxLen) # 32