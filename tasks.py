# -*- coding: utf-8 -*-
import functools
import os

import invoke


def _out(name, message):
    print('[\033[1;37m{}\033[0m] {}'.format(name, message))


@invoke.task(name='collect')
def asset_collect(verbose=False, **kwargs):
    out = functools.partial(_out, 'project.collect')
    hide = 'out' if not verbose else None

    # Build and send it off.
    out('Using `buildstatic` to concatenate assets.')
    invoke.run('python manage.py buildstatic --configuration=Production', hide=hide)
    out('Updating `settings/manifest.json` with new asset hashes.')
    invoke.run('python manage.py createstaticmanifest --configuration=Production', hide=hide)
    out('Uploading and post-processing all of the assets.')
    invoke.run('python manage.py eccollect --configuration=Production --noinput', hide=hide)


@invoke.task(name='test')
def development_test(verbose=True, coverage=False, **kwargs):
    out = functools.partial(_out, 'development.test')
    hide = 'out' if not verbose else None
    pytest = 'py.test tests/'

    if coverage:
        out('Running tests (with Coverage report).')
        invoke.run('coverage run --branch --source base -m %s' % pytest, pty=True, hide=hide)
        invoke.run('coverage html', pty=True, hide=hide)
        invoke.run('open htmlcov/index.html')
    else:
        out('Running tests.')
        invoke.run('%s' % pytest, pty=True, hide=hide)


@invoke.task(name='deploy', pre=['test', 'collect'])
def deploy(verbose=False, migrate=False, **kwargs):
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
    if migrate:
        out('Snapshotting the production database.')
        invoke.run('heroku pgbackups:capture --expire', hide=hide)
        out('The migrations flag has been triggered, disable preboot.')
        invoke.run('heroku labs:disable preboot', hide=hide)

    out('Deploying project to Heroku.')
    invoke.run('git push heroku master')

    if migrate:
        out('Deploy to Heroku complete. Migrating...')
        invoke.run('heroku run python manage.py migrate')
        out('Re-enabling preboot.')
        invoke.run('heroku labs:enable preboot', hide=hide)

    # Done!
    out('All done~!')


@invoke.task(name='compile')
def asset_compile(verbose=False, **kwargs):
    out = functools.partial(_out, 'development.compile')
    hide = 'out' if not verbose else None
    STATIC_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'base', 'static')

    # Pre-compile all of our assets.
    out('Compiling Handlebars templates.')
    invoke.run('handlebars base/templates/partials/handlebars -f base/static/javascripts/application/templates.js', hide=hide)
    out('Compiling stylesheets using production environment settings.')
    invoke.run('compass compile -e production --force', hide=hide)

    # Compile the application-specific Javascript.
    invoke.run('yuglify {input} --type js --combine {output}'.format(
        input=os.path.join(STATIC_ROOT, 'javascripts', 'application', '*.js'),
        output=os.path.join(STATIC_ROOT, 'javascripts', 'application')), hide=hide)
    out('javascripts/application.min.js created and minified.')

    # Compile the 3rd-party Javascript components.
    invoke.run('yuglify {input} --type js --combine {output}'.format(
        input=os.path.join(STATIC_ROOT, 'javascripts', 'components', '*.js'),
        output=os.path.join(STATIC_ROOT, 'javascripts', 'components')), hide=hide)
    out('javascripts/components.min.js created and minified.')

    # Compile the stylesheets.
    invoke.run('autoprefixer -b "> 1%, last 3 versions, ff 17, opera 12.1" {input}'.format(
        input=os.path.join(STATIC_ROOT, 'stylesheets', 'application.css')), hide=hide)
    out('stylesheets/application.css auto-prefixed.')
    invoke.run('yuglify {input} --type css --combine {output}'.format(
        input=os.path.join(STATIC_ROOT, 'stylesheets', 'application.css'),
        output=os.path.join(STATIC_ROOT, 'stylesheets', 'production')), hide=hide)
    out('stylesheets/production.min.css created and minified.')


@invoke.task(name='flake')
def development_flake(**kwargs):
    invoke.run('flake8 --max-complexity 6 > flake8.txt')


@invoke.task(name='server')
def development_server(**kwargs):
    # Use Foreman to start all the development processes.
    invoke.run('foreman start -f Procfile.dev', pty=True)


@invoke.task(name='capture')
def heroku_capture(verbose=False, **kwargs):
    out = functools.partial(_out, 'heroku.capture')
    hide = 'out' if not verbose else None

    out('Snapshotting the production database.')
    invoke.run('heroku pgbackups:capture --expire', hide=hide)


@invoke.task(name='imagekit')
def heroku_imagekit(verbose=False, **kwargs):
    out = functools.partial(_out, 'heroku.imagekit')
    hide = 'out' if not verbose else None

    invoke.run('heroku run python manage.py generateimages', hide=hide)
    out('Thumbnails successfully generated by ImageKit.')


@invoke.task(name='migrate', pre=['heroku.capture'])
def heroku_migrate(app='', **kwargs):
    invoke.run('heroku run python manage.py migrate %s' % app)


@invoke.task(name='pull', pre=['heroku.capture'])
def heroku_pull(verbose=False, database='hello-base', **kwargs):
    out = functools.partial(_out, 'heroku.pull')
    hide = 'out' if not verbose else None

    # Fetch the latest database dump.
    invoke.run('curl -o latest.dump `heroku pgbackups:url`', hide=hide)
    out('Latest database dump (latest.dump) grabbed via curl.')

    # Restore it.
    invoke.run('pg_restore --verbose --clean --no-acl --no-owner -h localhost -d %s latest.dump' % database, hide=hide)
    invoke.run('rm latest.dump', hide=hide)
    out('Restored latest production dump to local database.')


@invoke.task(name='syncdb')
def heroku_syncdb(**kwargs):
    invoke.run('heroku run python manage.py syncdb')


ns = invoke.Collection(
    asset_collect, asset_compile, deploy, development_flake, development_server, development_test,
    heroku=invoke.Collection(
        heroku_capture, heroku_imagekit, heroku_migrate, heroku_pull, heroku_syncdb,
    )
)
