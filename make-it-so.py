from logging import DEBUG, basicConfig
from os.path import join, isdir, isfile
from time import time

from flask import Flask, redirect, request, make_response, render_template

from git import prepare_git_checkout, PrivateRepoException, MissingRepoException
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

    other = redirect(get_redirect(request.path, referer_url), 302)
    other.headers['Cache-Control'] = 'no-store private'
    other.headers['Vary'] = 'Referer'

    return other

def get_auth():
    ''' Get (username, password) tuple from flask.request, or None.
    '''
    auth = request.authorization
    
    return (auth.username, auth.password) if auth else None

def make_401_response():
    ''' Create an HTTP 401 Not Authorized response to trigger basic auth.
    '''
    resp = make_response('No!', 401)
    resp.headers['WWW-Authenticate'] = 'Basic realm="Please enter a Github username and password. These will be passed on to Github.com, and not stored or recorded."'
    
    return resp

def make_404_response(template, vars):
    '''
    '''
    return make_response(render_template(template, **vars), 404)

@app.route('/')
def hello_world():
    if should_redirect():
        return make_redirect()
    
    script = '''
    javascript:(
        function ()
        {
            document.getElementsByTagName('head')[0].appendChild(document.createElement('script')).src='http://host:port/bookmarklet.js';
        }()
    );
    '''
    
    script = script.replace('http', request.scheme)
    script = script.replace('host:port', request.host)
    script = script.replace(' ', '').replace('\n', '')
    
    return render_template('index.html', script=script, request=request)

@app.route('/.well-known/status')
def wellknown_status():
    if should_redirect():
        return make_redirect()
    
    status = '''
    {
      "status": "ok",
      "updated": %d,
      "dependencies": [ ],
      "resources": { }
    }
    ''' % time()
    
    resp = make_response(status, 200)
    resp.headers['Content-Type'] = 'application/json'

    return resp

@app.route('/bookmarklet.js')
def bookmarklet_script():
    if should_redirect():
        return make_redirect()
    
    js = open('scripts/bookmarklet.js').read()

    script = make_response(js.replace('host:port', request.host), 200)
    script.headers['Content-Type'] = 'text/javascript'
    script.headers['Cache-Control'] = 'no-store private'

    return script

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
    
    return redirect('/%s/%s/%s/' % (account, repo, ref), 302)

@app.route('/<account>/<repo>/<ref>/')
def repo_ref_slash(account, repo, ref):
    ''' Show repository root directory listing.
    '''
    if should_redirect():
        return make_redirect()
    
    try:
        site_path = jekyll_build(prepare_git_checkout(account, repo, ref, auth=get_auth()))
    except MissingRepoException:
        return make_404_response('no-such-repo.html', dict(account=account, repo=repo))
    except PrivateRepoException:
        return make_401_response()

    return get_directory_response(site_path)

@app.route('/<account>/<repo>/<ref>/<path:path>')
def repo_ref_path(account, repo, ref, path):
    ''' Show response for a path, whether a file or directory.
    '''
    if should_redirect():
        return make_redirect()

    try:
        site_path = jekyll_build(prepare_git_checkout(account, repo, ref, auth=get_auth()))
    except MissingRepoException:
        return make_404_response('no-such-repo.html', dict(account=account, repo=repo))
    except PrivateRepoException:
        return make_401_response()
    
    local_path = join(site_path, path)

    if isfile(local_path) and not isdir(local_path):
        return get_file_response(local_path)
    
    if isdir(local_path) and not path.endswith('/'):
        other = redirect('/%s/%s/%s/%s/' % (account, repo, ref, path), 302)
        other.headers['Cache-Control'] = 'no-store private'
        return other
    
    if isdir(local_path):
        return get_directory_response(local_path)
    
    kwargs = dict(account=account, repo=repo, ref=ref, path=path)
    return make_404_response('error-404.html', kwargs)

@app.route('/<path:path>')
def all_other_paths(path):
    '''
    '''
    if should_redirect():
        return make_redirect()

if __name__ == '__main__':
    basicConfig(level=DEBUG, format='%(levelname)06s: %(message)s')
    app.run('0.0.0.0', debug=True)

    
