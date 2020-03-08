import sys, requests, json
url = 'http://127.0.0.1:5000/yelp/'
user_id = ''
while(user_id==''):
    print('Enter user_id to login:')
    uid = sys.stdin.readline()[:-1]
    resp = requests.get(url + 'login?u=' + uid)
    if json.loads(resp.json())['status'] == 0:
        user_id = uid
    print('\n' + resp.json() + '\n')

while(True):
    print('1) Star/Unstar a review\n2) New post\n3) Follow a user\n4) Follow a business\n5) Get new posts by people you followed\n6) Get new posts by business you followed\n7) Exit')
    opt = sys.stdin.readline()[:-1]
    if opt == '1':
        print('Enter review_id:')
        resp = requests.get(url + 'star?u=' + user_id + '&r=' + sys.stdin.readline()[:-1])
    elif opt == '2':
        print('Enter business_id:')
        bid = sys.stdin.readline()[:-1]
        print('Enter review content:')
        resp = requests.get(url + 'newpost?u=' + user_id + '&b=' + bid + '&r=' + sys.stdin.readline()[:-1])
    elif opt == '3':
        print('Enter the user_id you want to follow:')
        resp = requests.get(url + 'followu?u=' + user_id + '&f=' + sys.stdin.readline()[:-1])
    elif opt == '4':
        print('Enter the business_id you want to follow:')
        resp = requests.get(url + 'followb?u=' + user_id + '&b=' + sys.stdin.readline()[:-1])
    elif opt == '5':
        resp = requests.get(url + 'ffposts?u=' + user_id)
    elif opt == '6':
        resp = requests.get(url + 'fbposts?u=' + user_id)
    else:
        break
    print('\n' + str(resp.json()) + '\n')