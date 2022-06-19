from pathlib import Path
from datetime import datetime

# Common settings ---
AUTHOR = 'Tom Flanigan'
SITENAME = 'Tom Flanigan'
SITEURL = 'https://thomasflanigan.com'
FIRST_YEAR = '2020'
END_YEAR = datetime.now().year
TIMEZONE = 'America/Chicago'
DEFAULT_LANG = 'en'

PATH = 'content'
# Necessary for now because excludes settings only work on directories and not files.
# TODO: Move this piece to plugin or submit feature to Pelican to support exc files.
poems = tuple(Path(PATH).glob('**/music/poems-lyrics/*.md'))
blog = tuple(Path(PATH).glob('**/tech/blog/*.md'))
ARTICLE_PATHS = [p.absolute() for p in (poems + blog)]
DIRECTORY_INDEX_STEM = 'index'
PAGE_PATHS = [p.absolute() for p in Path(PATH).glob('**/*.md')
              if (p.stem != DIRECTORY_INDEX_STEM and p.absolute() not in ARTICLE_PATHS)]
OUTPUT_PATH = 'output/'
PATH_METADATA = '(?P<path_no_ext>.*)\..*'
ARTICLE_URL = ARTICLE_SAVE_AS = PAGE_URL = PAGE_SAVE_AS = '{path_no_ext}.html'
STATIC_PATHS = ['images']

THEME = './themes/tom'
THEME_STATIC_DIR = '.'
THEME_STATIC_PATHS = ['static']

PLUGINS = ['directory_index', 'jinja2content']
PLUGIN_PATHS = [Path('plugins/directory-index/pelican/plugins/directory_index')]
JINJA2CONTENT_TEMPLATES = [Path(PATH, '_templates').absolute()]

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

QUICKLINKS = (
    ('Instagram', 'https://www.instagram.com/material_soul/'),
    ('Etsy', 'https://www.etsy.com/shop/MaterialSoulArt'),
    ('Deviant Art', 'https://www.deviantart.com/material-soul'),
    ('Twitter', 'https://twitter.com/Material__Soul'),
    ('Tumblr', 'https://www.tumblr.com/blog/material-soul'),
    ('Facebook', 'https://www.facebook.com/materialsoul'),
    ('Bandcamp', 'https://materialsoul.bandcamp.com/'),
    ('Github', 'https://github.com/exvertus/'),
    ('LinkedIn','https://www.linkedin.com/in/thomas-flanigan/'),)
QUICKLINKS_SAVE_AS = 'quicklinks.html'
QUICKLINKS_HEADER = 'Links'

DEFAULT_PAGINATION = False
DEFAULT_DATE_FORMAT = '%d %b %Y'

DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
DIRECT_TEMPLATES = []

LOAD_CONTENT_CACHE = False
DELETE_OUTPUT_DIRECTORY = True

USE_FOLDER_AS_CATEGORY = True

GITHUB_REPO_URL = "https://github.com/exvertus/thomasflanigan/"

# Local-only settings ---
RELATIVE_URLS = True
