module.exports = (grunt) ->
  # Configuration.
  grunt.initConfig
    pkg: grunt.file.readJSON 'package.json'

    autoprefixer:
      production:
        src: './base/static/stylesheets/application.css'
        dest: './base/static/stylesheets/production.css'

    csso:
      production:
        files:
          './base/static/stylesheets/production.min.css': ['./base/static/stylesheets/production.css']

    sass:
      development:
        options:
          style: 'compressed'
        files:
          './base/static/stylesheets/application.css': './base/assets/stylesheets/application.scss'

    uglify:
      production:
        files:
          './base/static/javascripts/components.min.js': ['./base/static/javascripts/components/*.js'],
          './base/static/javascripts/application.min.js': ['./base/static/javascripts/application/*.js']

    watch:
      css:
        files: '**/*.scss'
        tasks: ['sass']

  # Imports.
  grunt.loadNpmTasks 'grunt-autoprefixer'
  grunt.loadNpmTasks 'grunt-contrib-sass'
  grunt.loadNpmTasks 'grunt-contrib-uglify'
  grunt.loadNpmTasks 'grunt-contrib-watch'
  grunt.loadNpmTasks 'grunt-csso'

  # Task registration.
  grunt.registerTask 'default', [
    'sass',
    'watch'
  ]
  grunt.registerTask 'deploy', [
    'sass',
    'autoprefixer',
    'csso',
    'uglify'
  ]
