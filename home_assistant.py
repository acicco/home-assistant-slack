import requests
import json


class Device:
    def __init__(self, device_name, device_id, device_type, device_state):
        self.device_name = device_name
        self.device_id = device_id
        self.device_type = device_type
        self.device_state = device_state

    def __str__(self):
        return "Device: {}, ID: {}, Type: {}, State: {}".format(
            self.device_name, self.device_id, self.device_type, self.device_state
        )

    def getId(self):
        return self.device_id.split(".")[1]


class HomeAssistant:
    def __init__(self, name, ip, port, token):
        self.name = name
        self.ip = ip
        self.port = port
        self.token = token
        self.devices = []

    def get_name(self):
        return self.name

    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.port

    def getDevices(self):
        url = "http://" + self.ip + ":" + str(self.port) + "/api/states"
        headers = {"Authorization": "Bearer " + self.token}
        response = requests.get(url, headers=headers)
        devices = response.json()
        for device in devices:
            device_type = device["entity_id"].split(".")[0]
            self.devices.append(
                Device(
                    device["attributes"]["friendly_name"],
                    device["entity_id"],
                    device_type,
                    device["state"],
                )
            )
        return self.devices

    def findDevice(self, device_name):
        for device in self.devices:
            if device.device_name.lower().find(device_name.lower()) != -1:
                return device

        return None

    # toggle device state
    def toggleDevice(self, device_name):
        device = self.findDevice(device_name)
        if device is None:
            return False

        if device.device_state == "on":
            action = "off"

        elif device.device_state == "off":
            action = "on"

        else:
            return False

        url = (
            "http://"
            + self.ip
            + ":"
            + str(self.port)
            + "/api/services/"
            + device.device_type
            + "/turn_"
            + action
        )
        headers = {"Authorization": "Bearer " + self.token}
        data = json.dumps({"entity_id": device.device_id})
        response = requests.post(url, headers=headers, data=data)

        return {
            "status": response.status_code,
            "device": {"name": device.device_name, "state": action},
        }
