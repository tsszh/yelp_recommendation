import json

business_dict = {}
with open("data/business_map.jl") as f:
	for line in f:
		d = json.loads(line)
		business_dict[d[0]] = d[1]
f.close()

filterSet = set([
	"Restaurants",
	"Food",
	"Diners",
	"Bars",
	"Breakfast & Brunch",
	"Nightlife"
])

with open("data/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json") as fr,\
	 open("data/business.jl", "w") as fw:
	for line in fr:
		d = json.loads(line)
		if not "Restaurants" in d['categories']: continue
		fw.write( json.dumps([
			business_dict[ d['business_id'] ],
			"%s, %s"%(d['name'], d['city']),
			list( filter(lambda r: not r in filterSet, d['categories']) )
			]) )
		fw.write('\n')
fr.close()
fw.close()