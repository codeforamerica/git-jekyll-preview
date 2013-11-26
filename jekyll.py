from os.path import join, exists
from logging import info

from util import run_cmd, touch, is_fresh

def jekyll_build(checkout_path):
    '''
    '''
    jekyll_path = join(checkout_path, '_site')

    if exists(jekyll_path) and is_fresh(jekyll_path):
        return jekyll_path
    
    info('Building jekyll ' + jekyll_path)
    run_cmd(('jekyll', 'build'), checkout_path)
    touch(jekyll_path)
    
    return jekyll_path
