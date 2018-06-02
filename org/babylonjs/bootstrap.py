import logging
from org.transcrypt.stubs.browser import __pragma__
# todo -- replace with symbol pragma


__pragma__('ifndef', 'release')
logging.basicConfig(level=logging.DEBUG)
__pragma__('else')
logging.basicConfig(level=logging.WARNING)
__pragma__('endif')


logging.getLogger(__name__).debug('starting babylon api')

