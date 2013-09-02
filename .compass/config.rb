require "compass-normalize"
require "susy"

# Set this to the root of your project when deployed:
http_path = (environment == :production) ? "//hello-base.s3.amazonaws.com/base/" : "/"

css_dir = "static/stylesheets"
fonts_dir = "static/fonts"
images_dir = "static/images"
javascripts_dir = "static/javascripts"
sass_dir = "base/assets/sass"

# output_style = :compressed
# output_style = :compact
output_style = (environment == :production) ? :compressed : :compact

# To disable debugging comments that display the original location of your selectors. Uncomment:
line_comments = false
# line_comments = (environment == :production) ? false : true

# If you prefer the indented syntax, you might want to regenerate this
# project again passing --syntax sass, or you can uncomment this:
# preferred_syntax = :sass
# and then run:
# sass-convert -R --from scss --to sass ranking/static/scss scss && rm -rf sass && mv scss sass
