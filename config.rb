# Require any additional compass plugins here.
require "autoprefixer-rails"
require "compass-normalize"
require "csso"
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

# Autoprefixer.
on_stylesheet_saved do |file|
    css = File.read(file)
    File.open(file, "w") do |io|
        io << Csso.optimize(AutoprefixerRails.compile(css))
    end
end
