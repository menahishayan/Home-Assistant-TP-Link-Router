# Home Assistant TP Link Router
 Home Assistant component for complete router administration of the TP Link Archer C50 and the TP Link N600 based on the [TP-Link Router API](https://github.com/menahishayan/TP-Link-Archer-C50-API.git)

**v1.0.0**

## Installation

### HACS (recommended)

1. Go to the Community Store.
2. Search for `Home Assistant TP Link Router`.
3. Navigate to `Home Assistant TP Link Router` integration
4. Press `Install`.

### Manual

Clone this repository in your existing (or create it) `custom_components/` folder.

```bash
cd custom_components/
git clone https://github.com/menahishayan/Home-Assistant-TP-Link-Router.git
```

Or using submodules:

```bash
cd custom_components/
git submodule add https://github.com/menahishayan/Home-Assistant-TP-Link-Router.git
```

### Setup

**Add the following to your configuration.yaml:**  
1. For Switches:
```yaml
switch:
  - platform: tplink_router
    host: 'hostname or IP'
    username: 'username'
    password: 'password'
```
2. For Sensors:
```yaml
sensor:
  - platform: tplink_router
    host: 'hostname or IP'
    username: 'username'
    password: 'password'
```
3. Device Tracker:
```yaml
device_tracker:
  - platform: tplink_router
    host: 'hostname or IP'
    username: 'username'
    password: 'password'
```

## Components
### Switches
 - Router Power (Restart)
 - WAN Connection Enable/Disable
 - 2.4Ghz Band Enable/Disable
 - 5Ghz Band Enable/Disable

### Sensors
 - IP Addresses of clients across 2.4Ghz, 5Ghz and LAN

### Device Tracker
 - Track clients by MAC address across 2.4Ghz, 5Ghz and LAN

## Troubleshooting/Error Reporting/Contributing
 - If you face an error, you may debug using a HTTP Requests tool/monitor on your router's configuration webpage. Additionally, you may open a new issue on this repo prefixed by [Bug]
 - If you would like to help improve the package, request features or add support for more models, open an issue prefixed by [Feature Request] or [Improvement]

## PRs and Commit Template
PRs and commits that you make to this repo must include the following:  
- Type: bug-fix or enhancement
- Description: Brief description about what the commit achieves
- Notes: (heads ups/pointers to other developers if necessary)

## Contributing
This integration is merely a Home Assistant interface for the [TP-Link Router API](https://github.com/menahishayan/TP-Link-Archer-C50-API.git). To help improve the core API itself, such as adding more controls, or supporting more routers, head over to the API's repo and create a pull request there.

For improvements in how this integration actually interfaces the API with Home Assisant's developer modules, you may make a pull request here.

## Changelog
### v1.0.0
 - First Production Release
