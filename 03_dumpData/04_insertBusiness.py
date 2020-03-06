import json, mysql.connector

conn = mysql.connector.connect(user='root', password='password', host='127.0.0.1')
cur = conn.cursor()
cur.execute("use yelp;")
cur.execute("begin;")

l = ['business_id', 'name', 'address', 'city', 'state', 'postal_code', 'latitude', 'longitude', 'stars', 'review_count', 'is_open']

data = [json.loads(line) for line in open('../raw.nosync/yelp_dataset/business.json', 'r')]
# data = [json.loads(line) for line in open('quote.json', 'r')]
for d in data:
    s = "insert into Business(business_id, name, address, city, state, postal_code, latitude, longitude, stars, review_count, is_open) values ("
    for attr in l:
        if isinstance(d[attr], str):
            if '"' in d[attr]:
                d[attr] = d[attr].replace('"', '\\"')
            s = s + '"' + d[attr] + '", '
        else:
            s = s + str(d[attr]) + ', '
    s = s[:-2] + ');'
    # print(s)
    cur.execute(s)
cur.execute("commit;")