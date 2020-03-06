import json

attr = ['GoodForMeal', 'HairSpecializesIn', 'DogsAllowed', 'Ambience', 'CoatCheck', 'Music', 'BikeParking', 'GoodForDancing', 'Open24Hours', 'RestaurantsTakeOut', 'RestaurantsReservations', 'AgesAllowed', 'Smoking', 'WiFi', 'AcceptsInsurance', 'BYOB', 'DietaryRestrictions', 'RestaurantsAttire', 'RestaurantsPriceRange2', 'WheelchairAccessible', 'Alcohol', 'BYOBCorkage', 'OutdoorSeating', 'RestaurantsDelivery', 'HasTV', 'RestaurantsCounterService', 'ByAppointmentOnly', 'Corkage', 'RestaurantsGoodForGroups', 'BestNights', 'HappyHour', 'RestaurantsTableService', 'GoodForKids', 'BusinessParking', 'BusinessAcceptsCreditCards', 'NoiseLevel', 'BusinessAcceptsBitcoin', 'DriveThru', 'Caters']
attrDict = {}
for i in attr:
    attrDict[i] = set()

data = [json.loads(line) for line in open('../raw.nosync/yelp_dataset/business.json', 'r')]

nested = ['GoodForMeal', 'HairSpecializesIn', 'Ambience', 'Music', 'DietaryRestrictions', 'BestNights', 'BusinessParking']
nestedAttr = {}
for i in nested:
    nestedAttr[i] = set()

for d in data:
    if d['attributes'] is not None:
        for k, v in d['attributes'].items():
            if v is not None and k in nested:
                newDict = eval(v)
                if newDict is not None: 
                    for k1, v1 in newDict.items():
                        nestedAttr[k].add(k1)

with open('../raw.nosync/nestedAttr.txt', 'w') as f:
    for k, v in nestedAttr.items():
        f.write(k + ': ')
        for i in v:
            f.write(i + ' ')
        f.write('\n')

# with open('businessAttr.txt', 'w') as f:
#     for k, v in attrDict.items():
#         f.write(k + '\n')
#         f.write(str(v) + '\n\n')