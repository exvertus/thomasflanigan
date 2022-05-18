import logging
import os

from pelican import generators, signals
from pelican.readers import Readers
from pelican.utils import DateFormatter

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PrefixLoader

log = logging.getLogger(__name__)

class IndexGenerator:
    def __init__(self, context, settings, path, theme, output_path,
                 readers_cache_name='', **kwargs):
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

        self.file_stem = self.settings.get("DIRECTORY_INDEX_STEM")
        log.info('break here')

    def generate_context(self):
        """
        Find all index.{ext} files in content folder
        and add them to self.pages
        """
        log.info('break here')

    def generate_output(self, writer):
        log.info('break here')

def get_generators(pelican):
    return IndexGenerator

def register():
    signals.get_generators.connect(get_generators)
