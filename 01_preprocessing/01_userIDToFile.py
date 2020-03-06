import json

users = set()
friends = set()

for i in range(1, 8):
    data = [json.loads(line) for line in open('../raw.nosync/yelp_dataset/user/user' + str(i) + '.json', 'r')]
    for d in data:
        users.add(d['user_id'])
        if d['friends'] is not None:
            friends |= set(d['friends'].split(', '))


# print(len(users))
# print(len(friends))
# print(len(friends - users))
without = friends - users

with open('../raw.nosync/usersWithInfo.txt', 'w') as f:
    for a in users:
        f.write(a + '\n')

with open('../raw.nosync/usersAll.txt', 'w') as f:
    for a in friends:
        f.write(a + '\n')

with open('../raw.nosync/usersWithoutInfo.txt', 'w') as f:
    for a in without:
        f.write(a + '\n')