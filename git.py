from os.path import join, exists, dirname
from os import getcwd, mkdir, environ
from logging import info, debug

from util import locked_file, is_fresh, touch, run_cmd
from requests import get

class PrivateRepoException (Exception): pass

def prepare_git_checkout(account, repo, ref, auth):
    '''
    '''
    repo_href = 'https://github.com/%s/%s.git' % (account, repo)
    repo_path = join(getcwd(), 'repos/%s-%s' % (account, repo))
    repo_refs = repo_href + '/info/refs?service=git-upload-pack'
    checkout_path = join(getcwd(), 'checkouts/%s-%s-%s' % (account, repo, ref))
    checkout_lock = checkout_path + '.lock'
    
    if exists(checkout_path) and is_fresh(checkout_path):
        return checkout_path
    
    auth_check = get(repo_refs, auth=auth)
    
    if auth_check.status_code == 401:
        # Github wants a username & password
        raise PrivateRepoException()
    
    elif auth:
        debug('Adding Github credentials to environment')
        environ.update(dict(GIT_ASKPASS=join(dirname(__file__), 'askpass.py')))
        environ.update(dict(GIT_USERNAME=auth[0], GIT_PASSWORD=auth[1]))
    
    else:
        debug('Clearing Github credentials from environment')
        environ.update(dict(GIT_ASKPASS='', GIT_USERNAME='', GIT_PASSWORD=''))

    with locked_file(checkout_lock):
        if not exists(repo_path):
            git_clone(repo_href, repo_path)
        else:
            git_fetch(repo_path)

        git_checkout(repo_path, checkout_path, ref)
        from jekyll import jekyll_build
        jekyll_build(checkout_path)
    
    # Make sure these are gone before we return.
    environ.update(dict(GIT_ASKPASS='', GIT_USERNAME='', GIT_PASSWORD=''))
    
    return checkout_path

def git_clone(href, path):
    ''' Clone a git repository from its remote address to a local path.
    '''
    info('Cloning to ' + path)
    run_cmd(('git', 'clone', '--mirror', href, path))

def git_fetch(repo_path):
    ''' Run `git fetch` inside a local git repository.
    '''
    info('Fetching in ' + repo_path)
    
    run_cmd(('git', 'fetch'), repo_path)
    
    touch(repo_path)

def git_checkout(repo_path, checkout_path, ref):
    ''' Check out a git repository to a given reference and path.
    '''
    info('Checking out to ' + checkout_path)

    if not exists(checkout_path):
        mkdir(checkout_path)

    run_cmd(('git', '--work-tree='+checkout_path, 'checkout', ref, '--', '.'), repo_path)
    
    touch(checkout_path)
