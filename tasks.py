# -*- coding: utf-8 -*-
import functools
import os

import invoke


def _out(name, message):
    print('[\033[1;37m{}\033[0m] {}'.format(name, message))


@invoke.task(name='collect')
def development_collectstatic(**kwargs):
    out = functools.partial(_out, 'development.collectstatic')
    # Pre-compile all of our assets.
    invoke.run('handlebars base/templates/partials/handlebars -f base/static/javascripts/application/templates.js')
    invoke.run('compass compile -e production --force')

    # Build and send it off.
    invoke.run('python manage.py buildstatic --configuration=Production')
    invoke.run('python manage.py createstaticmanifest --configuration=Production')
    invoke.run('python manage.py eccollect --pp=progressive --configuration=Production --noinput')


@invoke.task(name='yuglify')
def development_yuglify(**kwargs):
    out = functools.partial(_out, 'development.yuglify')
    STATIC_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'base', 'static')

    # Compile the application-specific Javascript.
    invoke.run('yuglify {input} --type js --combine {output}'.format(
        input=os.path.join(STATIC_ROOT, 'javascripts', 'application', '*.js'),
        output=os.path.join(STATIC_ROOT, 'javascripts', 'application')
    ))

    # Compile the 3rd-party Javascript components.
    invoke.run('yuglify {input} --type js --combine {output}'.format(
        input=os.path.join(STATIC_ROOT, 'javascripts', 'components', '*.js'),
        output=os.path.join(STATIC_ROOT, 'javascripts', 'components')
    ))

    # Compile the stylesheets.
    invoke.run('yuglify {input} --type js --combine {output}'.format(
        input=os.path.join(STATIC_ROOT, 'stylesheets', 'application.css'),
        output=os.path.join(STATIC_ROOT, 'stylesheets', 'production')
    ))


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
    development_collectstatic,
    development_server,
    development_yuglify,
    heroku=invoke.Collection(
        heroku_collectstatic,
        heroku_migrate,
        heroku_syncdb,
    )
)
