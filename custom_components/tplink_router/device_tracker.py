import tplinkrouter
import logging
import voluptuous as vol
from homeassistant.components.device_tracker import (DOMAIN, PLATFORM_SCHEMA, DeviceScanner)
from homeassistant.const import ( CONF_HOST, CONF_PASSWORD, CONF_USERNAME)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})

def get_scanner(hass, config):
    return TPLinkDeviceTracker(config,hass)

class TPLinkDeviceTracker(DeviceScanner):
    def __init__(self,config,hass):
        self.router = tplinkrouter.C50(config[DOMAIN][CONF_HOST],config[DOMAIN][CONF_USERNAME],config[DOMAIN][CONF_PASSWORD],_LOGGER)
        self._unique_id = self.router.__name__.lower().replace(' ','_') + '_device_tracker'
        self._name = self.router.__name__ + ' Device Tracker'
        self.devices = {}
        self.hass = hass

    def scan_devices(self):
        self.hass.loop.create_task(self.async_device_scanner)
        macs = [d for d in self.devices]
        return macs

    async def async_device_scanner(self):
        self.devices = self.router.get_clients_by_mac()
        
    async def get_device_name(self, device):
        if device in self.devices:
            return self.devices[device]['hostName']
        else:
            return device

    async def get_extra_attributes(self, device):
        if device in self.devices:
            return {
                'host_name': self.devices[device]['hostName'],
                'mac_address': device,
                'ip_address': self.devices[device]['IPAddress'],
            }
        else:
            return None



            