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
@app.route('/yelp/newuser', methods=['GET'])
def newuser():
    n = request.args.get('n')
    if n:
        try:
            uid = getRandom()
            cur.execute('begin;')
            cur.execute('INSERT INTO Users(user_id, name, yelping_since) VALUES (%s, %s, %s);', (uid, n, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            cur.execute('commit;')
            return jsonify({"status": 0, "message": uid})
        except Exception as e:
            return jsonify({"status": 1, "message": str(e)})
    else:
        return not_found(404)

# User login
@app.route('/yelp/login', methods=['GET'])
def login():
    u = request.args.get('u')
    if u:
        try:
            cur.execute('SELECT user_id FROM Users WHERE user_id=%s;', (u, ))
            uid = cur.fetchone()
            return jsonify({"status": 0, "message": uid['user_id']}) if cur.rowcount else jsonify({"status": 1, "message": "No such user"})
        except Exception as e:
            return jsonify({"status": 1, "message": str(e)})
    else:
        return not_found(404)

# A user gives a star to a review
@app.route('/yelp/star', methods=['GET'])
def star():
    u = request.args.get('u')
    r = request.args.get('r')
    if u and r:
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
    else:
        return not_found(404)

# Fetch all new posts by the followed people of a user
@app.route('/yelp/ffposts', methods=['GET'])
def ffposts():
    u = request.args.get('u')
    if u:
        try:
            cur.execute('begin;')
            cur.execute(''' SELECT Reviews.review_id as review_id, Reviews.user_id as reviewer, business_id, content 
                            FROM UserFollowers
                            INNER JOIN Reviews ON Reviews.user_id = UserFollowers.user_id2
                            LEFT JOIN ReadReviews ON Reviews.review_id = ReadReviews.review_id
                            WHERE ReadReviews.review_id IS NULL AND UserFollowers.user_id1=%s;''', (u,))
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

# Fetch all new posts by the followed business of a user
@app.route('/yelp/fbposts', methods=['GET'])
def fbposts():
    u = request.args.get('u')
    if u:
        try:
            cur.execute('begin;')
            cur.execute(''' SELECT Reviews.review_id as review_id, Reviews.user_id as reviewer, Reviews.business_id as business_id, content 
                            FROM BusinessFollowers
                            INNER JOIN Reviews ON Reviews.business_id = BusinessFollowers.business_id
                            LEFT JOIN ReadReviews ON Reviews.review_id = ReadReviews.review_id
                            WHERE ReadReviews.review_id IS NULL AND BusinessFollowers.user_id=%s;''', (u,))
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

# Initiate a new post
@app.route('/yelp/newpost', methods=['GET'])
def newpost():
    u = request.args.get('u')
    b = request.args.get('b')
    r = request.args.get('r')
    if u and b and r:
        try:
            cur.execute('begin;')
            rid = getRandom()
            cur.execute('INSERT INTO Reviews(review_id, user_id, business_id, content, review_date) VALUES ("' + rid + '", %s, %s, %s, NOW());', (u, b, r))
            cur.execute('commit;')
            return jsonify({"status": 0, "message": rid})
        except Exception as e:
            cur.execute('rollback;')
            return jsonify({"status": 1, "message": str(e)})
    else:
        return not_found(404)

# A user follows another user
@app.route('/yelp/followu', methods=['GET'])
def followu():
    u = request.args.get('u')
    f = request.args.get('f')
    if u and f:
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
    else:
        return not_found(404)

# A user follows a business
@app.route('/yelp/followb', methods=['GET'])
def followb():
    u = request.args.get('u')
    b = request.args.get('b')
    if u and b:
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
    else:
        return not_found(404)

conn = mysql.connector.connect(user='root', password='password', host='127.0.0.1')
cur = conn.cursor(dictionary=True)
cur.execute("use yelp;")
app.run()