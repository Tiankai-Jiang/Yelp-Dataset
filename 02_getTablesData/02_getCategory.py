import json

category = set()

data = [json.loads(line) for line in open('../raw.nosync/yelp_dataset/business.json', 'r')]
for d in data:
    if d['categories']:
        for a in d['categories'].split(', '):
            category.add(a)

dic = {}

with open('../raw.nosync/categories.txt', 'w') as f:
    for i, j in enumerate(category,1):
        dic[j] = i
        f.write(str(i) + ', ' + j + '\n')

juncTable = set()
for d in data:
    if d['categories']:
        for a in d['categories'].split(', '):
            juncTable.add((d['business_id'], dic[a]))

res = sorted(list(juncTable))
with open('../raw.nosync/categoryJunc.txt', 'w') as f:
    for i in res:
        f.write(i[0] + ' ' + str(i[1]) + '\n')