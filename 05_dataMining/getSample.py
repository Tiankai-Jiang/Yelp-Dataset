import json, csv

outfile = open("../raw.nosync/reviewSample.csv", 'w')
sfile = csv.writer(outfile, delimiter ="\t", quoting=csv.QUOTE_MINIMAL)
sfile.writerow(['stars', 'text'])

with open('../raw.nosync/yelp_dataset/review/review1.json') as f:
    i = 0
    for line in f:
        if i < 125000:
            i += 1
            row = json.loads(line)
            sfile.writerow([row['stars'], (row['text'])])
        else:
            break
outfile.close()