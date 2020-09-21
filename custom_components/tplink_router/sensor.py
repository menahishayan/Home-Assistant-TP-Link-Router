import tplinkrouter
import logging
import re
import voluptuous as vol
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.config_validation import (PLATFORM_SCHEMA)
from homeassistant.const import ( CONF_HOST, CONF_PASSWORD, CONF_USERNAME)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_HOST = "host"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})

async def async_setup_platform(_hass, config, async_add_entities, _discovery_info=None):
    router = tplinkrouter.C50(config.get(CONF_HOST),config.get(CONF_USERNAME),config.get(CONF_PASSWORD))
    sensors = []
    for d in router.get_clients().values():
        sensors.append(TPLinkClient(router,d))
    async_add_entities(sensors)

class TPLinkClient(Entity):
    """TP-Link Router Client Sensor"""
    def __init__(self, router,device):
        self.router = router
        self.device = device
        self._unique_id = device['hostName'].lower().replace('-','_') + '_ip'
        self._name = device['hostName']
        self._icon = 'mdi:devices'
        self._state = 'Not Connected'
       
    @property
    def unique_id(self):
        return self._unique_id

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        return self._state

    def update(self):
        try:
            clients = self.router.get_clients()
            self._state = clients[self.device['hostName']]['IPAddress']
        except:
            self._state = 'Not Connected'

    @property
    def device_state_attributes(self):
        return {
            'friendly_name': self._name,
            'unique_id': self._unique_id,
            'icon': self._icon
        }
    