from invoke import run, task

@task
def deploy():
    print('So you want to deploy? Let\'s get started.')

    # Static Files.
    print('- Run the stylesheets through Compass using "Production" settings...')
    run('compass compile -e production --force -q')

    print('- Compile all of the Handlebars...')
    run('handlebars base/templates/partials/handlebars -f static/javascripts/application/templates.js')

    print('- Collecting the static files and throwing them on S3...')
    run('python manage.py collectstatic --configuration=Production --noinput -v 0')

    # Heroku.
    print('- Deploying Hello! Base to Heroku...')
    run('git push heroku master')

    # Done!
    print('')
    print('All done!')
