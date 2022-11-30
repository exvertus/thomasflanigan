from pathlib import Path

# Common settings ---
AUTHOR = 'Tom Flanigan'
SITENAME = 'Tom Flanigan'
SITEURL = 'https://thomasflanigan.com'
SITESUBTITLE = "Art, Music, Tech"
TIMEZONE = 'America/Chicago'
DEFAULT_LANG = 'en'

PATH = 'content'
ARTICLE_PATHS = [p.absolute() for p in Path(PATH).glob('**/articles/*.md')]
PAGE_PATHS = [p.absolute() for p in Path(PATH).glob('**/pages/*.md')]
OUTPUT_PATH = 'output/'
# PATH_METADATA = '(?P<path_no_ext>.*)\..*'
STATIC_PATHS = ['images']

THEME = './themes/html5up-massively'
THEME_STATIC_DIR = '.'
THEME_STATIC_PATHS = ['static']
FEATURED_ARTICLE = -1

PLUGINS = ['jinja2content']
JINJA2CONTENT_TEMPLATES = [Path(PATH, '_templates').absolute()]

# Feeds
FEED_DOMAIN = SITEURL
FEED_RSS = 'feeds/all.rss.xml'
FEED_ALL_RSS = FEED_ALL_ATOM = CATEGORY_FEED_ATOM = None
AUTHOR_FEED_RSS = TRANSLATION_FEED_ATOM = AUTHOR_FEED_ATOM = None

SOCIAL = (
    # ('Deviant Art', 'https://www.deviantart.com/material-soul'),
    # ('Twitter', 'https://twitter.com/Material__Soul'),
    # ('Tumblr', 'https://www.tumblr.com/blog/material-soul'),
    # ('Facebook', 'https://www.facebook.com/materialsoul'),
    ('Bandcamp', 'https://materialsoul.bandcamp.com/'),
    ('Github', 'https://github.com/exvertus/'),
    ('LinkedIn','https://www.linkedin.com/in/thomas-flanigan/'),
    ('Instagram', 'https://www.instagram.com/material_soul/'),)

DEFAULT_DATE_FORMAT = '%d %b %Y'
DEFAULT_PAGINATION = False

LOAD_CONTENT_CACHE = False
DELETE_OUTPUT_DIRECTORY = True

GITHUB_REPO_URL = "https://github.com/exvertus/thomasflanigan/"

# Local-only settings ---
RELATIVE_URLS = True
