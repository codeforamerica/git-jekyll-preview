#!/usr/bin/env python
from __future__ import division
from sys import argv
from os.path import join, isdir
from os import statvfs, listdir, stat, remove
from shutil import rmtree

if __name__ == '__main__':

    checkouts, repos = argv[1:]
    
    # Look at checkouts and repos in turn.
    for dirname in (checkouts, repos):

        # Calculate free space
        info = statvfs(dirname)
        free = info.f_bavail / info.f_blocks
        
        # Skip if free space is over 20%
        if free > .2:
            continue
        
        # Order directory contents by age, oldest-first
        paths = [join(dirname, name) for name in listdir(dirname)]
        times = [stat(path).st_mtime for path in paths]
        infos = zip(times, paths)
        infos.sort()
        
        if dirname == checkouts:
            # Remove twenty-five checkouts at a time
            removals = infos[:25]

        elif dirname == repos:
            # Remove one repo at a time
            removals = infos[:1]
        
        # Delete things
        for (time, path) in removals:
            print 'Removing', path
            
            if isdir(path):
                rmtree(path)
            else:
                remove(path)
