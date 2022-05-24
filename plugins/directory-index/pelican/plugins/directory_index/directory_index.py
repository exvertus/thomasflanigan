import logging
import os
import types
from pathlib import Path

from pelican.generators import Generator, ArticlesGenerator, PagesGenerator, signals
from pelican.contents import Content
from pelican.readers import Readers
from pelican.utils import DateFormatter

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PrefixLoader

log = logging.getLogger(__name__)

class IndexPage(Content):
    mandatory_properties = tuple()
    allowed_statuses = ('published')
    default_status = 'published'
    default_template = 'index'

    def _expand_settings(self, key):
        klass = 'draft_page' if self.status == 'draft' else None
        return super()._expand_settings(key, klass)

class IndexGenerator(Generator):
    # TODO: Add caching by importing CachingGenerator
    def __init__(self, context, settings, path, theme, output_path, **kwargs):
        # Do not use super init from baseclass generator unless tested... 
        # risks over-sending generator_init signals... 
        # other base methods do not send signals
        self.context = context
        self.settings = settings
        self.path = path
        self.theme = theme
        self.output_path = output_path
        self.file_stem = self.settings.get("DIRECTORY_INDEX_STEM", 'index')
        self.settings['INDEXPAGE_URL'] = self.settings.get("INDEXPAGE_URL", '{path_no_ext}.html')
        self.settings['INDEXPAGE_SAVE_AS'] = self.settings.get("INDEXPAGE_SAVE_AS", '{path_no_ext}.html')
        self.index_pages = []
        self.indexes = {}

        for arg, value in kwargs.items():
            setattr(self, arg, value)

        self.readers = Readers(self.settings)

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
                        context=self.indexes)
                except Exception as e:
                    log.error(
                        'Could not process %s\n%s', index_path, e,
                        exc_info=self.settings.get('DEBUG', False))
                    self._add_failed_source_path(index_path)
                    continue

                if not index_page.is_valid():
                    self._add_failed_source_path(index_path)
                    continue

                self.index_pages.append(index_page)
                self.add_source_path(index_page)
                self.add_static_links(index_page)

        self._update_context(('indexes', ))

    def generate_output(self, writer):
        for index in self.index_pages:
            index_dir = Path(index.relative_dir)
            if not index_dir.parts:
                articles_header = 'All'
            else:
                articles_header = index_dir.parts[-1].capitalize()
            path_to_root = "../" * len(index_dir.parts)
            relative_articles = \
                [article for article in self.context.get('articles', [])
                 if Path(article.save_as).is_relative_to(index_dir)]
            local_pages = \
                [index_page for index_page in self.index_pages
                 if index_page.relative_dir 
                 and Path(index_page.relative_dir).parent == index_dir] \
              + [page for page in self.context['pages']
                 if Path(page.save_as).parent == index_dir]
            writer.write_file(
                name=index.save_as, 
                template=self.get_template(index.template),
                context=self.context,
                template_name='index',
                page=index,
                path_to_root=path_to_root,
                articles=relative_articles,
                articles_header=articles_header,
                local_pages=local_pages,
                relative_urls=self.settings['RELATIVE_URLS'],
                override_output=hasattr(index, 'override_save_as'),
                url=index.url)

def get_generators(pelican):
    return IndexGenerator

def disable_page_writing(generators):
    """
    Disable normal article and page generation.
    The html5up Dimension theme fits better as index pages.
    """
    def generate_output_override(self, writer):
        if isinstance(self, ArticlesGenerator):
            log.debug('Skipping normal article generation...')
        if isinstance(self, PagesGenerator):
            log.debug('Skipping normal pages generation...')

    for generator in generators:
        if isinstance(generator, (ArticlesGenerator, PagesGenerator)):
            generator.generate_output = types.MethodType(generate_output_override, generator)

def register():
    signals.get_generators.connect(get_generators)
    signals.all_generators_finalized.connect(disable_page_writing)
