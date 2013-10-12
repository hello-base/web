# Require any additional compass plugins here.
require "compass-normalize"
require "susy"

http_path = "/"
css_dir = "base/static/stylesheets"
sass_dir = "base/assets/stylesheets"
images_dir = "base/static/images"
javascripts_dir = "base/static/javascripts"
fonts_dir = "static/fonts"

# Output options.
line_comments = false
output_style = (environment == :production) ? :compressed : :compact
