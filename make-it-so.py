from logging import DEBUG, basicConfig
from os.path import join, isdir, isfile
from traceback import format_exc
from urllib import urlencode
from time import time

from flask import Flask, redirect, request, make_response, render_template, session

from requests import post
from requests_oauthlib import OAuth2Session
from git import prepare_git_checkout, PrivateRepoException
from git import MissingRepoException, MissingRefException
from href import needs_redirect, get_redirect
from util import get_directory_response
from util import get_file_response
from jekyll import jekyll_build

from git import github_client_id, github_client_secret
flask_secret_key = 'poop'

app = Flask(__name__)
app.secret_key = flask_secret_key

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

def get_token():
    ''' Get OAuth token from flask.session, or a fake one guaranteed to fail.
    '''
    token = dict(token_type='bearer', access_token='<fake token, will fail>')
    token.update(session.get('token', {}))
    
    return token

def make_401_response():
    ''' Create an HTTP 401 Not Authorized response to trigger Github OAuth.
    
        Start by redirecting the user to Github OAuth authorization page:
        http://developer.github.com/v3/oauth/#redirect-users-to-request-github-access
    '''
    state_id = 'foobar' # fake.
    states = session.get('states', {})
    states[state_id] = dict(redirect=request.url, created=time())
    session['states'] = states
    
    data = dict(scope='user,repo', client_id=github_client_id, state=state_id)
    
    auth = redirect('https://github.com/login/oauth/authorize?' + urlencode(data), 302)
    auth.headers['Cache-Control'] = 'no-store private'
    auth.headers['Vary'] = 'Referer'

    return auth

def make_404_response(template, vars):
    '''
    '''
    return make_response(render_template(template, **vars), 404)

def make_500_response(error, traceback):
    '''
    '''
    vars = dict(error=error, traceback=traceback)
    
    return make_response(render_template('error-runtime.html', **vars), 500)

@app.route('/')
def hello_world():
    if should_redirect():
        return make_redirect()
    
    id = session.get('id', None)
    
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
    
    return render_template('index.html', id=id, script=script, request=request)

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

@app.route('/oauth/callback')
def get_oauth_callback():
    ''' Handle Github's OAuth callback after a user authorizes.
    
        http://developer.github.com/v3/oauth/#github-redirects-back-to-your-site
    '''
    if 'error' in request.args:
        return render_template('error-oauth.html', reason="you didn't authorize access to your account.")
    
    try:
        code, state_id = request.args['code'], request.args['state']
    except:
        return render_template('error-oauth.html', reason='missing code or state in callback.')
    
    try:
        state = session['states'].pop(state_id)
    except:
        return render_template('error-oauth.html', reason='state "%s" not found?' % state_id)
    
    #
    # Exchange the temporary code for an access token:
    # http://developer.github.com/v3/oauth/#parameters-1
    #
    data = dict(client_id=github_client_id, code=code, client_secret=github_client_secret)
    resp = post('https://github.com/login/oauth/access_token', urlencode(data),
                headers={'Accept': 'application/json'})
    auth = resp.json()
    
    if 'error' in auth:
        return render_template('error-oauth.html', reason='Github said "%(error)s".' % auth)
    
    elif 'access_token' not in auth:
        return render_template('error-oauth.html', reason="missing `access_token`.")
    
    session['token'] = auth
    
    #
    # Figure out who's here.
    #
    url = 'https://api.github.com/user'
    id = OAuth2Session(github_client_id, token=session['token']).get(url).json()
    id = dict(login=id['login'], avatar_url=id['avatar_url'], html_url=id['html_url'])
    session['id'] = id
    
    other = redirect(state['redirect'], 302)
    other.headers['Cache-Control'] = 'no-store private'
    other.headers['Vary'] = 'Referer'

    return other

@app.route('/logout', methods=['POST'])
def logout():
    '''
    '''
    if 'id' in session:
        session.pop('id')

    if 'token' in session:
        session.pop('token')
    
    return redirect('/', 302)

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
        site_path = jekyll_build(prepare_git_checkout(account, repo, ref, token=get_token()))
    except MissingRepoException:
        return make_404_response('no-such-repo.html', dict(account=account, repo=repo))
    except MissingRefException:
        return make_404_response('no-such-ref.html', dict(account=account, repo=repo, ref=ref))
    except PrivateRepoException:
        return make_401_response()
    except RuntimeError, e:
        return make_500_response(e, format_exc())

    return get_directory_response(site_path)

@app.route('/<account>/<repo>/<ref>/<path:path>')
def repo_ref_path(account, repo, ref, path):
    ''' Show response for a path, whether a file or directory.
    '''
    if should_redirect():
        return make_redirect()

    try:
        site_path = jekyll_build(prepare_git_checkout(account, repo, ref, token=get_token()))
    except MissingRepoException:
        return make_404_response('no-such-repo.html', dict(account=account, repo=repo))
    except MissingRefException:
        return make_404_response('no-such-ref.html', dict(account=account, repo=repo, ref=ref))
    except PrivateRepoException:
        return make_401_response()
    except RuntimeError, e:
        return make_500_response(e, format_exc())
    
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

    
