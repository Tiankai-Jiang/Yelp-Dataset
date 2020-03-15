import sys, requests, json, os
from prettytable import PrettyTable, ALL
from textwrap import fill

url = 'http://127.0.0.1:5000/yelp/'
user_id = ''
while(user_id==''):
    print('1) Login\n2) Register\n3) Exit')
    opt = sys.stdin.readline()[:-1]
    table = PrettyTable(field_names=['Message'], align='l', hrules=ALL)
    if opt == '1':
        print('Enter user_id:')
        resp = requests.post(url + 'login', json = {'user_id': sys.stdin.readline()[:-1]})
    elif opt == '2':
        print('Enter new username:')
        resp = requests.post(url + 'newuser', json = {'username': sys.stdin.readline()[:-1]})
    else: sys.exit()
    print("\033c", end="")
    if resp.json()['status'] == 0: user_id = resp.json()['message']
    table.add_row(['Success'] if resp.json()['status'] == 0 else [resp.json()['message']])
    print(table)
    print()

while(True):
    print('1) Star/Unstar a review\n2) Get all starred reviews\n3) New review\n4) Follow/Unfollow a user\n5) Follow/Unfollow a business')
    print('6) Get new posts by people you followed\n7) Get new posts by business you followed')
    print('8) Get all your posts\n9) Get all following users\n10) Get all following business\n11) Delete your review')
    print('12) Change username\n13) Who am I\n14) Clean review history\n15) Exit')
    opt = sys.stdin.readline()[:-1]
    if opt == '1':
        print('Enter review_id:')
        resp = requests.post(url + 'star', json = {'user_id': user_id, 'review_id': sys.stdin.readline()[:-1]})
    elif opt == '2': resp = requests.get(url + 'stars?u=' + user_id)
    elif opt == '3':
        print('Enter business_id:')
        bid = sys.stdin.readline()[:-1]
        print('Enter review content:')
        resp = requests.post(url + 'newpost', json = {'user_id': user_id, 'business_id': bid, 'content': sys.stdin.readline()[:-1]})
    elif opt == '4':
        print('Enter the user_id you want to follow/unfollow:')
        resp = requests.post(url + 'followu', json = {'user_id1': user_id, 'user_id2': sys.stdin.readline()[:-1]})
    elif opt == '5':
        print('Enter the business_id you want to follow/unfollow:')
        resp = requests.post(url + 'followb', json = {'user_id': user_id, 'business_id': sys.stdin.readline()[:-1]})
    elif opt == '6':
        print('Number of reviews you want(or press Enter to retrieve all)')
        resp = requests.get(url + 'uposts?u=' + user_id + '&l=' + sys.stdin.readline()[:-1])
    elif opt == '7':
        print('Number of reviews you want(or press Enter to retrieve all)')
        resp = requests.get(url + 'bposts?u=' + user_id + '&l=' + sys.stdin.readline()[:-1])
    elif opt == '8': resp = requests.get(url + 'mposts?u=' + user_id)
    elif opt == '9': resp = requests.get(url + 'followulist?u=' + user_id)
    elif opt == '10': resp = requests.get(url + 'followblist?u=' + user_id)
    elif opt == '11':
        resp = requests.get(url + 'mposts?u=' + user_id)
        m = resp.json()['message']
        table = PrettyTable(field_names=['No', 'business name', 'review snippet', 'review date'], align='l', hrules=ALL)
        [table.add_row([str(count), ele['business_name'], ele['content'][:50] + '...', fill(ele['review_date'], width=20)]) for count, ele in enumerate(m, 1)]
        print(table)
        print('\nWhich review you want to delete?')
        try:
            resp = requests.post(url + 'dpost', json = {'user_id': user_id, 'review_id': m[int(sys.stdin.readline()[:-1])-1]['review_id']})
        except:
            resp = requests.models.Response()
            resp._content = b'{"status" : 1, "message": "Invalid No"}'
    elif opt == '12':
        print('Enter new username:')
        resp = requests.post(url + 'cn', json = {'user_id': user_id, 'username': sys.stdin.readline()[:-1]})
    elif opt == '13': resp = requests.get(url + 'whoami?u=' + user_id)
    elif opt == '14': resp = requests.post(url + 'reset', json = {'user_id': user_id})
    else: sys.exit()
    # print(json.dumps(resp.json(), indent = 1))
    r = resp.json()['message']
    print("\033c", end="")
    if isinstance(r, list):
        if r:
            table = PrettyTable(field_names=[*r[0]], align='l', hrules=ALL)
            [table.add_row([fill(str(y), width=50) for y in list(x.values())]) for x in r]
            print(table.get_string(fields=[x for x in [*r[0]] if x not in {'review_id', 'review_date'}]))
            print(str(len(r)) + ' rows in set')
        else:
            table = PrettyTable(field_names=['Message'], align='l', hrules=ALL)
            table.add_row(['Empty set'])
            print(table)
    else:
        table = PrettyTable(field_names=['Message'], align='l', hrules=ALL)
        table.add_row([fill(r, width=50)])
        print(table)
    print()