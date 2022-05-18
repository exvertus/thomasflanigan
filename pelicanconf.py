from pathlib import Path

# Common settings ---
AUTHOR = 'Tom Flanigan'
SITENAME = 'Tom Flanigan | Material Soul'
SITEURL = 'https://thomasflanigan.com'

PATH = 'content'
# Necessary for now because excludes settings only work on directories and not files.
# TODO: Move this piece to plugin or submit feature to Pelican to support exc files.
poems = tuple(Path(PATH).glob('**/music/poems-lyrics/*.md'))
blog = tuple(Path(PATH).glob('**/tech/blog/*.md'))
ARTICLE_PATHS = [str(p.absolute()) for p in (poems + blog)]
PAGE_PATHS = [str(p.absolute()) for p in Path(PATH).glob('**/*[!index].md')
              if not str(p.absolute()) in ARTICLE_PATHS]
DIRECTORY_INDEX_STEM = 'index'
OUTPUT_PATH = 'output/'
PATH_METADATA = '(?P<path_no_ext>.*)\..*'
ARTICLE_URL = ARTICLE_SAVE_AS = PAGE_URL = PAGE_SAVE_AS = '{path_no_ext}.html'
THEME = './themes/tom'
PLUGINS = ['directory_index']
PLUGIN_PATHS = ['plugins\directory-index\pelican\plugins\directory_index']
STATIC_PATHS = ['images']

TIMEZONE = 'America/Chicago'
DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

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
DIRECT_TEMPLATES = ['categories', 'tags', 'archives']

LOAD_CONTENT_CACHE = False
DELETE_OUTPUT_DIRECTORY = True

USE_FOLDER_AS_CATEGORY = True

# Local-only settings ---
RELATIVE_URLS = True
