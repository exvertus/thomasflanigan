import logging

from pelican import signals

log = logging.getLogger(__name__)

def page_generator_init_hook(page_generator):
    log.info('break here')

def page_generator_preread_hook(page_generator):
    log.info('break here')

def page_generator_context_hook(page_generator, metadata):
    # This gets called PER PAGE
    log.info('break here')

def page_generator_finalized_hook(page_generator):
    log.info('break here')

def all_generators_finalized_hook(generators):
    log.info('break here')

def article_generator_write_article_hook(article_generator, content):
    log.info('break here')

def article_writer_finalized_hook(article_generator, writer):
    log.info('break here')

def page_generator_write_page_hook(page_generator, content):
    log.info('break here')

def page_writer_finalized_hook(page_generator, writer):
    log.info('break here')

def finalized_hook(pelican):
    log.info('break here')

def register():
    signals.page_generator_context.connect(page_generator_context_hook)
    signals.page_generator_preread.connect(page_generator_preread_hook)
    signals.page_generator_init.connect(page_generator_init_hook)
    signals.page_generator_finalized.connect(page_generator_finalized_hook)
    signals.page_generator_write_page.connect(page_generator_write_page_hook)
    signals.page_writer_finalized.connect(page_writer_finalized_hook)
    signals.all_generators_finalized.connect(all_generators_finalized_hook)
    signals.article_generator_write_article.connect(article_generator_write_article_hook)
    signals.article_writer_finalized.connect(article_writer_finalized_hook)
    signals.finalized.connect(finalized_hook)
    
