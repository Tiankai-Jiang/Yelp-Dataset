import sys, requests, json

url = 'http://127.0.0.1:5000/yelp/'
user_id = ''
while(user_id==''):
    print('1) Login\n2) Register')
    opt = sys.stdin.readline()[:-1]
    if opt == '1':
        print('Enter user_id:')
        resp = requests.post(url + 'login', json = {'user_id': sys.stdin.readline()[:-1]})
        if resp.json()['status'] == 0: user_id = resp.json()['message']
        print(json.dumps(resp.json(), indent=1))
    elif opt == '2':
        print('Enter new username:')
        resp = requests.post(url + 'newuser', json = {'username': sys.stdin.readline()[:-1]})
        if resp.json()['status'] == 0: user_id = resp.json()['message']
        print(json.dumps(resp.json(), indent=1))

while(True):
    print('1) Star/Unstar a review\n2) New post\n3) Follow/Unfollow a user\n4) Follow/Unfollow a business\n5) Get new posts by people you followed\n6) Get new posts by business you followed\n7) Exit')
    opt = sys.stdin.readline()[:-1]
    if opt == '1':
        print('Enter review_id:')
        resp = requests.post(url + 'star', json = {'user_id': user_id, 'review_id': sys.stdin.readline()[:-1]})
    elif opt == '2':
        print('Enter business_id:')
        bid = sys.stdin.readline()[:-1]
        print('Enter review content:')
        resp = requests.post(url + 'newpost', json = {'user_id': user_id, 'business_id': bid, 'content': sys.stdin.readline()[:-1]})
    elif opt == '3':
        print('Enter the user_id you want to follow/unfollow:')
        resp = requests.post(url + 'followu', json = {'user_id1': user_id, 'user_id2': sys.stdin.readline()[:-1]})
    elif opt == '4':
        print('Enter the business_id you want to follow/unfollow:')
        resp = requests.post(url + 'followb', json = {'user_id': user_id, 'business_id': sys.stdin.readline()[:-1]})
    elif opt == '5':
        resp = requests.get(url + 'ffposts?u=' + user_id)
    elif opt == '6':
        resp = requests.get(url + 'fbposts?u=' + user_id)
    else:
        break
    print(json.dumps(resp.json(), indent=1))