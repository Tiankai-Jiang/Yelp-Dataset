import json, mysql.connector, string, random

def getRandom():
    return '"' + ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(22)) + '"'

conn = mysql.connector.connect(user='root', password='password', host='127.0.0.1')
cur = conn.cursor()
cur.execute("use yelp;")
cur.execute("begin;")

l = ['user_id', 'business_id', 'text', 'date', 'compliment_count']
data = [json.loads(line) for line in open('../raw.nosync/yelp_dataset/tip.json', 'r')]

for d in data:
    s = "insert into Tips(tip_id, user_id, business_id, content, tip_date, compliment_count) values (" + getRandom() + ", "
    for attr in l:
        if isinstance(d[attr], str):
            if '\\' in d[attr]:
                d[attr] = d[attr].replace('\\', '\\\\')
            if '"' in d[attr]:
                d[attr] = d[attr].replace('"', '\\"')
            s = s + '"' + d[attr] + '", '
        else:
            s = s + str(d[attr]) + ', '
    s = s[:-2] + ');'
    # print(s)
    cur.execute(s)
cur.execute("commit;")