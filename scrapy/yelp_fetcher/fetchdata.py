"""
This Python script sends a signed OAuth request to Yelp's Search web service and parses the JSON file returned in a looping manner until it reaches the known limit of Yelp's returned results - 1000
"""
import requests
import oauth2
import json
import sys
import time
import re

consumer_key = "nCMEN9VxOhmMvzywgv_xgQ"
consumer_secret = "e_AO_k3kCxBtNicfGGN3wkFA-5M"
token = "tvcX-bydNutCUOOeWUZThg42fhdXy2-R"
token_secret ="M8aFixHy_789P5d0fjBJSoSKifM"
url_params = {'location':'New+York+City', 'limit':'20', 'offset' : '0'}
url="http://api.yelp.com/v2/search"

lines = ['{"businesses": [']

# Loop by incrementing the offset until it hits 100 results returned
for num in range (0,80,20):

    url_params.update({'offset':num+1})

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
    
    businesses = re.sub(r'^{\"region\":.+?\"businesses\":\s\[({.+?})\].+?$',r'\1,',requests.get(signed_url).text)
    lines.append(businesses)

# Remove the last line and checks if that contains a ',' at the end. It should have since every line is appended with a ',' in the loop above
temp = lines[-1]
del lines[-1]

# If it does, remove the ',' and append the line back
if temp[-1]==',':
   lines.append(temp[:-1])
else:
   lines.append(temp)

lines.append("]}")

data = json.loads(''.join(lines))
businesses = data['businesses']
rows = []
for b in businesses:
    l = []
    l.append(b['id'])
    l.append(b['name'])
    l.append(b['rating'])
    l.append(b['categories'])
    l.append(b['location']['coordinate'])
    rows.append(l)

for r in rows:
    print r