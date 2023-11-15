# Home Assistant TP Link Router
 Home Assistant component for complete router administration of the TP Link Archer C50 and the TP Link N600 based on the [TP-Link Router API](https://github.com/menahishayan/TP-Link-Archer-C50-API.git)

### Looking for Maintainers
Between full-time work and commitments, I no longer find the time to maintain this project. As a result you'll find a number of open issues. If you're interested to contribute, feel free to open a PR! Until then, this project is stale and likely won't recieve updates.

## Installation

### HACS (recommended)

1. Go to the Community Store.
2. Search for `Home Assistant TP Link Router`.
3. Navigate to `Home Assistant TP Link Router` integration
4. Press `Install`.

### Manual

1. Clone this repository
```bash
git clone https://github.com/menahishayan/Home-Assistant-TP-Link-Router.git
```
2. Move `tplink_router` to `custom_components`
```bash
mv Home-Assistant-TP-Link-Router/custom_components/tplink_router <HA_ROOT>/custom_components/
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
 
## Adding Support For More Models
Head over to [CONTRIBUTING.md](https://github.com/menahishayan/TP-Link-Archer-C50-API/blob/master/CONTRIBUTING.md)

## Troubleshooting/Error Reporting/Contributing
 - If you face an error, you may debug using a HTTP Requests tool/monitor on your router's configuration webpage. Additionally, you may open a new issue on this repo prefixed by [Bug]
 - If you would like to help improve the package, request features or add features, open an issue prefixed by [Feature Request] or [Improvement]

## PRs and Commit Template
PRs and commits that you make to this repo must include the following:  
- Type: bug-fix or enhancement
- Description: Brief description about what the commit achieves
- Notes: (heads ups/pointers to other developers if necessary)

## Contributing
This integration is merely a Home Assistant interface for the [TP-Link Router API](https://github.com/menahishayan/TP-Link-Archer-C50-API.git). To help improve the core API itself, such as adding more controls, or supporting more routers, head over to the API's repo and create a pull request there.

For improvements in how this integration actually interfaces the API with Home Assisant's developer modules, you may make a pull request here.

## Changelog
### v1.0.3
 - Update README for Manual Install changes in HA 2023.x [#14](https://github.com/menahishayan/Home-Assistant-TP-Link-Router/issues/14)
 - Fix user agent issues [#11](https://github.com/menahishayan/Home-Assistant-TP-Link-Router/issues/11)
### v1.0.2
 - json file version number added
 - C7 logs out to prevent lock
### v1.0.1
 - Fix Github incorrect release
### v1.0.0
 - First Production Release

