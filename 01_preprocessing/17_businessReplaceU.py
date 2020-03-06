fin = open("../raw.nosync/yelp_dataset/business.json", "rt")
data = fin.read()
data = data.replace("\"u'", "\"'")
fin.close()

fin = open("../raw.nosync/yelp_dataset/business.json", "wt")
fin.write(data)
fin.close()