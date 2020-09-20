import tplinkrouter
import logging
import voluptuous as vol
from homeassistant.components.device_tracker import ( DOMAIN, PLATFORM_SCHEMA, DeviceScanner )
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import ( CONF_HOST, CONF_PASSWORD, CONF_USERNAME, HTTP_HEADER_X_REQUESTED_WITH)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})

async def async_setup_platform(_hass, config, async_add_entities, _discovery_info=None):
    switches = [TPLinkPower(config)]
    async_add_entities(switches, True)

def get_scanner(hass, config):
    router = tplinkrouter.C50(config[DOMAIN][CONF_HOST],config[DOMAIN][CONF_USERNAME],config[DOMAIN][CONF_PASSWORD])
    
    devices = []
    for d in router._get('dhcp_clients').values():
        devices.append(d)

    return devices

class TPLinkPower(SwitchEntity):
    def __init__(self, config):
        self._unique_id = 'tplink_c50_power'
        self._name = 'TP-Link C50 Power'
        self.router = tplinkrouter.C50(config[DOMAIN][CONF_HOST],config[DOMAIN][CONF_USERNAME],config[DOMAIN][CONF_PASSWORD])

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
    