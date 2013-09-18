from invoke import run, task

@task
def deploy():
    print('So you want to deploy? Let\'s get started.')

    # Static Files.
    print('- Run the stylesheets through Compass using "Production" settings...')
    run('compass compile -e production --force -q')

    print('- Collecting the static files and throwing them on S3...')
    run('python manage.py collectstatic --configuration=Production --noinput -v 0')

    # Heroku.
    print('- Deploying Hello! Base to Heroku...')
    run('git push heroku master')

    # Done!
    print('')
    print('All done!')


@invoke.task
def compile():
    # Compile the CSS.
    print('- Run the stylesheets through Compass using "Production" settings...')
    run('compass compile -e production --force -q')

    # Compile the Handlebars.
    print('- Compile all of the Handlebars...')
    run('handlebars base/templates/partials/handlebars -f static/javascripts/templates.js')


@invoke.task
def run():
    # Use Foreman to start all the development processes.
    run('foreman start -f Procfile.dev', pty=True)
