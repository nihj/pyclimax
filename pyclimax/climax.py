"""
Climax Controller Python API.

This lib is designed to simplify communication with Climax HA controllers
"""
import logging
import requests
import sys
import json
import os

#from .subscribe import SubscriptionRegistry
#from .subscribe import PyclimaxError

__author__ = 'nihj'

# Time to block on Climax poll if there are no changes in seconds
SUBSCRIPTION_WAIT = 30
# Min time to wait for event in miliseconds
SUBSCRIPTION_MIN_WAIT = 200
# Timeout for requests calls, as Climax sometimes just sits on sockets.
TIMEOUT = SUBSCRIPTION_WAIT

CATEGORY_DIMMER = 'Dimmer'
CATEGORY_SWITCH = 'Power Switch Meter'
CATEGORY_TEMPERATURE_SENSOR = 'Temperature Sensor'
CATEGORY_POWER_METER = 'Power Meter'

_CLIMAX_CONTROLLER = None

# Set up the console logger for debugging
logger = logging.getLogger(__name__)
# Set logging level (such as INFO, DEBUG, etc) via an environment variable
# Defaults to WARNING log level unless PYClimax_LOGLEVEL variable exists
logger_level = os.environ.get("PYCLIMAX_LOGLEVEL", None)
if logger_level:
    logger.setLevel(logger_level)
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(levelname)s@{%(name)s:%(lineno)d} - %(message)s'))
    logger.addHandler(ch)
logger.debug("DEBUG logging is ON")

def init_controller(url, username, password):
    """Initialize a controller.

    Provides a single global controller for applications that can't do this
    themselves
    """
    # pylint: disable=global-statement
    global _CLIMAX_CONTROLLER
    created = False
    if _CLIMAX_CONTROLLER is None:
        _CLIMAX_CONTROLLER = ClimaxController(url, username, password)
        created = True
        #_CLIMAX_CONTROLLER.start()
    return [_CLIMAX_CONTROLLER, created]


def get_controller():
    """Return the global controller from init_controller."""
    return _CLIMAX_CONTROLLER


