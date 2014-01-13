Git-Jekyll Preview
==================

Preview your Github-hosted websites before making them live. Use it to check
your plain static or [Jekyll](http://jekyllrb.com/)-generated websites before
you make them live to [Github Pages](http://pages.github.com/) or to your own
server.

Try it live at [jekit.codeforamerica.org](http://jekit.codeforamerica.org).

Status, Contact
---------------

Git-Jekyll Preview is mostly a singleton-app, built only to be run at a single
location. For the time being, it's not intended for general redeployment but
improvements for [jekit.codeforamerica.org](http://jekit.codeforamerica.org)
are welcomed.

[Michal Migurski](https://github.com/migurski) is currently maintainer.

Install
-------

Git-Jekyll Preview is intended to be run on its own Ubuntu server, and will
not currently work on a managed system like Heroku. Installation dependencies
are managed by [Chef](https://wiki.opscode.com/display/chef/Home). It should
be possible to install Chef and run all required recipes with the script
[install.sh](install.sh). Note the world-writeable directories created in
[chef/directories](chef/directories/recipes/default.rb).

The application is a [Flask](http://flask.pocoo.org)-based Python server which
shells out to [Git](https://www.kernel.org/pub/software/scm/git/docs/) for
interaction with Github. [OAuth](http://developer.github.com/v3/oauth/) is
used for authentication; put your client ID and secret in [git.py](git.py).

To run for testing:

    python make-it-so.py

To run in production, with [Gunicorn](http://gunicorn.org):

    gunicorn make-it-so:app
