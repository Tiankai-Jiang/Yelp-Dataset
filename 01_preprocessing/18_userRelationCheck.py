import json

for i in range(1, 8):
    data = [json.loads(line) for line in open('../raw.nosync/cleanUsers/user' + str(i) + '.json', 'r')]
    for d in data:
        if d['user_id'] == 'EL9Ugx4jO1vmawyL91NOsA':
            if 'zzpgpo54-_P-4rzzBtOuLQ' in d["friends"].split(', '):
                print('True') # the relationship are mutual
            else:
                print('False')