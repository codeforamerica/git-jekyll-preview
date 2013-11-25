from os.path import join
from logging import debug

from util import run_cmd

def jekyll_build(checkout_path):
    '''
    '''
    jekyll_path = join(checkout_path, '_site')
    debug('Building jekyll ' + jekyll_path)
    
    run_cmd(('jekyll', 'build'), checkout_path)
    
    return jekyll_path