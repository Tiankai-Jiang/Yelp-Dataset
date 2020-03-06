import json

attributes = ['GoodForMeal', 'HairSpecializesIn', 'DogsAllowed', 'Ambience', 'CoatCheck', 'Music', 'BikeParking', 'GoodForDancing', 'Open24Hours', 'RestaurantsTakeOut', 'RestaurantsReservations', 'AgesAllowed', 'Smoking', 'WiFi', 'AcceptsInsurance', 'BYOB', 'DietaryRestrictions', 'RestaurantsAttire', 'RestaurantsPriceRange2', 'WheelchairAccessible', 'Alcohol', 'BYOBCorkage', 'OutdoorSeating', 'RestaurantsDelivery', 'HasTV', 'RestaurantsCounterService', 'ByAppointmentOnly', 'Corkage', 'RestaurantsGoodForGroups', 'BestNights', 'HappyHour', 'RestaurantsTableService', 'GoodForKids', 'BusinessParking', 'BusinessAcceptsCreditCards', 'NoiseLevel', 'BusinessAcceptsBitcoin', 'DriveThru', 'Caters']

dic = {}
with open('../raw.nosync/attributes.txt', 'w') as f:
    for i, j in enumerate(attributes, 1):
        dic[j] = i
        f.write(str(i) + ' ' + j + '\n')


attrs = []
data = [json.loads(line) for line in open('../raw.nosync/yelp_dataset/business.json', 'r')]
for d in data:
    if d['attributes'] is not None:
        for k, v in d['attributes'].items():
            if v is not None:
                attrs.append((d['business_id'], str(dic[k]), v))

maxlen = 0
with open('../raw.nosync/attributeJunc.txt', 'w') as f:
    for a in attrs:
        if len(a[2]) > maxlen:
            maxlen = len(a[2])
        f.write(a[0] + ' || ' + a[1] + ' || ' + a[2] + '\n')

print(maxlen) # 160