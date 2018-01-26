import os
import json

import requests
import git


bitbucket_base_url = 'https://api.bitbucket.org/'

bitbucket_username = os.getenv('BITBUCKET_USERNAME', '')
bitbucket_password = os.getenv('BITBUCKET_PASSWORD', '')
my_repository_response = requests.get(
    bitbucket_base_url + '2.0/repositories/' + bitbucket_username,
    auth=(bitbucket_username, bitbucket_password))


my_repositories = json.loads(my_repository_response.text)['values']

repository_base_dir = './repositories'

if not os.path.exists(repository_base_dir):
    os.makedirs(repository_base_dir)

for repository in my_repositories:
    repository_dir = repository_base_dir
    if not os.path.exists(repository_dir):
        os.makedirs(repository_dir)

    git.Git(repository_dir).clone(repository['links']['clone'][0]['href'])







