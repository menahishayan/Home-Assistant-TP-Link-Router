"""TP-Link Archer C50"""

import logging

__version__ = '0.1.0'

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'momentary'

def setup(_hass, _config):
    _LOGGER.debug('setup')
    return True