# Common settings ---
AUTHOR = 'Tom Flanigan'
SITENAME = 'Tom Flanigan | Material Soul'
SITEURL = 'https://thomasflanigan.com'

PATH = 'content'
PAGE_PATHS = ['.']
ARTICLE_PATHS = ['tech/blog', 'music/poems-lyrics']
OUTPUT_PATH = 'output/'
THEME = './themes/tom'
PLUGINS = None
PLUGIN_PATHS = []
STATIC_PATHS = ['images']

TIMEZONE = 'America/Chicago'
DEFAULT_LANG = 'English'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (('Art', '/art'),
#          ('Music', '/music'),
#          ('Tech', '/tech'),)

# Social widget
SOCIAL = (('Instagram', 'https://www.instagram.com/tomisdrawingagain/'),
          ('Bandcamp', 'https://materialsoul.bandcamp.com/'),
          ('Github', 'https://github.com/exvertus/'),
          ('LinkedIn','https://www.linkedin.com/in/thomas-flanigan/'))

DEFAULT_PAGINATION = False
DEFAULT_DATE_FORMAT = '%d %b %Y'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
DIRECT_TEMPLATES = ['index', 'categories', 'tags', 'archives']

# YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'
LOAD_CONTENT_CACHE = False
DELETE_OUTPUT_DIRECTORY = True

USE_FOLDER_AS_CATEGORY = True

AUTHOR_SAVE_AS = 'author/{slug}.html'

# Local-only settings ---
RELATIVE_URLS = True
