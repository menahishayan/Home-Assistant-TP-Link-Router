import tplinkrouter
import logging
import re
import voluptuous as vol
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.config_validation import (PLATFORM_SCHEMA)
from homeassistant.const import ( CONF_HOST, CONF_PASSWORD, CONF_USERNAME)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})

def setup_platform(_hass, config, add_entities, _discovery_info=None):
    router = tplinkrouter.C50(config.get(CONF_HOST),config.get(CONF_USERNAME),config.get(CONF_PASSWORD),_LOGGER)
    sensors = []
    for d in router.get_clients().values():
        sensors.append(TPLinkClient(router,d,_hass))
    add_entities(sensors)

class TPLinkClient(Entity):
    """TP-Link Router Client Sensor"""
    def __init__(self, router,device,hass):
        self.router = router
        self.device = device
        self._unique_id = device['hostName'].lower().replace('-','_') + '_ip'
        self._name = device['hostName']
        self._icon = 'mdi:devices'
        self._state = 'Not Connected'
        self.hass = hass
       
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

    async def async_update(self):
        try:
            clients = await self.hass.async_add_executor_job(self.router.get_clients)
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
    