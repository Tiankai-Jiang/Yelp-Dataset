import json, mysql.connector

conn = mysql.connector.connect(user='root', password='password', host='127.0.0.1')
cur = conn.cursor()
cur.execute("use yelp;")
cur.execute("begin;")

with open('../raw.nosync/hours.txt', 'r') as f:
    for line in f:
        u = line[:-1].split()
        s = 'insert into BusinessHours (business_id, day, hours) values ("' + u[0] + '", "' + u[1] + '", "' + u[2] + '");'
        # print(s)
        cur.execute(s)
cur.execute("commit;")