import flask, mysql.connector, random, string
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def getRandom():
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits + '-_') for _ in range(22)) 

@app.errorhandler(404)
def not_found(e):
    return jsonify('{"status": 1, "message": "404"}'), 404

# A user gives a star to a review
@app.route('/yelp/login', methods=['GET'])
def login():
    u = request.args.get('u')

    conn = mysql.connector.connect(user='root', password='password', host='127.0.0.1')
    cur = conn.cursor(dictionary=True)
    cur.execute("use yelp;")

    if u:
        try:
            cur.execute('SELECT count(*) as c FROM Users WHERE user_id=%s;', (u, ))
            if cur.fetchone()['c'] > 0:
                cur.close()
                conn.close()
                return jsonify('{"status": 0, "message": "Success"}')
            else:
                cur.close()
                conn.close()
                return jsonify('{"status": 1, "message": "No such user"}')
        except Exception as e:
            cur.close()
            conn.close()
            return jsonify('{"status": 1, "message": "'+ str(e) + '"}')
    else:
        return not_found(404)

# A user gives a star to a review
@app.route('/yelp/star', methods=['GET'])
def star():
    query_parameters = request.args
    u = query_parameters.get('u')
    r = query_parameters.get('r')

    conn = mysql.connector.connect(user='root', password='password', host='127.0.0.1')
    cur = conn.cursor(dictionary=True)
    cur.execute("use yelp;")

    if u and r:
        try:
            cur.execute('SELECT count(*) as c FROM UserStars WHERE user_id=%s AND review_id=%s ;', (u, r))
            if cur.fetchone()['c'] > 0:
                cur.execute('begin;')
                cur.execute('UPDATE Reviews SET stars = stars - 1 WHERE review_id=%s;', (r,))
                cur.execute('DELETE FROM UserStars WHERE user_id=%s AND review_id=%s;', (u, r))
                cur.execute('commit;')
                cur.close()
                conn.close()
                return jsonify('{"status": 0, "message": "Unstarred"}')
            else:
                cur.execute('begin;')
                cur.execute('UPDATE Reviews SET stars = stars + 1 WHERE review_id=%s;', (r,))
                cur.execute('INSERT INTO UserStars(user_id, review_id) VALUES (%s, %s);', (u, r))
                cur.execute('commit;')
                cur.close()
                conn.close()
                return jsonify('{"status": 0, "message": "Starred"}')
        except Exception as e:
            cur.execute('rollback;')
            cur.close()
            conn.close()
            return jsonify('{"status": 1, "message": "'+ str(e) + '"}')
    else:
        return not_found(404)

# Fetch all new posts by the followed people of a user
@app.route('/yelp/ffposts', methods=['GET'])
def ffposts():
    query_parameters = request.args
    u = query_parameters.get('u')

    conn = mysql.connector.connect(user='root', password='password', host='127.0.0.1')
    cur = conn.cursor(dictionary=True)
    cur.execute("use yelp;")

    query = ''' SELECT Reviews.review_id as review_id, Reviews.user_id as reviewer, business_id, content FROM UserFollowers
    INNER JOIN Reviews ON Reviews.user_id = UserFollowers.user_id2
    LEFT JOIN ReadReviews ON Reviews.review_id = ReadReviews.review_id
    WHERE ReadReviews.review_id IS NULL AND UserFollowers.user_id1=%s;'''

    if u:
        try:
            cur.execute('begin;')
            cur.execute(query, (u,))
            res = cur.fetchall()
            for r in [x['review_id'] for x in res]:
                cur.execute('INSERT INTO ReadReviews(user_id, review_id) VALUES (%s, %s);', (u, r))
            cur.execute('commit;')
            cur.close()
            conn.close()
            resDict = {"status": 0}
            resDict["message"] = res
            return jsonify(resDict)
        except Exception as e:
            cur.execute('rollback;')
            cur.close()
            conn.close()
            return jsonify('{"status": 1, "message": "'+ str(e) + '"}')
    else:
        return not_found(404)

