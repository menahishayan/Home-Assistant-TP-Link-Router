import tplinkrouter
import logging
import voluptuous as vol
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.config_validation import (PLATFORM_SCHEMA)
from homeassistant.const import ( CONF_HOST, CONF_PASSWORD, CONF_USERNAME )
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})

async def async_setup_platform(_hass, config, async_add_entities, _discovery_info=None):
    router = tplinkrouter.C50(config.get(CONF_HOST),config.get(CONF_USERNAME),config.get(CONF_PASSWORD),_LOGGER)
    switches = [
        TPLinkPower(router,_hass),
        TPLink24Band(router,_hass),
        TPLink5Band(router,_hass),
        TPLinkWAN(router,_hass)
    ]
    async_add_entities(switches)

class TPLinkPower(SwitchEntity):
    """TP-Link Router Power Switch"""
    async def __init__(self, router,hass):
        self.router = router
        self._unique_id = router.__name__.lower().replace(" ", "_")
        self._name = router.__name__
        self._icon = 'mdi:router-wireless'
        self._state = False
        self.hass = hass

    @property
    async def unique_id(self):
        return self._unique_id

    @property
    async def state(self):
        await self.hass.async_add_executor_job(self.update)
        return 'on' if self._state else 'off'

    @property
    async def is_on(self):
        await self.hass.async_add_executor_job(self.update)
        return self._state

    @property
    async def is_off(self):
        await self.hass.async_add_executor_job(self.update)
        return not self._state

    async def update(self):
        self._state = await self.router.is_on()

    async def turn_on(self, **kwargs):
        self.async_schedule_update_ha_state()

    async def turn_off(self, **kwargs):
        await self.router.restart()
        self.async_schedule_update_ha_state()

    @property
    async def device_state_attributes(self):
        return {
            'friendly_name': self._name,
            'unique_id': self._unique_id,
            'icon': self._icon
        }
    
class TPLink24Band(SwitchEntity):
    """TP-Link Router 2.4GHz Switch"""
    async def __init__(self, router):
        self.router = router
        self._unique_id = router.__name__.lower().replace(" ", "_") + '_24ghz'
        self._name = router.__name__ + ' 2.4GHz'
        self._icon = 'mdi:wifi'
        self._state = False

    @property
    async def unique_id(self):
        return self._unique_id

    @property
    async def state(self):
        await self.hass.async_add_executor_job(self.update)
        return 'on' if self._state else 'off'

    @property
    async def is_on(self):
        await self.hass.async_add_executor_job(self.update)
        return self._state

    @property
    async def is_off(self):
        await self.hass.async_add_executor_job(self.update)
        return not self._state

    async def update(self):
        self._state = await self.router._get('bands')['[1,1,0,0,0,0]0']['enable'] == '1'

    async def turn_on(self, **kwargs):
        await self.router.set_band('2.4GHz',True)
        self._icon = 'mdi:wifi'
        self.async_schedule_update_ha_state()

    async def turn_off(self, **kwargs):
        await self.router.set_band('2.4GHz',False)
        self._icon = 'mdi:wifi-off'
        self.async_schedule_update_ha_state()

    @property
    async def device_state_attributes(self):
        return {
            'friendly_name': self._name,
            'unique_id': self._unique_id,
            'icon': self._icon
        }
    
class TPLink5Band(SwitchEntity):
    """TP-Link Router 5GHz Switch"""
    async def __init__(self, router):
        self.router = router
        self._unique_id = router.__name__.lower().replace(" ", "_") + '_5ghz'
        self._name = router.__name__ + ' 5GHz'
        self._icon = 'mdi:wifi'
        self._state = False

    @property
    async def unique_id(self):
        return self._unique_id

    @property
    async def state(self):
        await self.hass.async_add_executor_job(self.update)
        return 'on' if self._state else 'off'

    @property
    async def is_on(self):
        await self.hass.async_add_executor_job(self.update)
        return self._state

    @property
    async def is_off(self):
        await self.hass.async_add_executor_job(self.update)
        return not self._state

    async def update(self):
        self._state = await self.router._get('bands')['[1,2,0,0,0,0]0']['enable'] == '1'

    async def turn_on(self, **kwargs):
        await self.router.set_band('5GHz',True)
        self._icon = 'mdi:wifi'
        self.async_schedule_update_ha_state()

    async def turn_off(self, **kwargs):
        await self.router.set_band('5GHz',False)
        self._icon = 'mdi:wifi-off'
        self.async_schedule_update_ha_state()

    @property
    async def device_state_attributes(self):
        return {
            'friendly_name': self._name,
            'unique_id': self._unique_id,
            'icon': self._icon
        }
    
class TPLinkWAN(SwitchEntity):
    """TP-Link WAN Connection Switch"""
    async def __init__(self, router):
        self.router = router
        self._unique_id = router.__name__.lower().replace(" ", "_") + '_wan'
        self._name = router.__name__ + ' WAN'
        self._icon = 'mdi:wan'
        self._state = False

    @property
    async def unique_id(self):
        return self._unique_id

    @property
    async def state(self):
        await self.hass.async_add_executor_job(self.update)
        return 'on' if self._state else 'off'

    @property
    async def is_on(self):
        await self.hass.async_add_executor_job(self.update)
        return self._state

    @property
    async def is_off(self):
        await self.hass.async_add_executor_job(self.update)
        return not self._state

    async def update(self):
        self._state = await self.router._get('wan')['[1,1,1,0,0,0]0']['connectionStatus'] == 'Connected'

    async def turn_on(self, **kwargs):
        await self.router._set('wan', [{}, {'[WAN_PPP_CONN#1,1,1,0,0,0#0,0,0,0,0,0]1,19': {'enable': '1'}}, {}])
        self.async_schedule_update_ha_state()

    async def turn_off(self, **kwargs):
        await self.router._set('wan', [{}, {'[WAN_PPP_CONN#1,1,1,0,0,0#0,0,0,0,0,0]1,19': {'enable': '0'}}])
        self.async_schedule_update_ha_state()

    @property
    async def device_state_attributes(self):
        return {
            'friendly_name': self._name,
            'unique_id': self._unique_id,
            'icon': self._icon
        }
    