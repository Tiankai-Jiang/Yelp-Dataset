import json

userWithInfo = set([line[:-1] for line in open('../raw.nosync/usersWithInfo.txt', 'r')])

for i in range(1, 8):
    data = [json.loads(line) for line in open('../raw.nosync/yelp_dataset/user/user' + str(i) + '.json', 'r')]
    for d in data:
        tmp = set(d['friends'].split(', ')) & userWithInfo
        if(len(tmp) == 0):
            d['friends'] = ""
        else:
            string = ""
            for t in tmp:
                string = string + t + ", "
            string = string[:-2]
            d['friends'] = string

    with open('../raw.nosync/cleanUsers/user' + str(i) + '.json', 'w') as f:
        for d in data:
            json.dump(d, f)
            f.write("\n")   
       