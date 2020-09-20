import tplinkrouter
import logging
import voluptuous as vol
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.config_validation import (PLATFORM_SCHEMA)
from homeassistant.const import ( CONF_HOST, CONF_PASSWORD, CONF_USERNAME )
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

def setup_platform(_hass, config, add_entities, _discovery_info=None):
    add_entities([TPLinkPower(config)])

class TPLinkPower(SwitchEntity):
    def __init__(self, config):
        self._unique_id = 'tplink_c50_power'
        self._name = 'TP-Link C50 Power'
        self.router = tplinkrouter.C50(config.get(CONF_HOST),config.get(CONF_USERNAME),config.get(CONF_PASSWORD))

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def state(self):
        if self.router._get('version'):
            return 'on'
        else:
            return 'off'

    @property
    def is_on(self):
        return self.router._get('version')

    @property
    def is_off(self):
        return self.router._get('version')

    def turn_on(self, **kwargs):
        _LOGGER.debug('on')
        self.router._get('version')

    def turn_off(self, **kwargs):
        _LOGGER.debug('off')
        self.router._get('restart')

    @property
    def device_state_attributes(self):
        attrs = {
            'friendly_name': self._name,
            'unique_id': self._unique_id,
        }
        return attrs

    def _activate(self, on_off):
        _LOGGER.debug('toggle')
        self.router._get('restart')
        self.async_schedule_update_ha_state()
    