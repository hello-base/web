# Require any additional compass plugins here.
require "compass-normalize"
require "susy"

# Set this to the root of your project when deployed:
http_path = "/"
css_dir = "base/static/stylesheets"
sass_dir = "base/assets/stylesheets"
images_dir = "base/static/images"
javascripts_dir = "base/static/javascripts"
fonts_dir = "static/fonts"

output_style = (environment == :production) ? :compressed : :compact

# To enable relative paths to assets via compass helper functions. Uncomment:
# relative_assets = true

# To disable debugging comments that display the original location of your selectors. Uncomment:
line_comments = false


# If you prefer the indented syntax, you might want to regenerate this
# project again passing --syntax sass, or you can uncomment this:
# preferred_syntax = :sass
# and then run:
# sass-convert -R --from scss --to sass ranking/static/scss scss && rm -rf sass && mv scss sass
