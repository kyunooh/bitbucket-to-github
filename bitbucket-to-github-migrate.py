import os
import json

import requests


bitbucket_username = os.getenv('BITBUCKET_USERNAME', '')
bitbucket_password = os.getenv('BITBUCKET_PASSWORD', '')
r = requests.get('https://api.bitbucket.org/2.0/repositories/' + bitbucket_username, auth=(bitbucket_username, bitbucket_password))

bitbuckets = json.loads(r.text)


print(bitbuckets)
