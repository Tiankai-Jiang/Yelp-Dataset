import json

attr = ['GoodForMeal', 'HairSpecializesIn', 'DogsAllowed', 'Ambience', 'CoatCheck', 'Music', 'BikeParking', 'GoodForDancing', 'Open24Hours', 'RestaurantsTakeOut', 'RestaurantsReservations', 'AgesAllowed', 'Smoking', 'WiFi', 'AcceptsInsurance', 'BYOB', 'DietaryRestrictions', 'RestaurantsAttire', 'RestaurantsPriceRange2', 'WheelchairAccessible', 'Alcohol', 'BYOBCorkage', 'OutdoorSeating', 'RestaurantsDelivery', 'HasTV', 'RestaurantsCounterService', 'ByAppointmentOnly', 'Corkage', 'RestaurantsGoodForGroups', 'BestNights', 'HappyHour', 'RestaurantsTableService', 'GoodForKids', 'BusinessParking', 'BusinessAcceptsCreditCards', 'NoiseLevel', 'BusinessAcceptsBitcoin', 'DriveThru', 'Caters']
nested = ['GoodForMeal', 'HairSpecializesIn', 'Ambience', 'Music', 'DietaryRestrictions', 'BestNights', 'BusinessParking']
normal = list(set(attr)-set(nested))
normalAttr = {}
for i in normal:
    normalAttr[i] = set()

data = [json.loads(line) for line in open('../raw.nosync/yelp_dataset/business.json', 'r')]

for d in data:
    if d['attributes'] is not None:
        for k, v in d['attributes'].items():
            if v is not None and k in normal:
                normalAttr[k].add(str(v))

with open('../raw.nosync/normalAttr.txt', 'w') as f:
    for k, v in normalAttr.items():
        f.write(k + ': ')
        for i in v:
            f.write(i + ' ')
        f.write('\n')