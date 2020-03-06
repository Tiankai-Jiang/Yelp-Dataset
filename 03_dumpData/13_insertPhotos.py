import json, mysql.connector

conn = mysql.connector.connect(user='root', password='password', host='127.0.0.1')
cur = conn.cursor()
cur.execute("use yelp;")
cur.execute("begin;")

l = ['photo_id', 'business_id', 'label']
data = [json.loads(line) for line in open('../raw.nosync/yelp_dataset/photo.json', 'r')]
for d in data:
    s = "insert into Photos(photo_id, business_id, label, caption) values ("
    for attr in l:
        if isinstance(d[attr], str):
            s = s + '"' + d[attr] + '", '
        else:
            s = s + str(d[attr]) + ', '
    if d['caption']:
        if '\\' in d['caption']:
            d['caption'] = d['caption'].replace('\\', '\\\\')
        if '"' in d['caption']:
            d['caption'] = d['caption'].replace('"', '\\"')
        s = s + '"' + d['caption'] + '");'
    else:
        s = s + 'NULL);'
    # print(s)
    cur.execute(s)
cur.execute("commit;")


