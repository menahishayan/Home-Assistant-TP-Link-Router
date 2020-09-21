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
    return TPLinkDeviceTracker(config)

class TPLinkDeviceTracker(DeviceScanner):
    def __init__(self,config):
        self.router = tplinkrouter.C50(config[DOMAIN][CONF_HOST],config[DOMAIN][CONF_USERNAME],config[DOMAIN][CONF_PASSWORD])
        self.devices = {}

    def scan_devices(self):
        self.devices = self.router.get_clients_by_mac()
        macs = [d for d in self.devices]
        return macs

    def get_device_name(self, device):
        try:
            return self.devices[device]['hostName']
        except:
            return None


            