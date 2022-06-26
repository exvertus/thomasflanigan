import logging
import os
import types
from pathlib import Path

from pelican.generators import Generator, ArticlesGenerator, PagesGenerator, signals
from pelican.contents import Content
from pelican.readers import Readers
from pelican.utils import (DateFormatter, order_content)

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

    def get_path(self):
        self.index_dir = Path(self.relative_dir)

    def get_article_header(self):
        if self.metadata.get("articles_header", ''):
            return self.metadata.get("articles_header")
        elif not self.index_dir.parts:
            return 'All Articles'
        else:
            return  f"{self.index_dir.parts[-1].capitalize()} Articles"

    def page_belongs(self, page):
        """
        True if page is a supported sub-dir of this index
        """
        log.info('break here')

    def article_belongs(self, article):
        """
        True if article is a supported sub-dir of this index
        """
        log.info('break here')

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
        self.articles_gen = None
        self.pages_gen = None
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
        """
        For each index page, generate index.html with 
        articles and pages at the same depth.
        """
        all_articles = self.context.get('articles', [])
        # Need to ensure index pages are sorted shallow to deep
        self.index_pages.sort(key=lambda inx : len(Path(inx.relative_dir).parts))
        for index in self.index_pages:
            index.get_path()
            articles_header = index.get_article_header()
            path_to_root = "../" * len(index.index_dir.parts)
            relative_articles = []
            for article in all_articles:
                if index.article_belongs(article):
                    # fix save_as still
                    relative_articles.append(article)
            local_indexes = \
                [index_page for index_page in self.index_pages
                 if index_page.relative_dir 
                 and Path(index_page.relative_dir).parent == index.index_dir]
            local_pages = \
                [page for page in self.context['pages']
                 if Path(page.save_as).parent == index.index_dir]
            for each_list in (local_indexes, local_pages):
                each_list.sort(key=lambda page: page.title)
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
                local_indexes=local_indexes,
                relative_urls=self.settings['RELATIVE_URLS'],
                override_output=hasattr(index, 'override_save_as'),
                url=index.url)
        if self.settings.get('QUICKLINKS', None):
            writer.write_file(
                name=self.settings.get('QUICKLINKS_SAVE_AS', 'quicklinks.html'),
                template=self.get_template('quicklinks'),
                path_to_root='/',
                context=self.context,
                template_name='quicklinks',
                url=self.settings.get('QUICKLINKS_SAVE_AS', 'quicklinks.html'),
                links_header=self.settings.get('QUICKLINKS_HEADER', 'Links'),
            )
        self.articles_gen.generate_feeds(writer)

def get_generators(pelican):
    return IndexGenerator

def disable_page_writing(generators):
    """
    Disable normal article and page generation.
    The html5up Dimension theme fits better as index pages.
    """
    def generate_output_override(self, _):
        pass

    for generator in generators:
        if isinstance(generator, IndexGenerator):
            index_gen = generator
            break

    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            index_gen.articles_gen = generator
            generator.generate_output = types.MethodType(generate_output_override, generator)
            log.debug('Skipping normal article generation...')
        if isinstance(generator, PagesGenerator):
            index_gen.pages_gen = generator
            generator.generate_output = types.MethodType(generate_output_override, generator)
            log.debug('Skipping normal pages generation...')

def register():
    signals.get_generators.connect(get_generators)
    signals.all_generators_finalized.connect(disable_page_writing)
