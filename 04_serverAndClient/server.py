import flask, mysql.connector, random, string
from flask import request, jsonify
from datetime import datetime

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def getRandom():
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits + '-_') for _ in range(22)) 

@app.errorhandler(404)
def not_found(e):
    return jsonify({"status": 1, "message": "404"}), 404

# New user
@app.route('/yelp/newuser', methods=['POST'])
def newuser():
    try:
        uid = getRandom()
        cur.execute('begin;')
        cur.execute('INSERT INTO Users(user_id, name, yelping_since) VALUES (%s, %s, %s);', (uid, request.get_json()['username'], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        cur.execute('commit;')
        return jsonify({"status": 0, "message": uid})
    except Exception as e:
        return jsonify({"status": 1, "message": str(e)})

# User login
@app.route('/yelp/login', methods=['POST'])
def login():
    try:
        cur.execute('SELECT user_id FROM Users WHERE user_id=%s;', (request.get_json()['user_id'], ))
        uid = cur.fetchone()
        return jsonify({"status": 0, "message": uid['user_id']}) if cur.rowcount else jsonify({"status": 1, "message": "No such user"})
    except Exception as e:
        return jsonify({"status": 1, "message": str(e)})

# A user gives a star to a review
@app.route('/yelp/star', methods=['POST'])
def star():
    data = request.get_json()
    u = data['user_id']
    r = data['review_id']
    try:
        cur.execute('SELECT count(*) as c FROM UserStars WHERE user_id=%s AND review_id=%s ;', (u, r))
        if cur.fetchone()['c'] > 0:
            cur.execute('begin;')
            cur.execute('UPDATE Reviews SET stars = stars - 1 WHERE review_id=%s;', (r,))
            cur.execute('DELETE FROM UserStars WHERE user_id=%s AND review_id=%s;', (u, r))
            cur.execute('commit;')
            return jsonify({"status": 0, "message": "Unstarred"})
        else:
            cur.execute('begin;')
            cur.execute('UPDATE Reviews SET stars = stars + 1 WHERE review_id=%s;', (r,))
            cur.execute('INSERT INTO UserStars(user_id, review_id) VALUES (%s, %s);', (u, r))
            cur.execute('commit;')
            return jsonify({"status": 0, "message": "Starred"})
    except Exception as e:
        cur.execute('rollback;')
        return jsonify({"status": 1, "message": str(e)})

# Initiate a new post
@app.route('/yelp/newpost', methods=['POST'])
def newpost():
    data = request.get_json()
    try:
        cur.execute('begin;')
        rid = getRandom()
        cur.execute('INSERT INTO Reviews(review_id, user_id, business_id, content, review_date) VALUES ("' + rid + '", %s, %s, %s, NOW());', (data['user_id'], data['business_id'], data['content']))
        cur.execute('commit;')
        return jsonify({"status": 0, "message": rid})
    except Exception as e:
        cur.execute('rollback;')
        return jsonify({"status": 1, "message": str(e)})

# A user follows another user
@app.route('/yelp/followu', methods=['POST'])
def followu():
    data = request.get_json()
    u = data['user_id1']
    f = data['user_id2']
    if u == f:
        return jsonify({"status": 1, "message": "You cannot follow yourself!"})
    try:
        cur.execute('SELECT count(*) as c FROM UserFollowers WHERE user_id1=%s AND user_id2=%s ;', (u, f))
        if cur.fetchone()['c'] > 0:
            cur.execute('begin;')
            cur.execute('DELETE FROM UserFollowers WHERE user_id1=%s AND user_id2=%s;', (u, f))
            cur.execute('commit;')
            return jsonify({"status": 0, "message": "Unfollowed"})
        else:
            cur.execute('begin;')
            cur.execute('INSERT INTO UserFollowers(user_id1, user_id2) VALUES (%s, %s);', (u, f))
            cur.execute('commit;')
            return jsonify({"status": 0, "message": "Followed"})
    except Exception as e:
        cur.execute('rollback;')
        return jsonify({"status": 1, "message": str(e)})

# A user follows a business
@app.route('/yelp/followb', methods=['POST'])
def followb():
    data = request.get_json()
    u = data['user_id']
    b = data['business_id']
    try:
        cur.execute('SELECT count(*) as c FROM BusinessFollowers WHERE user_id=%s AND business_id=%s ;', (u, b))
        if cur.fetchone()['c'] > 0:
            cur.execute('begin;')
            cur.execute('DELETE FROM BusinessFollowers WHERE user_id=%s AND business_id=%s;', (u, b))
            cur.execute('commit;')
            return jsonify({"status": 0, "message": "Unfollowed"})
        else:           
            cur.execute('begin;')
            cur.execute('INSERT INTO BusinessFollowers(user_id, business_id) VALUES (%s, %s);', (u, b))
            cur.execute('commit;')
            return jsonify({"status": 0, "message": "Followed"})
    except Exception as e:
        cur.execute('rollback;')
        return jsonify({"status": 1, "message": str(e)})

# Fetch new posts by the followed people of a user
@app.route('/yelp/uposts', methods=['GET'])
def uposts():
    u = request.args.get('u')
    l = request.args.get('l')
    if u:
        try:
            cur.execute('begin;')
            cur.execute(''' SELECT Reviews.review_id as review_id, Users.name as reviewer, Business.name as business_name, content, review_date
                            FROM UserFollowers INNER JOIN Reviews ON Reviews.user_id = UserFollowers.user_id2
                            LEFT JOIN ReadReviews USING(review_id) INNER JOIN Users ON Reviews.user_id = Users.user_id
                            INNER JOIN Business USING(business_id) WHERE ReadReviews.review_id IS NULL 
                            AND UserFollowers.user_id1=%s ORDER BY review_date LIMIT %s;''', (u, int(l) if l else 10000))
            res = cur.fetchall()
            for r in [x['review_id'] for x in res]:
                cur.execute('INSERT INTO ReadReviews(user_id, review_id) VALUES (%s, %s);', (u, r))
            cur.execute('commit;')
            return jsonify({"status": 0, "message": res})
        except Exception as e:
            cur.execute('rollback;')
            return jsonify({"status": 1, "message": str(e)})
    else:
        return not_found(404)

# Fetch new posts by the followed business of a user
@app.route('/yelp/bposts', methods=['GET'])
def bposts():
    u = request.args.get('u')
    l = request.args.get('l')
    if u:
        try:
            cur.execute('begin;')
            cur.execute(''' SELECT Reviews.review_id as review_id, Users.name as reviewer, Business.name as business_name, content, review_date
                            FROM BusinessFollowers INNER JOIN Reviews USING(business_id)
                            LEFT JOIN ReadReviews USING(review_id) INNER JOIN Business USING(business_id)
                            INNER JOIN Users ON Reviews.user_id = Users.user_id
                            WHERE ReadReviews.review_id IS NULL AND BusinessFollowers.user_id=%s
                            ORDER BY review_date desc LIMIT %s;''', (u, int(l) if l else 10000))
            res = cur.fetchall()
            for r in [x['review_id'] for x in res]:
                cur.execute('INSERT INTO ReadReviews(user_id, review_id) VALUES (%s, %s);', (u, r))
            cur.execute('commit;')
            return jsonify({"status": 0, "message": res})
        except Exception as e:
            cur.execute('rollback;')
            return jsonify({"status": 1, "message": str(e)})
    else:
        return not_found(404)

# Fetch all my posts
@app.route('/yelp/mposts', methods=['GET'])
def mposts():
    u = request.args.get('u')
    if u:
        try:
            cur.execute('''SELECT review_id, name AS business_name, Reviews.stars AS stars, useful, funny, cool, content, review_date
                FROM Reviews INNER JOIN Business USING(business_id) where user_id =%s;''', (u,))
            return jsonify({"status": 0, "message": cur.fetchall()})
        except Exception as e:
            return jsonify({"status": 1, "message": str(e)})
    else:
        return not_found(404)

@app.route('/yelp/followulist', methods=['GET'])
def followulist():
    u = request.args.get('u')
    if u:
        try:
            cur.execute('SELECT user_id2 as user_id from UserFollowers where user_id1 =%s;', (u,))
            return jsonify({"status": 0, "message": cur.fetchall()})
        except Exception as e:
            return jsonify({"status": 1, "message": str(e)})
    else:
        return not_found(404)

@app.route('/yelp/followblist', methods=['GET'])
def followblist():
    u = request.args.get('u')
    if u:
        try:
            cur.execute('SELECT business_id from BusinessFollowers where user_id =%s;', (u,))
            return jsonify({"status": 0, "message": cur.fetchall()})
        except Exception as e:
            return jsonify({"status": 1, "message": str(e)})
    else:
        return not_found(404)

# Delete my review
@app.route('/yelp/dpost', methods=['POST'])
def dpost():
    data = request.get_json()
    u = data['user_id']
    r = data['review_id']
    try:
        cur.execute('begin;')
        cur.execute('DELETE from Reviews where review_id =%s AND user_id = %s', (r, u))
        cur.execute('commit;')
        return jsonify({"status": 0, "message": "Success"})
    except Exception as e:
        cur.execute('rollback;')
        return jsonify({"status": 1, "message": str(e)})

# change username
@app.route('/yelp/cn', methods=['POST'])
def cn():
    data = request.get_json()
    try:
        cur.execute('begin;')
        cur.execute('UPDATE Users SET name =%s where user_id =%s', (data['username'], data['user_id']))
        cur.execute('commit;')
        return jsonify({"status": 0, "message": "Success"})
    except Exception as e:
        cur.execute('rollback;')
        return jsonify({"status": 1, "message": str(e)})

# get user info
@app.route('/yelp/whoami', methods=['GET'])
def whoami():
    u = request.args.get('u')
    if u:
        try:
            cur.execute('SELECT * from Users where user_id =%s;', (u,))
            return jsonify({"status": 0, "message": cur.fetchall()})
        except Exception as e:
            return jsonify({"status": 1, "message": str(e)})
    else:
        return not_found(404)

# get new posts with pages
conn = mysql.connector.connect(user='root', password='password', host='127.0.0.1')
cur = conn.cursor(dictionary=True)
cur.execute("use yelp;")
app.run()