class ClimaxController(object):
    """Class to interact with the Climax device."""

    # pylint: disable=too-many-instance-attributes
    temperature_units = 'C'

    def __init__(self, base_url, username, password):
        """Setup Climax controller at the given URL.

        base_url: Climax API URL, eg http://Climax:80.
        """
        self.base_url = base_url
        self.username = username
        self.password = password
        self.devices = []
        self.version = None
        self.zwave_version = None
        self.mac = None

        #self.subscription_registry = SubscriptionRegistry()
        self.device_id_map = {}

    def post_request(self, method, payload, timeout=TIMEOUT):
        """Post a request and return the result."""
        requests_url = self.base_url + "/action/" + method 
        return requests.post(requests_url, auth=(self.username, self.password), timeout=timeout, params=payload)

    def get_request(self, method, payload={}, timeout=TIMEOUT):
        """Post a request and return the result."""
        requests_url = self.base_url + "/action/" + method

        r = requests.get(requests_url, auth=(self.username, self.password), timeout=timeout, params=payload)
        

        return r

    def get_device_by_name(self, device_name):
        """Search the list of connected devices by name.

        device_name param is the string name of the device
        """

        # Find the device for the Climax device name we are interested in
        found_device = None
        for device in self.get_devices():
            if device.name == device_name:
              found_device = device
              # found the first (and should be only) one so we will finish
              break

        if found_device is None:
            logger.debug('Did not find device with {}'.format(device_name))

        return found_device

    def get_device_by_id(self, device_id):
        """Search the list of connected devices by ID.

        device_id param is the integer ID of the device
        """

        # Find the device for the Climax device name we are interested in
        found_device = None
        for device in self.get_devices():
            if device.device_id == device_id:
              found_device = device
              # found the first (and should be only) one so we will finish
              break

        if found_device is None:
            logger.debug('Did not find device with {}'.format(device_id))

        return found_device

    def get_devices(self):
        """Get list of connected devices."""
        # pylint: disable=too-many-branches

        j = self.get_request('deviceListGet').json()

        self.devices = []
        items = j.get('senrows')

        for item in items:
            device_type = item.get('type_f')
            if CATEGORY_DIMMER in device_type:
                device = ClimaxDimmer(item, self)
            elif CATEGORY_SWITCH in device_type:
                device = ClimaxSwitch(item, self)
            elif (CATEGORY_TEMPERATURE_SENSOR in device_type or
                CATEGORY_POWER_METER in device_type):
                device = ClimaxSensor(item, self)
            else:
                device = ClimaxDevice(item, self)
            
            self.devices.append(device)

        return self.devices

    def refresh_data(self):
        """Refresh data from Climax device."""
        j = self.get_request('welcomeGet').json()

        self.version = j.get('version')
        self.zwave_version = j.get('zw_ver')
        self.mac = j.get('mac')

        device_id_map = {}

        j = self.get_request('deviceListGet').json()

        devs = j.get('senrows')
        for dev in devs:
            device_id_map[dev.get('id')] = dev

        return device_id_map

    # def get_changed_devices(self, timestamp):
    #     """Get data since last timestamp.

    #     This is done via a blocking call, pass NONE for initial state.
    #     """
    #     if timestamp is None:
    #         payload = {}
    #     else:
    #         payload = {
    #             'timeout': SUBSCRIPTION_WAIT,
    #             'minimumdelay': SUBSCRIPTION_MIN_WAIT
    #         }
    #         payload.update(timestamp)
    #     # double the timeout here so requests doesn't timeout before Climax
    #     payload.update({
    #         'id': 'lu_sdata',
    #     })

    #     logger.debug("get_changed_devices() requesting payload %s", str(payload))
    #     r = self.data_request(payload, TIMEOUT*2)
    #     r.raise_for_status()

    #     # If the Climax disconnects before writing a full response (as lu_sdata
    #     # will do when interrupted by a Luup reload), the requests module will
    #     # happily return 200 with an empty string. So, test for empty response,
    #     # so we don't rely on the JSON parser to throw an exception.
    #     if r.text == "":
    #         raise PyclimaxError("Empty response from Climax")

    #     # Catch a wide swath of what the JSON parser might throw, within
    #     # reason. Unfortunately, some parsers don't specifically return
    #     # json.decode.JSONDecodeError, but so far most seem to derive what
    #     # they do throw from ValueError, so that's helpful.
    #     try:
    #         result = r.json()
    #     except ValueError as ex:
    #         raise PyclimaxError("JSON decode error: " + str(ex))

    #     if not ( type(result) is dict
    #              and 'loadtime' in result and 'dataversion' in result ):
    #         raise PyclimaxError("Unexpected/garbled response from Climax")

    #     # At this point, all good. Update timestamp and return change data.
    #     device_data = result.get('devices')
    #     timestamp = {
    #         'loadtime': result.get('loadtime'),
    #         'dataversion': result.get('dataversion')
    #     }
    #     return [device_data, timestamp]

    # def start(self):
    #     """Start the subscription thread."""
    #     self.subscription_registry.start()

    # def stop(self):
    #     """Stop the subscription thread."""
    #     self.subscription_registry.stop()

    # def register(self, device, callback):
    #     """Register a device and callback with the subscription service."""
    #     self.subscription_registry.register(device, callback)

    # def unregister(self, device, callback):
    #     """Unregister a device and callback with the subscription service."""
    #     self.subscription_registry.unregister(device, callback)


