business = set([line for line in open('../raw.nosync/business.txt', 'r')])
businessInReviews = set([line for line in open('../raw.nosync/businessInReviews.txt', 'r')])
businessInCheckin = set([line for line in open('../raw.nosync/businessInCheckin.txt', 'r')])
businessInTip = set([line for line in open('../raw.nosync/businessInTips.txt', 'r')])
businessInPhoto = set([line for line in open('../raw.nosync/businessInPhoto.txt', 'r')])

print(len(business - businessInReviews))
print(businessInReviews - business)
print(len(business - businessInCheckin))
print(businessInCheckin - business)
print(len(business - businessInTip))
print(businessInTip - business)
print(len(business - businessInPhoto))
print(businessInPhoto - business)

# The result shows that all business_ids in reviews, checkin, tip and photo are in the business table