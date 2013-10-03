module.exports = (grunt) ->
  # Configuration.
  grunt.initConfig
    pkg: grunt.file.readJSON 'package.json'

    sass:
      main:
        options:
          style: 'compressed'
        files:
          './base/static/stylesheets/application.css': './base/assets/stylesheets/application.scss'

    watch:
      css:
        files: '**/*.scss'
        tasks: ['sass']

  # Imports.
  grunt.loadNpmTasks 'grunt-autoprefixer'
  grunt.loadNpmTasks 'grunt-contrib-sass'
  grunt.loadNpmTasks 'grunt-contrib-uglify'
  grunt.loadNpmTasks 'grunt-contrib-watch'

  # Task registration.
  grunt.registerTask 'default', ['sass', 'watch']
