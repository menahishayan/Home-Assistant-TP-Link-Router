"""TP-Link Archer C50"""

import logging

__version__ = '1.0.2'

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'tplink_router'

def setup(_hass, _config):
    _LOGGER.debug('setup')
    return True
