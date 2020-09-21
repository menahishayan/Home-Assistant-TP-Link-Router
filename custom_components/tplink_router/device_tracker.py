import tplinkrouter
import logging
import re
import voluptuous as vol
from homeassistant.components.device_tracker import (
    DOMAIN, PLATFORM_SCHEMA, DeviceScanner)
from homeassistant.helpers.config_validation import (PLATFORM_SCHEMA)
from homeassistant.const import ( CONF_HOST, CONF_PASSWORD, CONF_USERNAME)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_HOST = "host"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_CONSIDER_HOME = "consider_home"
CONF_NEW_DEVICE_DEFAULTS = "new_device_defaults"
CONF_TRACK_NEW = "track_new_devices"
DEFAULT_CONSIDER_HOME = 180
DEFAULT_TRACK_NEW = True

NEW_DEVICE_DEFAULTS_SCHEMA = vol.Any(
    None,
    vol.Schema({vol.Optional(CONF_TRACK_NEW, default=DEFAULT_TRACK_NEW): cv.boolean}),
)
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Optional(CONF_CONSIDER_HOME, default=DEFAULT_CONSIDER_HOME): vol.All(
            cv.time_period, cv.positive_timedelta
        ),
    vol.Optional(CONF_NEW_DEVICE_DEFAULTS, default={}): NEW_DEVICE_DEFAULTS_SCHEMA,
})

# async def async_setup_platform(_hass, config, async_add_entities, _discovery_info=None):
#     router = tplinkrouter.C50(config.get(CONF_HOST),config.get(CONF_USERNAME),config.get(CONF_PASSWORD))
#     sensors = [TPLinkDeviceTracker(router)]
#     async_add_entities(sensors)

def get_scanner(hass, config):
    router = tplinkrouter.C50(config.get(CONF_HOST),config.get(CONF_USERNAME),config.get(CONF_PASSWORD))
    return TPLinkDeviceTracker(router)

class TPLinkDeviceTracker(DeviceScanner):
    def __init__(self,router):
        self.router = router