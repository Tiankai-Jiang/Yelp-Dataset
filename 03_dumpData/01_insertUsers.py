import json, mysql.connector

conn = mysql.connector.connect(user='root', password='password', host='127.0.0.1')
cur = conn.cursor()
cur.execute("use yelp;")
cur.execute("begin;")

l = ['user_id', 'name', 'review_count', 'yelping_since', 'useful', 'funny', 'cool', 'fans', 'average_stars', 'compliment_hot', 'compliment_more', 'compliment_profile', 'compliment_cute', 'compliment_list', 'compliment_note', 'compliment_plain', 'compliment_cool', 'compliment_funny', 'compliment_writer', 'compliment_photos']
for i in range(1, 8):
    data = [json.loads(line) for line in open('../raw.nosync/cleanUsers/user' + str(i) + '.json', 'r')]
    for d in data:
        s = "insert into Users (user_id, name, review_count, yelping_since, useful, funny, cool, fans, average_stars, compliment_hot, compliment_more, compliment_profile, compliment_cute, compliment_list, compliment_note, compliment_plain, compliment_cool, compliment_funny, compliment_writer, compliment_photos) values ("
        for attr in l:
            if isinstance(d[attr], str):
                s = s + '"' + d[attr] + '", '
            else:
                s = s + str(d[attr]) + ', '
        s = s[:-2] + ');'
        cur.execute(s)
cur.execute("commit;")