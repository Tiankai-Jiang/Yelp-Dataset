import json, mysql.connector

conn = mysql.connector.connect(user='root', password='password', host='127.0.0.1')
cur = conn.cursor()
cur.execute("use yelp;")
cur.execute("begin;")

with open('../raw.nosync/attributes.txt', 'r') as f:
    for line in f:
        u = line.split()
        s = 'insert into Attributes (attribute_id, attribute_name) values (' + u[0] + ', "' + u[1] + '");'
        cur.execute(s)
cur.execute("commit;")