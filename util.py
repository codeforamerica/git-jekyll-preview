from os import utime, stat, listdir
from fcntl import flock, LOCK_EX, LOCK_UN
from contextlib import contextmanager
from subprocess import Popen, PIPE
from mimetypes import guess_type
from logging import debug
from os.path import join
from time import time

from flask import Response

@contextmanager
def locked_file(path):
    ''' Create a file, lock it, then unlock it. Use as a context manager.
    
        Yields nothing.
    '''
    debug('Locking ' + path)
    
    try:
        file = open(path, 'a')
        flock(file, LOCK_EX)
        
        yield

    finally:
        debug('Unlocking ' + path)
        flock(file, LOCK_UN)

def is_fresh(path):
    ''' Return true if path is younger than 10 seconds.
    '''
    return stat(path).st_mtime > time() - 10

def touch(path):
    ''' Touch the path to bring its modified timestamp to now.
    '''
    debug('Touching ' + path)
    utime(path, None)

def run_cmd(args, cwd=None):
    ''' Runs a single command in a new process, returns its stdout.
    '''
    command = Popen(args, stdout=PIPE, cwd=cwd)
    command.wait()
    
    if command.returncode != 0:
        raise RuntimeError(command.stderr.read())
    
    return command.stdout.read()

def get_file_response(path):
    ''' Return a flask Response for a simple file.
    '''
    mimetype, encoding = guess_type(path)
    
    with open(path) as file:
        return Response(file.read(), headers={'Content-Type': mimetype})

def get_directory_response(path):
    ''' Return a flask Response for a directory listing.
    '''
    names = listdir(path)

    if 'index.html' in names:
        return get_file_response(join(path, 'index.html'))
    
    items = ['<li><a href="%s">%s</a></li>' % (n, n) for n in names]
    html = '<ul>' + ''.join(items) + '</ul>'
    
    return Response(html, headers={'Content-Type': 'text/html'})
