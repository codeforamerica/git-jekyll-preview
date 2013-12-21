from os.path import join, exists
from logging import info, debug
from shutil import copyfile

from util import run_cmd, touch, is_fresh, locked_file

def jekyll_build(checkout_path):
    '''
    '''
    checkout_lock = checkout_path + '.jekyll-lock'
    jekyll_path = join(checkout_path, '_site')
    built_hash_file = checkout_path + '.built-hash'
    hash_file = checkout_path + '.commit-hash'

    if exists(jekyll_path) and is_fresh(jekyll_path):
        return jekyll_path
    
    with locked_file(checkout_lock):
        do_build = True
    
        if exists(built_hash_file):
            built_hash = open(built_hash_file).read().strip()
            commit_hash = open(hash_file).read().strip()
        
            if built_hash == commit_hash:
                debug('Skipping build to ' + jekyll_path)
                do_build = False
    
        if do_build:
            info('Building jekyll ' + jekyll_path)
            run_cmd(('jekyll', 'build'), checkout_path)
        
            if exists(hash_file):
                copyfile(hash_file, built_hash_file)
    
        touch(jekyll_path)

    return jekyll_path