# Fetch all new posts by the followed business of a user
@app.route('/yelp/fbposts', methods=['GET'])
def fbposts():
    query_parameters = request.args
    u = query_parameters.get('u')

    conn = mysql.connector.connect(user='root', password='password', host='127.0.0.1')
    cur = conn.cursor(dictionary=True)
    cur.execute("use yelp;")

    query = ''' SELECT Reviews.review_id as review_id, Reviews.user_id as reviewer, Reviews.business_id as business_id, content FROM BusinessFollowers
    INNER JOIN Reviews ON Reviews.business_id = BusinessFollowers.business_id
    LEFT JOIN ReadReviews ON Reviews.review_id = ReadReviews.review_id
    WHERE ReadReviews.review_id IS NULL AND BusinessFollowers.user_id=%s;'''

    if u:
        try:
            cur.execute('begin;')
            cur.execute(query, (u,))
            res = cur.fetchall()
            for r in [x['review_id'] for x in res]:
                cur.execute('INSERT INTO ReadReviews(user_id, review_id) VALUES (%s, %s);', (u, r))
            cur.execute('commit;')
            cur.close()
            conn.close()
            resDict = {"status": 0}
            resDict["message"] = res
            return jsonify(resDict)
        except Exception as e:
            cur.execute('rollback;')
            cur.close()
            conn.close()
            return jsonify('{"status": 1, "message": "'+ str(e) + '"}')
    else:
        return not_found(404)

# Initiate a new post
@app.route('/yelp/newpost', methods=['GET'])
def newpost():
    query_parameters = request.args
    u = query_parameters.get('u')
    b = query_parameters.get('b')
    r = query_parameters.get('r')

    conn = mysql.connector.connect(user='root', password='password', host='127.0.0.1')
    cur = conn.cursor(dictionary=True)
    cur.execute("use yelp;")

    if u and b and r:
        try:
            cur.execute('begin;')
            rid = getRandom()
            # + and other special characters are required to be handled in advance.
            cur.execute('INSERT INTO Reviews(review_id, user_id, business_id, content, review_date) VALUES ("' + rid + '", %s, %s, %s, NOW());', (u, b, r))
            print(rid)
            cur.execute('commit;')
            cur.close()
            conn.close()
            return jsonify('{"status": 0, "message": "Success"}')
        except Exception as e:
            cur.execute('rollback;')
            cur.close()
            conn.close()
            return jsonify('{"status": 1, "message": "'+ str(e) + '"}')
    else:
        return not_found(404)

# A user follows another user
@app.route('/yelp/followu', methods=['GET'])
def followu():
    query_parameters = request.args
    u = query_parameters.get('u')
    f = query_parameters.get('f')

    conn = mysql.connector.connect(user='root', password='password', host='127.0.0.1')
    cur = conn.cursor(dictionary=True)
    cur.execute("use yelp;")

    if u and f:
        if u == f:
            cur.close()
            conn.close()
            return jsonify('{"status": 1, "message": "You cannot follow yourself!"}')
        try:
            cur.execute('begin;')
            cur.execute('INSERT INTO UserFollowers(user_id1, user_id2) VALUES (%s, %s);', (u, f))
            cur.execute('commit;')
            cur.close()
            conn.close()
            return jsonify('{"status": 0, "message": "Success"}')
        except Exception as e:
            cur.execute('rollback;')
            cur.close()
            conn.close()
            return jsonify('{"status": 1, "message": "'+ str(e) + '"}')
    else:
        return not_found(404)

# A user follows a business
@app.route('/yelp/followb', methods=['GET'])
def followb():
    query_parameters = request.args
    u = query_parameters.get('u')
    b = query_parameters.get('b')

    conn = mysql.connector.connect(user='root', password='password', host='127.0.0.1')
    cur = conn.cursor(dictionary=True)
    cur.execute("use yelp;")

    if u and b:
        try:
            cur.execute('begin;')
            cur.execute('INSERT INTO BusinessFollowers(user_id, business_id) VALUES (%s, %s);', (u, b))
            cur.execute('commit;')
            cur.close()
            conn.close()
            return jsonify('{"status": 0, "message": "Success"}')
        except Exception as e:
            cur.execute('rollback;')
            cur.close()
            conn.close()
            return jsonify('{"status": 1, "message": "'+ str(e) + '"}')
    else:
        return not_found(404)

app.run()

