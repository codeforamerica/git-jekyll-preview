from logging import DEBUG, basicConfig
from os.path import join, isdir, isfile

from flask import Flask, redirect, request, make_response

from git import prepare_git_checkout, PrivateRepoException
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

@app.route('/')
def hello_world():
    if should_redirect():
        return make_redirect()
    
    script = '''
        if(location.href.match(/^https:\/\/github.com\/.+\/.+\/(edit|blob)\/.+\/_posts\/....-..-..-.+$/))
        {
            var url = location.href.replace(/^https:\/\/github.com\/(.+\/.+)\/(edit|blob)\/(.+)\/_posts\/(....)-(..)-(..)-(.+)$/,
                                            'http://host:port/$1/$3/$4/$5/$6/$7');
        }
        else if(location.href.match(/^https:\/\/github.com\/.+\/.+\/(edit|blob)\/[^\/]+\/.+$/))
        {
            var url = location.href.replace(/^https:\/\/github.com\/(.+\/.+)\/(edit|blob)\/([^\/]+\/.+)$/,
                                            'http://host:port/$1/$3');
        }
        else if(location.href.match(/^http:\/\/prose.io\/#.+\/.+\/edit\/.+\/_posts\/....-..-..-.+$/))
        {
            var url = location.href.replace(/^http:\/\/prose.io\/#(.+\/.+)\/edit\/(.+)\/_posts\/(....)-(..)-(..)-(.+)$/,
                                            'http://host:port/$1/$2/$3/$4/$5/$6');
        }
        else if(location.href.match(/^http:\/\/prose.io\/#.+\/.+\/edit\/[^\/]+\/.+$/))
        {
            var url = location.href.replace(/^http:\/\/prose.io\/#(.+\/.+)\/edit\/([^\/]+\/.+)$/,
                                            'http://host:port/$1/$2');
        }
        else
        {
            var url = false;
        }
        
        if(url)
        {
            if(url && url.match(/\.(md|markdown)$/)) {
                url = url.replace(/\.(md|markdown)$/, '.html');
            }
        
            alert(url);
        }
    '''
    
    script = script.replace('host:port', request.host).replace('+', '%2B')
    script = script.replace('var ', 'var%20').replace('else if', 'else%20if')
    script = script.replace(' ', '').replace('\n', '').replace('#', '%23')
    
    return 'Drag this to your bookmarks bar: <a href="javascript:%s">Preview on %s</a>' % (script, request.host)

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
    except PrivateRepoException:
        return make_401_response()
    
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

    
