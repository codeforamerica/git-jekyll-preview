from logging import DEBUG, basicConfig
from os.path import join, isdir, isfile

from flask import Flask, redirect

from git import prepare_git_checkout
from util import get_directory_response
from util import get_file_response

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world'

@app.route('/<account>/<repo>')
def repo_only(account, repo):
    ''' Redirect to "master" on a hunch.
    '''
    return redirect('/%s/%s/master/' % (account, repo), 302)

@app.route('/<account>/<repo>/')
def repo_only_slash(account, repo):
    ''' Redirect to "master" on a hunch.
    '''
    return redirect('/%s/%s/master/' % (account, repo), 302)

@app.route('/<account>/<repo>/<ref>')
def repo_ref(account, repo, ref):
    ''' Redirect to add trailing slash.
    '''
    prepare_git_checkout(account, repo, ref)
    return redirect('/%s/%s/%s/' % (account, repo, ref), 302)

@app.route('/<account>/<repo>/<ref>/')
def repo_ref_slash(account, repo, ref):
    ''' Show repository root directory listing.
    '''
    checkout_path = prepare_git_checkout(account, repo, ref)
    return get_directory_response(checkout_path)

@app.route('/<account>/<repo>/<ref>/<path:path>')
def repo_ref_path(account, repo, ref, path):
    ''' Show response for a path, whether a file or directory.
    '''
    checkout_path = prepare_git_checkout(account, repo, ref)
    local_path = join(checkout_path, path)
    
    if isfile(local_path) and not isdir(local_path):
        return get_file_response(local_path)
    
    if isdir(local_path) and not path.endswith('/'):
        return redirect('/%s/%s/%s/%s/' % (account, repo, ref, path), 302)
    
    if isdir(local_path):
        return get_directory_response(local_path)
    
    return 'finished path ' + path

if __name__ == '__main__':
    basicConfig(level=DEBUG, format='%(levelname)06s: %(message)s')
    app.run(debug=True)

    