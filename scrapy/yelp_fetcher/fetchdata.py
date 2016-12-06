"""
This Python script sends a signed OAuth request to Yelp's Search web service and parses the JSON file returned in a looping manner until it reaches the known limit of Yelp's returned results - 1000
"""
import requests
import oauth2
import json
import sys
import time
import re
import os

consumer_key = "nCMEN9VxOhmMvzywgv_xgQ"
consumer_secret = "e_AO_k3kCxBtNicfGGN3wkFA-5M"
token = "tvcX-bydNutCUOOeWUZThg42fhdXy2-R"
token_secret ="M8aFixHy_789P5d0fjBJSoSKifM"
url="http://api.yelp.com/v2/search"

city_list = [
    'New+York+City',
    'Los+Angeles',
    'Chicago',
    'Houston',
    'San+Francisco',
    'Philadelphia',
    'Phoenix',
    'Dallas',
    'Seattle',
    'Boston',
    'San+Diego',
    'Washington',
    'Las+Vegas',
    'Pittsburgh',
    'Madison'
]

file_chunk_size = 1000
for city in city_list:
    filepath = "data/business.%s.jl" % city
    if os.path.isfile(filepath): continue
    url_params = {'location':city, 'limit':'20', 'offset' : '0'}
    with open(filepath, 'a') as f:
        # Loop by incrementing the offset until it hits 100 results returned
        for num in range (0,file_chunk_size,20):
            url_params.update({'offset':num})

            consumer = oauth2.Consumer(consumer_key, consumer_secret)
            oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

            oauth_request.update(
                {
                    'oauth_nonce': oauth2.generate_nonce(),
                    'oauth_timestamp': oauth2.generate_timestamp(),
                    'oauth_token': token,
                    'oauth_consumer_key': consumer_key
                }
            )
            new_token = oauth2.Token(token, token_secret)
            oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, new_token)
            signed_url = oauth_request.to_url()

            res = json.loads(requests.get(signed_url).text)
            try:
                businesses = res['businesses']
            except Exception as e:
                f.write(json.dumps(res))
                continue
            for b in businesses:
                try:
                    l = []
                    l.append(b['id'])
                    l.append(b['name'])
                    l.append(b['rating'])
                    l.append(b['categories'])
                    l.append(b['location']['coordinate'])
                    l.append(b['review_count'])
                    f.write(json.dumps(l))
                    f.write('\n')
                except Exception as e:
                    continue
            print num,
        print "\nFinish File %s (%d)"%(city, file_chunk_size)

    f.close()