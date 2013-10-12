# -*- coding: utf-8 -*-
import functools
import os

import invoke


def _out(name, message):
    print('[\033[1;37m{}\033[0m] {}'.format(name, message))


@invoke.task(name='deploy', pre=['collect'])
def deploy(verbose=False, **kwargs):
    out = functools.partial(_out, 'project.deploy')
    hide = 'out' if not verbose else None

    # Before deploying, check if manifest.json has updated.
    MANIFEST = 'base/settings/manifest.json'
    out('Checking if manifest.json has been updated.')
    if invoke.run('git diff --name-only {0}'.format(MANIFEST), hide=hide).stdout:
        # manifest.json has been updated, let's commit it.
        out('manifest.json has been updated. Committing.')
        invoke.run('git add {0}'.format(MANIFEST), hide=hide)
        invoke.run('git commit -m "Static manifest has updated; committing updated manifest.json."', hide=hide)

    # Ready? Let's go.
    out('Deploying project to Heroku.')
    invoke.run('git push heroku master')

    # Done!
    out('All done~!')


@invoke.task(name='collect')
def collect(verbose=False, **kwargs):
    out = functools.partial(_out, 'project.collect')
    hide = 'out' if not verbose else None

    # Pre-compile all of our assets.
    out('Compiling Handlebars templates.')
    invoke.run('handlebars base/templates/partials/handlebars -f base/static/javascripts/application/templates.js', hide=hide)
    out('Compiling stylesheets using production environment settings.')
    invoke.run('compass compile -e production --force', hide=hide)
    out('Using Autoprefix to auto-prefix.')
    invoke.run('autoprefixer base/static/stylesheets/application.css', hide=hide)

    # Build and send it off.
    out('Using `buildstatic` to concatenate assets.')
    invoke.run('python manage.py buildstatic --configuration=Production', hide=hide)
    out('Updating `settings/manifest.json` with new asset hashes.')
    invoke.run('python manage.py createstaticmanifest --configuration=Production', hide=hide)
    out('Uploading and post-processing all of the assets.')
    invoke.run('python manage.py eccollect --pp=progressive --configuration=Production --noinput', hide=hide)


@invoke.task(name='yuglify')
def development_yuglify(**kwargs):
    out = functools.partial(_out, 'development.yuglify')
    STATIC_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'base', 'static')

    # Compile the application-specific Javascript.
    invoke.run('yuglify {input} --type js --combine {output}'.format(
        input=os.path.join(STATIC_ROOT, 'javascripts', 'application', '*.js'),
        output=os.path.join(STATIC_ROOT, 'javascripts', 'application')))
    out('javascripts/application.min.js created and minified.')

    # Compile the 3rd-party Javascript components.
    invoke.run('yuglify {input} --type js --combine {output}'.format(
        input=os.path.join(STATIC_ROOT, 'javascripts', 'components', '*.js'),
        output=os.path.join(STATIC_ROOT, 'javascripts', 'components')))
    out('javascripts/components.min.js created and minified.')

    # Compile the stylesheets.
    invoke.run('yuglify {input} --type js --combine {output}'.format(
        input=os.path.join(STATIC_ROOT, 'stylesheets', 'application.css'),
        output=os.path.join(STATIC_ROOT, 'stylesheets', 'production')))
    out('stylesheets/production.min.css created and minified.')


@invoke.task(name='server')
def development_server(**kwargs):
    # Use Foreman to start all the development processes.
    out = functools.partial(_out, 'development.server')
    invoke.run('foreman start -f Procfile.dev', pty=True)


@invoke.task(name='capture')
def heroku_capture(verbose=False, **kwargs):
    out = functools.partial(_out, 'heroku.capture')
    hide = 'out' if not verbose else None

    out('Snapshotting the production database.')
    invoke.run('heroku pgbackups:capture', hide=hide)


@invoke.task(name='migrate', pre=['heroku.capture'])
def heroku_migrate(app='', **kwargs):
    out = functools.partial(_out, 'heroku.migrate')
    invoke.run('heroku run python manage.py migrate %s' % app)


@invoke.task(name='pull', pre=['heroku.capture'])
def heroku_pull(verbose=False, database='hello-base', **kwargs):
    out = functools.partial(_out, 'heroku.pull')
    hide = 'out' if not verbose else None

    # Fetch the latest database dump.
    invoke.run('curl -o latest.dump `heroku pgbackups:url`')
    out('Latest database dump (latest.dump) grabbed via curl.', hide=hide)

    # Restore it.
    invoke.run('pg_restore --verbose --clean --no-acl --no-owner -h localhost -d %s latest.dump' % database, hide=hide)
    out('Restored latest production dump to local database.')


@invoke.task(name='syncdb')
def heroku_syncdb(**kwargs):
    out = functools.partial(_out, 'heroku.syncdb')
    invoke.run('heroku run python manage.py syncdb')


ns = invoke.Collection(
    collect, deploy, development_server, development_yuglify,
    heroku=invoke.Collection(
        heroku_capture, heroku_migrate, heroku_pull, heroku_syncdb,
    )
)
