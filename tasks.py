# -*- coding: utf-8 -*-
import functools

import invoke


def _out(name, message):
    print('[\033[1;37m{}\033[0m] {}'.format(name, message))


@invoke.task(name='deploy')
def deploy(**kwargs):
    print('So you want to deploy? Let\'s get started.')

    # Heroku.
    print('- Deploying Hello! Base to Heroku...')
    invoke.run('git push heroku master')

    # Done!
    print('')
    print('All done!')


@invoke.task(name='collect')
def development_collectstatic(**kwargs):
    out = functools.partial(_out, 'development.collectstatic')
    # Pre-compile all of our assets.
    invoke.run('handlebars base/templates/partials/handlebars -f base/static/javascripts/application/templates.js')
    invoke.run('compass compile -e production --force')

    # Build and send it off.
    invoke.run('python manage.py buildstatic --configuration=Production')
    invoke.run('python manage.py createstaticmanifest --configuration=Production')
    invoke.run('python manage.py eccollect --pp=progressive --configuration=Production --noinput --dry-run')


@invoke.task(name='server')
def development_server(**kwargs):
    # Use Foreman to start all the development processes.
    out = functools.partial(_out, 'development.server')
    invoke.run('foreman start -f Procfile.dev', pty=True)


@invoke.task(name='collectstatic')
def heroku_collectstatic(**kwargs):
    out = functools.partial(_out, 'heroku.collectstatic')
    invoke.run('heroku run python manage.py collectstatic --noinput')


@invoke.task(name='migrate')
def heroku_migrate(app='', **kwargs):
    out = functools.partial(_out, 'heroku.migrate')
    invoke.run('heroku run python manage.py migrate %s' % app)


@invoke.task(name='syncdb')
def heroku_syncdb(**kwargs):
    out = functools.partial(_out, 'heroku.syncdb')
    invoke.run('heroku run python manage.py syncdb')


ns = invoke.Collection(
    deploy,
    development_collectstatic,
    development_server,
    heroku=invoke.Collection(
        heroku_collectstatic,
        heroku_migrate,
        heroku_syncdb,
    )
)
