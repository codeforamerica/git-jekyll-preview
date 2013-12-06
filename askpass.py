#!/usr/bin/env python
#
# Short & sweet script for use with git clone and fetch credentials.
# Requires GIT_USERNAME and GIT_PASSWORD environment variables.
#

import sys, os

print >> sys.stderr, sys.argv
print >> sys.stderr, os.environ

if sys.argv[1] == "Username for 'https://github.com': ":
    print os.environ['GIT_USERNAME']
    exit()

if sys.argv[1] == "Password for 'https://%(GIT_USERNAME)s@github.com': " % os.environ:
    print os.environ['GIT_PASSWORD']
    exit()

exit(1)
