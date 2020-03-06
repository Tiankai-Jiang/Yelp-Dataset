import json

friends = []
for i in range(1,8):
    data = [json.loads(line) for line in open('../raw.nosync/cleanUsers/user' + str(i) + '.json', 'r')]
    for d in data:
        if d['friends']:
            tmp = d['friends'].split(', ')
            for a in tmp:
                friends.append((d['user_id'], a))

with open('../raw.nosync/friends.txt', 'w') as f:
    for i in friends:
        f.write(i[0] + ' ' + i[1] + '\n')