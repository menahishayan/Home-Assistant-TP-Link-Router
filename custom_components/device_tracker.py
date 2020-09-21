"""Support for TP-Link routers."""

import base64
import logging
import re
import requests
import voluptuous as vol
from homeassistant.components.device_tracker import (
    DOMAIN, PLATFORM_SCHEMA, DeviceScanner)
from homeassistant.const import (
    CONF_HOST, CONF_PASSWORD, CONF_USERNAME, HTTP_HEADER_X_REQUESTED_WITH)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_USERNAME): cv.string
})

def get_scanner(hass, config):
    """Validate the configuration and return a TP-Link scanner."""
    for cls in [N600TplinkDeviceScanner]:
        scanner = cls(config[DOMAIN])
        if scanner.success_init:
            return scanner

    return None


class TplinkDeviceScanner(DeviceScanner):
    """Abstract parent class for all TPLink device scanners."""

    def __init__(self, config):
        """Generic scanner initialization."""
        host = config[CONF_HOST]
        username, password = config[CONF_USERNAME], config[CONF_PASSWORD]

        self.parse_macs_hyphens = re.compile('[0-9A-F]{2}-[0-9A-F]{2}-' +
                                             '[0-9A-F]{2}-[0-9A-F]{2}-' +
                                             '[0-9A-F]{2}-[0-9A-F]{2}')
        self.parse_macs_colons = re.compile('[0-9A-F]{2}:[0-9A-F]{2}:' +
                                            '[0-9A-F]{2}:[0-9A-F]{2}:' +
                                            '[0-9A-F]{2}:[0-9A-F]{2}')

        self.host = host
        self.username = username
        self.password = password

        self.last_results = {}
        self.success_init = self._update_info()

    def scan_devices(self):
        """Scan for new devices and return a list with found device IDs."""
        self._update_info()
        return self.last_results

    # pylint: disable=no-self-use
    def get_device_name(self, device):
        """Firmware doesn't save the name of the wireless device.
        Home Assistant will default to MAC address."""
        return None

    def get_base64_cookie_string(self):
        """Encode Base 64 authentication string for some scanners."""
        username_password = '{}:{}'.format(self.username, self.password)
        b64_encoded_username_password = base64.b64encode(
            username_password.encode('ascii')
        ).decode('ascii')
        return 'Authorization=Basic {}'.format(b64_encoded_username_password)


class N600TplinkDeviceScanner(TplinkDeviceScanner):
    """This class queries TP-Link N600 router and TL-WR840N router."""

    def _update_info(self):
        """Ensure the information from the TP-Link router is up to date.
        Return boolean if scanning successful.
        """
        _LOGGER.info("[N600] Loading wireless clients...")

        # Router uses Authorization cookie instead of header.
        cookie = self.get_base64_cookie_string()

        referer = 'http://{}'.format(self.host)
        mac_results = []

        # Check both the 2.4GHz and 5GHz client lists.
        for clients_frequency in ('1', '2'):

            # Refresh associated clients.
            page = requests.post(
                'http://{}/cgi?7'.format(self.host),
                headers={'referer': referer, 'cookie': cookie},
                data=(
                    '[ACT_WLAN_UPDATE_ASSOC#1,{},0,0,0,0#0,0,0,0,0,0]0,0\r\n'
                    ).format(clients_frequency),
                timeout=4)
            if not page.status_code == 200:
                _LOGGER.error("Error %s from router", page.status_code)
                return False

            # Retrieve associated clients.
            page = requests.post(
                'http://{}/cgi?6'.format(self.host),
                headers={'referer': referer, 'cookie': cookie},
                data=(
                    '[LAN_WLAN_ASSOC_DEV#0,0,0,0,0,0#1,{},0,0,0,0]0,1\r\n'
                    'AssociatedDeviceMACAddress\r\n'
                    ).format(clients_frequency),
                timeout=4)
            if not page.status_code == 200:
                _LOGGER.error("Error %s from router", page.status_code)
                return False

            mac_results.extend(self.parse_macs_colons.findall(page.text))

        if mac_results:
            self.last_results = mac_results
            return True

        return False

