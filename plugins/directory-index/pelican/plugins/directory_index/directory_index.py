import logging

from pelican import signals

log = logging.getLogger(__name__)

def page_generator_context_hook():
    log.info('break here')

def page_generator_preread_hook():
    log.info('break here')

def page_generator_init_hook():
    log.info('break here')

def page_generator_finalized_hook():
    log.info('break here')

def page_generator_write_page_hook():
    log.info('break here')

def page_writer_finalized_hook():
    log.info('break here')


def register():
    signals.page_generator_context.connect(page_generator_context_hook)
    signals.page_generator_preread.connect(page_generator_preread_hook)
    signals.page_generator_init.connect(page_generator_init_hook)
    signals.page_generator_finalized.connect(page_generator_finalized_hook)
    signals.page_generator_write_page.connect(page_generator_write_page_hook)
    signals.page_writer_finalized.connect(page_writer_finalized_hook)
    
