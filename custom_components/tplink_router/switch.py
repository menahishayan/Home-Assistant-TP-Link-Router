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

def async_setup_platform(_hass, config, async_add_entities, _discovery_info=None):
    router = tplinkrouter.C50(config.get(CONF_HOST),config.get(CONF_USERNAME),config.get(CONF_PASSWORD))
    switches = [
        TPLinkPower(router),
        TPLink24Band(router),
        TPLink5Band(router),
        TPLinkWAN(router)
    ]
    async_add_entities(switches)

class TPLinkPower(SwitchEntity):
    """TP-Link Router Power Switch"""
    def __init__(self, router):
        self.router = router
        self._unique_id = router.__name__.lower().replace(" ", "_")
        self._name = router.__name__
        self._icon = 'mdi:router-wireless'

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def state(self):
        return 'on' if self.router.is_on() else 'off'

    @property
    def is_on(self):
        return self.router.is_on()

    @property
    def is_off(self):
        return not self.router.is_on()

    def turn_on(self, **kwargs):
        self.router.is_on()
        self.async_schedule_update_ha_state()

    def turn_off(self, **kwargs):
        self.router.restart()
        self.async_schedule_update_ha_state()

    @property
    def device_state_attributes(self):
        self.router.logout()
        return {
            'friendly_name': self._name,
            'unique_id': self._unique_id,
            'icon': self._icon
        }
    
class TPLink24Band(SwitchEntity):
    """TP-Link Router 2.4GHz Switch"""
    def __init__(self, router):
        self.router = router
        self._unique_id = router.__name__.lower().replace(" ", "_") + '_24ghz'
        self._name = router.__name__ + ' 2.4GHz'
        self._icon = 'mdi:wifi'

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def state(self):
        return 'on' if self.router._get('bands')['[1,1,0,0,0,0]0']['enable'] == '1' else 'off'

    @property
    def is_on(self):
        return self.router._get('bands')['[1,1,0,0,0,0]0']['enable'] == '1'

    @property
    def is_off(self):
        return not self.router._get('bands')['[1,1,0,0,0,0]0']['enable'] == '1'

    def turn_on(self, **kwargs):
        self.router.set_band('2.4GHz',True)
        self._icon = 'mdi:wifi'
        self.async_schedule_update_ha_state()

    def turn_off(self, **kwargs):
        self.router.set_band('2.4GHz',False)
        self._icon = 'mdi:wifi-off'
        self.async_schedule_update_ha_state()

    @property
    def device_state_attributes(self):
        self.router.logout()
        return {
            'friendly_name': self._name,
            'unique_id': self._unique_id,
            'icon': self._icon
        }
    
class TPLink5Band(SwitchEntity):
    """TP-Link Router 5GHz Switch"""
    def __init__(self, router):
        self.router = router
        self._unique_id = router.__name__.lower().replace(" ", "_") + '_5ghz'
        self._name = router.__name__ + ' 5GHz'
        self._icon = 'mdi:wifi'

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def state(self):
        return 'on' if self.router._get('bands')['[1,2,0,0,0,0]0']['enable'] == '1' else 'off'

    @property
    def is_on(self):
        return self.router._get('bands')['[1,2,0,0,0,0]0']['enable'] == '1'

    @property
    def is_off(self):
        return not self.router._get('bands')['[1,2,0,0,0,0]0']['enable'] == '1'

    def turn_on(self, **kwargs):
        self.router.set_band('5GHz',True)
        self._icon = 'mdi:wifi'
        self.async_schedule_update_ha_state()

    def turn_off(self, **kwargs):
        self.router.set_band('5GHz',False)
        self._icon = 'mdi:wifi-off'
        self.async_schedule_update_ha_state()

    @property
    def device_state_attributes(self):
        self.router.logout()
        return {
            'friendly_name': self._name,
            'unique_id': self._unique_id,
            'icon': self._icon
        }
    
class TPLinkWAN(SwitchEntity):
    """TP-Link WAN Connection Switch"""
    def __init__(self, router):
        self.router = router
        self._unique_id = router.__name__.lower().replace(" ", "_") + '_wan'
        self._name = router.__name__ + ' WAN'
        self._icon = 'mdi:wan'

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def state(self):
        return 'on' if self.router._get('wan')['[1,1,1,0,0,0]0']['connectionStatus'] == 'Connected' else 'off'

    @property
    def is_on(self):
        return self.router._get('wan')['[1,1,1,0,0,0]0']['connectionStatus'] == 'Connected'

    @property
    def is_off(self):
        return not self.router._get('wan')['[1,1,1,0,0,0]0']['connectionStatus'] == 'Connected'

    def turn_on(self, **kwargs):
        self.router._set('wan', [{}, {'[WAN_PPP_CONN#1,1,1,0,0,0#0,0,0,0,0,0]1,19': {'enable': '1'}}, {}])
        self.async_schedule_update_ha_state()

    def turn_off(self, **kwargs):
        self.router._set('wan', [{}, {'[WAN_PPP_CONN#1,1,1,0,0,0#0,0,0,0,0,0]1,19': {'enable': '0'}}])
        self.async_schedule_update_ha_state()

    @property
    def device_state_attributes(self):
        self.router.logout()
        return {
            'friendly_name': self._name,
            'unique_id': self._unique_id,
            'icon': self._icon
        }
    