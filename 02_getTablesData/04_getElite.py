import json

e = []
for i in range(1,8):
    data = [json.loads(line) for line in open('../raw.nosync/cleanUsers/user' + str(i) + '.json', 'r')]
    for d in data:
        if d['elite']:
            tmp = d['elite'].split(',')
            for year in tmp:
                e.append((d['user_id'], year))

with open('../raw.nosync/elite.txt', 'w') as f:
    for i in e:
        f.write(i[0] + ' ' + str(i[1]) + '\n')