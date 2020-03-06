import json

business = set([json.loads(line)['business_id'] for line in open('../raw.nosync/yelp_dataset/photo.json', 'r')])

with open('../raw.nosync/businessInPhoto.txt', 'w') as f:
    for a in business:
        f.write(a + '\n')