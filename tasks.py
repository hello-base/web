# -*- coding: utf-8 -*-
import functools

import invoke


def _out(name, message):
    print('[\033[1;37m{}\033[0m] {}'.format(name, message))


@invoke.task(name='deploy')
def deploy(**kwargs):
    print('So you want to deploy? Let\'s get started.')

    # Compile the Handlebars.
    print('- Compile all of the Handlebars...')
    invoke.run('handlebars base/templates/partials/handlebars -f static/javascripts/templates.js')

    # Static Files.
    print('- Run the stylesheets through Compass using "Production" settings...')
    invoke.run('compass compile -e production --force -q')

    print('- Collecting the static files and throwing them on S3...')
    invoke.run('python manage.py collectstatic --configuration=Production --noinput -v 0')

    # Heroku.
    print('- Deploying Hello! Base to Heroku...')
    invoke.run('git push heroku master')

    # Done!
    print('')
    print('All done!')


@invoke.task(name='collect')
def development_collectstatic(**kwargs):
    out = functools.partial(_out, 'development.collectstatic')
    invoke.run('python manage.py eccollect --pp=progressive --configuration=Production --noinput')
    invoke.run('python manage.py createstaticmanifest')


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
    development_server,
    heroku=invoke.Collection(
        heroku_collectstatic,
        heroku_migrate,
        heroku_syncdb,
    )
)
