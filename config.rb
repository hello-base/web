# Require any additional compass plugins here.
require "susy"

http_path = "/"
css_dir = "static/stylesheets"
sass_dir = "base/assets/stylesheets"
images_dir = "static/images"
javascripts_dir = "static/javascripts"
fonts_dir = "static/fonts"

# Output options.
line_comments = false
output_style = (environment == :production) ? :compressed : :compact
