from logging import DEBUG, basicConfig
from os.path import join, isdir, isfile

from flask import Flask, redirect, request

from git import prepare_git_checkout
from href import needs_redirect, get_redirect
from util import get_directory_response
from util import get_file_response
from jekyll import jekyll_build

app = Flask(__name__)

def should_redirect():
    ''' Return True if the current flask.request should redirect.
    '''
    referer_url = request.headers.get('Referer')
    
    if not referer_url:
        return False
    
    return needs_redirect(request.host, request.path, referer_url)

def make_redirect():
    ''' Return a flask.redirect for the current flask.request.
    '''
    referer_url = request.headers.get('Referer')
    return redirect(get_redirect(request.path, referer_url), 302)

@app.route('/')
def hello_world():
    if should_redirect():
        return make_redirect()
    
    return 'Hello world'

@app.route('/<account>/<repo>')
def repo_only(account, repo):
    ''' Redirect to "master" on a hunch.
    '''
    if should_redirect():
        return make_redirect()
    
    return redirect('/%s/%s/master/' % (account, repo), 302)

@app.route('/<account>/<repo>/')
def repo_only_slash(account, repo):
    ''' Redirect to "master" on a hunch.
    '''
    if should_redirect():
        return make_redirect()
    
    return redirect('/%s/%s/master/' % (account, repo), 302)

@app.route('/<account>/<repo>/<ref>')
def repo_ref(account, repo, ref):
    ''' Redirect to add trailing slash.
    '''
    if should_redirect():
        return make_redirect()
    
    jekyll_build(prepare_git_checkout(account, repo, ref))
    return redirect('/%s/%s/%s/' % (account, repo, ref), 302)

@app.route('/<account>/<repo>/<ref>/')
def repo_ref_slash(account, repo, ref):
    ''' Show repository root directory listing.
    '''
    if should_redirect():
        return make_redirect()
    
    site_path = jekyll_build(prepare_git_checkout(account, repo, ref))
    return get_directory_response(site_path)

@app.route('/<account>/<repo>/<ref>/<path:path>')
def repo_ref_path(account, repo, ref, path):
    ''' Show response for a path, whether a file or directory.
    '''
    if should_redirect():
        return make_redirect()

    site_path = jekyll_build(prepare_git_checkout(account, repo, ref))
    local_path = join(site_path, path)
    
    if isfile(local_path) and not isdir(local_path):
        return get_file_response(local_path)
    
    if isdir(local_path) and not path.endswith('/'):
        return redirect('/%s/%s/%s/%s/' % (account, repo, ref, path), 302)
    
    if isdir(local_path):
        return get_directory_response(local_path)
    
    return 'finished path ' + path

@app.route('/<path:path>')
def all_other_paths(path):
    '''
    '''
    if should_redirect():
        return make_redirect()

if __name__ == '__main__':
    basicConfig(level=DEBUG, format='%(levelname)06s: %(message)s')
    app.run('0.0.0.0', debug=True)

    
