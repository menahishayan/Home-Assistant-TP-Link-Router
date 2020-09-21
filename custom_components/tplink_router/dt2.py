import tplinkrouter
import logging
import re
import voluptuous as vol
from homeassistant.components.device_tracker import (
    DOMAIN, PLATFORM_SCHEMA, DeviceScanner)
from homeassistant.const import ( CONF_HOST, CONF_PASSWORD, CONF_USERNAME)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})

def get_scanner(hass, config):
    router = tplinkrouter.C50(config.get(CONF_HOST),config.get(CONF_USERNAME),config.get(CONF_PASSWORD))
    return TPLinkDeviceTracker(router)

class TPLinkDeviceTracker(DeviceScanner):
    def __init__(self,router):
        self.router = router
        self.last_results = {}
        self.update()

    def scan_devices(self):
        return self.last_results

    def get_device_name(self, device):
        return None

    def get_extra_attributes(self,device):
        return None

    def update(self):
        try:
            clients = self.router.get_clients_by_mac()
            macs = []

            for c in clients:
                macs.append(c.replace(':','_'))

            self.last_results = macs
            return True
        except:
            return False