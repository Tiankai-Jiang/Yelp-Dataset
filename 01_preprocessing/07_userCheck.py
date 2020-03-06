users = set([line for line in open('../raw.nosync/usersWithInfo.txt', 'r')])
usersInReview = set([line for line in open('../raw.nosync/usersInReviews.txt', 'r')])
usersInTips = set([line for line in open('../raw.nosync/usersInTips.txt', 'r')])

print(users - usersInReview)
print(usersInReview - users)
print(len(users - usersInTips))
print(usersInTips - users)
# result shows that all user_ids in reviews and tips are in the user table