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
    print('1) Star/Unstar a review\n2) New post\n3) Follow/Unfollow a user\n4) Follow/Unfollow a business')
    print('5) Get new posts by people you followed\n6) Get new posts by business you followed')
    print('7) Get all your posts\n8) Get all following users\n9) Get all following business\n10) Delete your review\n11) Exit')
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
        resp = requests.get(url + 'uposts?u=' + user_id)
    elif opt == '6':
        resp = requests.get(url + 'bposts?u=' + user_id)
    elif opt == '7':
        resp = requests.get(url + 'mposts?u=' + user_id)
    elif opt == '8':
        resp = requests.get(url + 'followulist?u=' + user_id)
    elif opt == '9':
        resp = requests.get(url + 'followblist?u=' + user_id)
    elif opt == '10':
        resp = requests.get(url + 'mposts?u=' + user_id)
        m = resp.json()['message']
        for count, ele in enumerate(m, 1):
            print(str(count) + '.\nbusiness name: ' + ele['business_name'] + '\nreview snippet: ' + ele['content'][:50] + '...\nreview date: ' + ele['review_date'] + '\n\n')
        print('Which review you want to delete?')
        try:
            resp = requests.post(url + 'dpost', json = {'user_id': user_id, 'review_id': m[int(sys.stdin.readline()[:-1])-1]['review_id']})
        except:
            print('Error')
    else:
        break
    print(json.dumps(resp.json(), indent=1))