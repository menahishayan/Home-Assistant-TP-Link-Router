import tplinkrouter
import logging
import voluptuous as vol
from homeassistant.components.device_tracker import (
    DOMAIN, PLATFORM_SCHEMA, DeviceScanner, CONF_TRACK_NEW)
from homeassistant.helpers.config_validation import (PLATFORM_SCHEMA)
from homeassistant.const import ( CONF_HOST, CONF_PASSWORD, CONF_USERNAME  )
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_HOST = "host"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_CONSIDER_HOME = "consider_home"
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

async def async_setup_platform(_hass, config, async_add_entities, _discovery_info=None):
    router = tplinkrouter.C50(config.get(CONF_HOST),config.get(CONF_USERNAME),config.get(CONF_PASSWORD))
    sensors = [TPLinkDeviceTracker(router)]
    async_add_entities(sensors)

class TPLinkDeviceTracker(DeviceScanner):
    """TP-Link Router Client Sensor"""
    def __init__(self, router):
        self.router = router
        self._unique_id = router.__name__.lower().replace(" ", "_") + '_device_tracker'
        self._name = router.__name__ + ' Device Tracker'
        self._icon = 'mdi:devices'

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def scan_devices(self):
        try:
            clients = self.router.get_clients_by_mac()
            return clients.keys()
        except:
            return []

    def get_device_name(self, device):
        try:
            clients = self.router.get_clients_by_mac()
            for c in clients.values():
                if c['MACAddress'] == device:
                    return c['hostName']
            
        except:
            return None

    @property
    def device_state_attributes(self):
        return {
            'friendly_name': self._name,
            'unique_id': self._unique_id,
            'icon': self._icon
        }
    