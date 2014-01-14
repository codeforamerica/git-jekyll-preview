from os.path import join, exists, dirname
from os import getcwd, mkdir, environ
from logging import info, debug

from util import locked_file, is_fresh, touch, run_cmd
from requests_oauthlib import OAuth2Session
from requests import get

github_client_id = r'e62e0d541bb6d0125b62'
github_client_secret = r'1f488407e92a59beb897814e9240b5a06a2020e3'

class PrivateRepoException (Exception): pass

class MissingRepoException (Exception): pass

class MissingRefException (Exception): pass

def prepare_git_checkout(account, repo, ref, token):
    '''
    '''
    repo_href = 'https://github.com/%s/%s.git' % (account, repo)
    repo_path = join(getcwd(), 'repos/%s-%s' % (account, repo))
    repo_refs = 'https://api.github.com/repos/%s/%s/branches' % (account, repo)
    checkout_path = join(getcwd(), 'checkouts/%s-%s-%s' % (account, repo, ref))
    checkout_lock = checkout_path + '.git-lock'
    
    if exists(checkout_path) and is_fresh(checkout_path):
        return checkout_path
    
    auth_check = OAuth2Session(github_client_id, token=token).get(repo_refs)
    
    if auth_check.status_code == 401:
        # Github wants authentication.
        raise PrivateRepoException()
    
    elif auth_check.status_code == 404:
        # This repository might not exist at all?
        raise MissingRepoException()
    
    branches = dict([(b['name'], b['commit']['sha']) for b in auth_check.json()])
    ref_sha = branches.get(ref, None)

    if ref_sha is None:
        # The repository exists, but the branch does not?
        raise MissingRefException()
    
    elif token:
        debug('Adding Github credentials to environment')
        environ.update(dict(GIT_ASKPASS=join(dirname(__file__), 'askpass.py')))
        environ.update(dict(GIT_USERNAME=token['access_token'], GIT_PASSWORD=''))
    
    else:
        debug('Clearing Github credentials from environment')
        environ.update(dict(GIT_ASKPASS='', GIT_USERNAME='', GIT_PASSWORD=''))

    with locked_file(checkout_lock):
        if not exists(repo_path):
            git_clone(repo_href, repo_path)
        else:
            git_fetch(repo_path, ref, ref_sha)

        git_checkout(repo_path, checkout_path, ref)
    
    # Make sure these are gone before we return.
    environ.update(dict(GIT_ASKPASS='', GIT_USERNAME='', GIT_PASSWORD=''))
    
    return checkout_path

def git_clone(href, path):
    ''' Clone a git repository from its remote address to a local path.
    '''
    info('Cloning to ' + path)
    run_cmd(('git', 'clone', '--mirror', href, path))

def get_ref_sha(repo_path, ref):
    ''' Get the current SHA for a ref in the given repo path.
    '''
    return run_cmd(('git', 'show', '--pretty=%H', '--summary', ref), repo_path).strip()

def git_fetch(repo_path, ref, sha):
    ''' Run `git fetch` inside a local git repository.
    '''
    info('Fetching in ' + repo_path)
    
    try:
        found_sha = get_ref_sha(repo_path, ref)
    except RuntimeError:
        #
        # Account for a missing ref by performing a complete fetch.
        #
        debug('Complete fetch in '+repo_path)
        run_cmd(('git', 'fetch'), repo_path)
        found_sha = get_ref_sha(repo_path, ref)
    
    if sha == found_sha:
        debug('Skipping fetch in '+repo_path)
    
    else:
        run_cmd(('git', 'fetch'), repo_path)
    
    touch(repo_path)

def git_checkout(repo_path, checkout_path, ref):
    ''' Check out a git repository to a given reference and path.
        
        This function is assumed to be run in a lock.
    '''
    info('Checking out to ' + checkout_path)

    if not exists(checkout_path):
        mkdir(checkout_path)
    
    hash_file = checkout_path + '.commit-hash'
    commit_hash = get_ref_sha(repo_path, ref)
    
    do_checkout = True
    
    if exists(hash_file):
        previous_hash = open(hash_file).read().strip()
        
        if previous_hash == commit_hash:
            debug('Skipping checkout to '+checkout_path)
            do_checkout = False

    if do_checkout:
        run_cmd(('git', '--work-tree='+checkout_path, 'checkout', ref, '--', '.'), repo_path)
    
    touch(checkout_path)
    
    with open(hash_file, 'w') as file:
        print >> file, commit_hash
