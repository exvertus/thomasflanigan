import logging

from pelican import signals

log = logging.getLogger(__name__)

def sanity_check(sender):
    print('sanity check passed')

def register():
    signals.initialized.connect(sanity_check)
