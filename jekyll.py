from os.path import join
from logging import debug

from util import working_directory, run_cmd

def jekyll_build(checkout_path):
    '''
    '''
    jekyll_path = join(checkout_path, '_site')
    debug('Building jekyll ' + jekyll_path)
    
    with working_directory(checkout_path):
        run_cmd('jekyll', 'build')
    
    return jekyll_path