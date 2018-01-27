import os
import json

import requests
import git
from github import Github
from github import GithubException

bitbucket_base_url = 'https://api.bitbucket.org/'

bitbucket_username = os.getenv('BITBUCKET_USERNAME', 'not initialized')
bitbucket_password = os.getenv('BITBUCKET_PASSWORD', 'not initialized')

github_api_base_url = 'https://api.github.com/'
github_base_url = 'https://github.com/'
github_token = os.getenv('GITHUB_TOKEN', 'not initialized')


repository_base_dir = './repositories'

if not os.path.exists(repository_base_dir):
    os.makedirs(repository_base_dir)


def create_github_repository(name, private=True):
    gh = Github(github_token)
    gh_user = gh.get_user()
    try:
        return gh_user.create_repo(name=name, private=private)
    except GithubException:
        return gh.get_repo(gh_user.login + '/' + name)

# Update bitbucket_username when get other owner's repositories
bitbucket_repos_response = json.loads(requests.get(
    bitbucket_base_url + '2.0/repositories/' + bitbucket_username,
    auth=(bitbucket_username, bitbucket_password)).text)


while True:
    bitbucket_repos = bitbucket_repos_response['values']
    for repository in bitbucket_repos:
        r = git\
            .Git(repository_base_dir)\
            .clone(repository['links']['clone'][0]['href'])

        repo_name = repository['name']
        gh_repo = create_github_repository(repo_name)
        g = git.Repo(repository_base_dir + os.sep + repo_name)

        gh_remote = g.create_remote('github', gh_repo.clone_url)
        gh_remote.push()

    if 'next' in bitbucket_repos_response:
        bitbucket_repos_response = \
            json.loads(
                requests.get(
                    bitbucket_repos_response['next'],
                    auth=(bitbucket_username, bitbucket_password)).text)
    else:
        break









