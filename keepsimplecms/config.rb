# Require any additional compass plugins here.

# Set this to the root of your project when deployed:
http_path = "/"

# CSS
css_dir = "static/css"
http_stylesheets_path = http_path + "static/css"

# SCSS
sass_dir = "static/scss"

# Images
images_dir = "static/images"
http_images_path = http_path + "static/images"

# Generated Images
generated_images_dir = "static/sprites"
http_generated_images_path = http_path + "static/sprites"

# Javascript
javascripts_dir = "static/js"
http_javascripts_path = http_path + "static/js"

# You can select your preferred output style here (can be overridden via the command line):
# output_style = :expanded or :nested or :compact or :compressed
output_style = (environment == :production) ? :compressed : :expanded

# To enable relative paths to assets via compass helper functions. Uncomment:
# relative_assets = true

# To disable debugging comments that display the original location of your selectors. Uncomment:
# line_comments = false
line_comments = (environment != :production)

# sprites: generation speed over file size in development
chunky_png_options = (environment == :production) ? :best_compression : :fast_rgba

require 'compass_twitter_bootstrap'

# If you prefer the indented syntax, you might want to regenerate this
# project again passing --syntax sass, or you can uncomment this:
# preferred_syntax = :sass
# and then run:
# sass-convert -R --from scss --to sass static/sass scss && rm -rf sass && mv scss sass
