import logging
import os
from pathlib import Path

from pelican import generators, signals
from pelican.contents import Content
from pelican.readers import Readers
from pelican.utils import DateFormatter

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PrefixLoader

log = logging.getLogger(__name__)

class IndexPage(Content):
    mandatory_properties = tuple()
    allowed_statuses = ('published')
    default_status = 'published'
    default_template = 'page'

    def _expand_settings(self, key):
        klass = 'draft_page' if self.status == 'draft' else None
        return super()._expand_settings(key, klass)

class IndexGenerator(generators.Generator):
    # TODO: Add caching by importing CachingGenerator
    def __init__(self, context, settings, path, theme, output_path,
                 readers_cache_name='', **kwargs):
        # Do not use super init from baseclass generator unless tested... 
        # risks over-sending generator_init signals... 
        # other base methods do not send signals
        self.context = context
        self.settings = settings
        self.path = path
        self.theme = theme
        self.output_path = output_path

        for arg, value in kwargs.items():
            setattr(self, arg, value)

        self.readers = Readers(self.settings, readers_cache_name)

        # templates cache
        self._templates = {}
        self._templates_path = list(self.settings['THEME_TEMPLATES_OVERRIDES'])

        theme_templates_path = os.path.expanduser(
            os.path.join(self.theme, 'templates'))
        self._templates_path.append(theme_templates_path)
        theme_loader = FileSystemLoader(theme_templates_path)

        simple_theme_path = os.path.dirname(os.path.abspath(__file__))
        simple_loader = FileSystemLoader(
            os.path.join(simple_theme_path, "themes", "simple", "templates"))

        self.env = Environment(
            loader=ChoiceLoader([
                FileSystemLoader(self._templates_path),
                simple_loader,  # implicit inheritance
                PrefixLoader({
                    '!simple': simple_loader,
                    '!theme': theme_loader
                })  # explicit ones
            ]),
            **self.settings['JINJA_ENVIRONMENT']
        )

        log.debug('Template list: %s', self.env.list_templates())

        # provide utils.strftime as a jinja filter
        self.env.filters.update({'strftime': DateFormatter()})

        # get custom Jinja filters from user settings
        custom_filters = self.settings['JINJA_FILTERS']
        self.env.filters.update(custom_filters)

        # get custom Jinja globals from user settings
        custom_globals = self.settings['JINJA_GLOBALS']
        self.env.globals.update(custom_globals)

        # get custom Jinja tests from user settings
        custom_tests = self.settings['JINJA_TESTS']
        self.env.tests.update(custom_tests)

        self.file_stem = self.settings.get("DIRECTORY_INDEX_STEM", 'index')
        self.settings['INDEXPAGE_URL'] = self.settings.get("INDEXPAGE_URL", '{path_no_ext}.html')
        self.settings['INDEXPAGE_SAVE_AS'] = self.settings.get("INDEXPAGE_SAVE_AS", '{path_no_ext}.html')
        self.index_pages = {}

    def generate_context(self):
        """
        Find all index.{ext} files in content folder
        Add them to self.context['generated_content'] 
        Careful: context dict ref shared globally between generators
        """
        for ext in self.readers.extensions:
            glob_pattern = f"**/*{self.settings['DIRECTORY_INDEX_STEM']}.{ext}"
            ext_indexes = Path(self.settings['PATH']).glob(glob_pattern)
            for index_path in ext_indexes:
                try:
                    index_page = self.readers.read_file(
                        base_path=self.path, 
                        path=index_path, 
                        content_class=IndexPage,
                        context=self.index_pages,
                        preread_signal=None,
                        preread_sender=self,
                        context_signal=None,
                        context_sender=self)
                except Exception as e:
                    log.error(
                        'Could not process %s\n%s', index_path, e,
                        exc_info=self.settings.get('DEBUG', False))
                    self._add_failed_source_path(index_path)
                    continue

                if not index_page.is_valid():
                    self._add_failed_source_path(index_path)
                    continue

                self.add_source_path(index_page)

    def generate_output(self, writer):
        log.info('break here')

def get_generators(pelican):
    return IndexGenerator

def register():
    signals.get_generators.connect(get_generators)
