import requests
import xml.etree.ElementTree as ET
import datetime


class Probe(object):
    """
    Class which abstracts an Apex probe
    """
    def __init__(self, name, value, type):
        self.name = name
        self.value = value
        self.type = type


class Outlet(object):
    """
    Class which abstracts an Apex outlet
    """
    def __init__(self, name, id, state, device_id):
        self.name = name
        self.id = id
        self.state = state
        self.device_id = device_id

    def get_state(self):
        if self.state == 'AON' or self.state == 'AOF' or self.state == 'AUTO':
            return 0
        elif self.state == 'OFF':
            return 1
        elif self.state == 'ON':
            return 2

    def on(self):
        self.state = 'ON'

    def off(self):
        self.state = 'OFF'

    def auto(self):
        self.state = 'AUTO'


class Apex(object):
    """
    Class which abstracts the interaction with the
    Neptune Apex Aquacontroller.
    """
    def __init__(self, ip_address, user='admin', passwd='1234'):
        self.ip_address = ip_address
        self.user = user
        self.passwd = passwd

        # to be set from api
        self.hostname = None
        self.serial = None
        self.timezone = None
        self.date = None
        self.power_failed = None
        self.power_restored = None
        self.probes = []
        self.outlets = []

        # urls
        self.protocol = 'http://'
        self.status_xml = '/cgi-bin/status.xml'
        self.status = '/status.sht'

    def get_api(self):
        """
        Fetch the data
        """
        response = requests.get(self.protocol + self.ip_address + self.status_xml, auth=(self.user, self.passwd))
        root = ET.fromstring(response.content)
        self.hostname = root.find('hostname').text
        self.serial = root.find('serial').text
        self.timezone = root.find('timezone').text
        self.date = datetime.datetime.strptime(root.find('date').text, '%m/%d/%Y %H:%M:%S')

        probes = root.find('probes')
        for probe in probes:
            self.probes.append(
                Probe(
                    probe.find('name').text,
                    probe.find('value').text,
                    probe.find('type').text,
                )
            )

        outlets = root.find('outlets')
        for outlet in outlets:
            self.outlets.append(
                Outlet(
                    outlet.find('name').text,
                    outlet.find('outputID').text,
                    outlet.find('state').text,
                    outlet.find('deviceID').text,
                )
            )
        return None

    def set_state(self):
        """
        Set a state
        """
        payload = {
            'Update': 'Update',
            'FeedSel': 0,
        }
        for outlet in self.outlets:
            payload[outlet.name + '_state'] = outlet.get_state()

        requests.post(self.protocol + self.ip_address + self.status,
                      auth=(self.user, self.passwd),
                      data=payload)

        return None

    def set_outlet(self, outlet_name, status):
        """
        Set an outlet and then set the state
        """
        if status not in ['on', 'off', 'auto']:
            Exception("Unrecognized outlet status: '%s'" % status)
        for outlet in self.outlets:
            if outlet.name == outlet_name:
                if status == 'on':
                    outlet.on()
                elif status == 'off':
                    outlet.off()
                elif status == 'auto':
                    outlet.auto()
        self.set_state()

        return None