from os.path import join, exists
from os import getcwd, mkdir
from logging import info

from util import locked_file, is_fresh, touch, run_cmd

def prepare_git_checkout(account, repo, ref):
    '''
    '''
    repo_href = 'https://github.com/%s/%s.git' % (account, repo)
    repo_path = join(getcwd(), 'repos/%s-%s' % (account, repo))
    checkout_path = join(getcwd(), 'checkouts/%s-%s-%s' % (account, repo, ref))
    checkout_lock = checkout_path + '.lock'
    
    if exists(checkout_path) and is_fresh(checkout_path):
        return checkout_path
    
    with locked_file(checkout_lock):
        if not exists(repo_path):
            git_clone(repo_href, repo_path)
        
        git_fetch(repo_path)
        git_checkout(repo_path, checkout_path, ref)
        from jekyll import jekyll_build
        jekyll_build(checkout_path)
    
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
