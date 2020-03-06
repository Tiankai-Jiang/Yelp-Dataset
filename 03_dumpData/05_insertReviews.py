import json, mysql.connector

conn = mysql.connector.connect(user='root', password='password', host='127.0.0.1')
cur = conn.cursor()
cur.execute("use yelp;")

l = ['review_id', 'user_id', 'business_id', 'stars', 'useful', 'funny', 'cool', 'text', 'date']
for i in range(1, 15):
    data = [json.loads(line) for line in open('../raw.nosync/yelp_dataset/review/review' + str(i) + '.json', 'r')]
    cur.execute("begin;")
    for d in data:
        s = "insert into Reviews(review_id, user_id, business_id, stars, useful, funny, cool, content, review_date) values ("
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