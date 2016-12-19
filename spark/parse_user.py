import json

user_dict = {}
with open("data/user_map.jl") as f:
	for line in f:
		d = json.loads(line)
		user_dict[d[0]] = d[1]
f.close()

with open("data/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_user.json") as fr,\
	 open("data/user.jl", "w") as fw:
	for line in fr:
		d = json.loads(line)
		fw.write( json.dumps([
			user_dict[ d['user_id'] ],
			d['name']
			]) )
		fw.write('\n')
fr.close()
fw.close()