class ClimaxDevice(object):  # pylint: disable=R0904
    """ Class to represent each Climax device."""

    def __init__(self, json_obj, Climax_controller):
        """Setup a Climax device."""
        self.json_state = json_obj
        self.device_id = self.json_state.get('id')
        self.Climax_controller = Climax_controller
        self.name = ''

        self.type = self.json_state.get('type_f')
        self.name = self.json_state.get('name')

        if not self.name:
            if self.type:
                self.name = ('Climax ' + self.type +
                             ' ' + str(self.device_id))
            else:
                self.name = 'Climax Device ' + str(self.device_id)

    def __repr__(self):
        if sys.version_info >= (3, 0):
            return "{} (id={} type={} name={})".format(
                self.__class__.__name__,
                self.device_id,
                self.type,
                self.name)
        else:
            return u"{} (id={} type={} name={})".format(
                self.__class__.__name__,
                self.device_id,
                self.type,
                self.name).encode('utf-8')

    def Climax_post_request(self, method, **kwargs):
        """Perfom a Climax_request for this device."""
        request_payload = {}
        request_payload.update(kwargs)

        return self.Climax_controller.post_request(method, request_payload)
    
    def Climax_get_request(self, method, **kwargs):
        """Perfom a Climax_request for this device."""
        request_payload = {}
        request_payload.update(kwargs)

        return self.Climax_controller.get_request(method, request_payload)

    def set_device_value(self, method, device_id, parameter_name, value):
        """Set a variable on the Climax device.

        This will call the Climax api to change device state.
        """

        payload = {
            'id': device_id,
            parameter_name: value
        }
        result = self.Climax_post_request(method, **payload)
        logger.debug("set_service_value: "
                  "result of Climax_request %s with payload %s: %s",
                  method, payload, result.text)

    def get_all_values(self):
        """Get all values from the deviceInfo area.

        The deviceInfo data is updated by the subscription service.
        """
        return self.json_state

    def get_value(self, name):
        """Get a value from the dev_info area.

        This is the common Climax data and is the best place to get state from
        if it has the data you require.

        This data is updated by the subscription service.
        """
        return self.get_strict_value(name.lower())

    def get_strict_value(self, name):
        """Get a case-sensitive keys value from the dev_info area.
        """
        dev_info = self.json_state
        return dev_info.get(name, None)

    def refresh(self):
        """Refresh the dev_info data used by get_value.

        Only needed if you're not using subscriptions.
        """
        j = self.Climax_get_request('deviceListGet').json()
        devices = j.get('senrows')
        for device_data in devices:
            if device_data.get('id') == self.device_id:
                self.update(device_data)

    def update(self, params):
        """Update the dev_info data from a dictionary.

        Only updates if it already exists in the device.
        """
        dev_info = self.json_state
        dev_info.update({k: params[k] for k in params if dev_info.get(k)})

    @property
    def is_dimmable(self):
        """Device is dimmable."""
        return CATEGORY_DIMMER in self.type

    @property
    def has_battery(self):
        """Device has a battery."""
        return self.get_value('battery') is not None

    @property
    def battery_level(self):
        """Battery level as a percentage."""
        return self.get_value('battery')

    @property
    def level(self):
        """Get level from Climax."""
        # Used for dimmers
        # Have seen formats of "0%"!
        level = self.get_value('status')

        level = level.strip('On (')
        try:
            return int(level.strip('%)'))
        except (TypeError, AttributeError, ValueError):
            pass
        return 0

    @property
    def temperature(self):
        """Temperature.

        You can get units from the controller.
        """

        temp = self.get_value('status')
        try:
            return float(temp.strip(' °C'))
        except (TypeError, AttributeError, ValueError):
            pass
        return 0.0

    @property
    def power(self):
        """Current power useage in watts"""
        power = self.get_value('status')
        
        power = power.strip('Off, ')
        power = power.strip('On, ')

        try:
            return float(power.strip('W'))
        except (TypeError, AttributeError, ValueError):
            pass
        return 0.0

    @property
    def energy(self):
        """Energy usage in kwh"""
        power = self.get_value('status')
        
        try:
            return float(power.strip('kWh'))
        except (TypeError, AttributeError, ValueError):
            pass
        return 0.0

    @property
    def Climax_device_id(self):
        """The ID Climax uses to refer to the device."""
        return self.device_id

    @property
    def should_poll(self):
        """Whether polling is needed if using subscriptions for this device."""
        return False


class ClimaxSwitch(ClimaxDevice):
    """Class to add switch functionality."""

    def set_switch_state(self, state):
        """Set the switch state, also update local state."""
        self.set_device_value(
            'deviceSwitchPSSPost',
            self.device_id,
            'switch',
            state)

    def switch_on(self):
        """Turn the switch on."""
        self.set_switch_state(1)

    def switch_off(self):
        """Turn the switch off."""
        self.set_switch_state(0)

    def switch_toggle(self):
        """Toggle the switch state."""

        print("Toggling switch")

        self.set_switch_state(2)

    def is_switched_on(self, refresh=False):
        """Get switch state.

        Refresh data from Climax if refresh is True, otherwise use local cache.
        Refresh is only needed if you're not using subscriptions.
        """
        if refresh:
            self.refresh()
        val = self.get_value('status')
        return 'On' in val


class ClimaxDimmer(ClimaxSwitch):
    """Class to add dimmer functionality."""

    def get_brightness(self, refresh=False):
        """Get dimmer brightness.

        Refresh data from Climax if refresh is True, otherwise use local cache.
        Refresh is only needed if you're not using subscriptions.
        Converts the Climax level property for dimmable lights from a percentage
        to the 0 - 255 scale used by HA.
        """
        if refresh:
            self.refresh()
        brightness = 0
        percent = self.level
        if percent > 0:
            brightness = round(percent * 2.55)
        return int(brightness)

    def set_brightness(self, brightness):
        """Set dimmer brightness.

        Converts the Climax level property for dimmable lights from a percentage
        to the 0 - 255 scale used by HA.
        """
        percent = 0
        if brightness > 0:
            percent = round(brightness / 2.55)

        self.set_device_value(
            'deviceSwitchDimmerPost',
            self.device_id,
            'level',
            percent)

class ClimaxSensor(ClimaxDevice):
    """Class to represent a supported sensor."""
