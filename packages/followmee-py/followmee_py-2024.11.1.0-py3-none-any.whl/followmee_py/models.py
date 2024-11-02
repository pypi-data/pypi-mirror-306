from datetime import datetime
from typing import List, Dict

TIME_FMT_STR = "%Y-%m-%dT%H:%M:%S%z"


class Result:
    def __init__(self, status_code: int, message: str = "", data: List[Dict] = None):
        """
        Result returned from low-level RestAdapter
        :param status_code: Standard HTTP Status code
        :param message: Human readable result
        :param data: Python List of Dicts
        """
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []


class DeviceInfo:
    def __init__(
        self,
        DeviceID: str,
        DeviceName: str,
        Platform: str,
        Edition: str,
        Group: str,
        Active: str,
        TrackerState: str,
        TrackerStateTime: str,
        Battery: str,
        BatteryTime: str,
    ):
        self.device_id = DeviceID
        self.device_name = DeviceName
        self.platform = Platform
        self.edition = Edition
        self.group = Group
        self.active = Active == "1"
        self.tracker_state = int(TrackerState)
        self.tracker_state_time = datetime.strptime(TrackerStateTime, TIME_FMT_STR)
        self.battery = float(Battery.strip("%")) / 100.0
        self.battery_time = datetime.strptime(BatteryTime, TIME_FMT_STR)


class LocationData:
    def __init__(
        self,
        DeviceName: str,
        DeviceID: str,
        Date: str,
        Latitude: float,
        Longitude: float,
        Type: str,
        Speedmph: int,
        Speedkmh: int,
        Direction: int,
        Altitudeft: int,
        Altitudem: int,
        Accuracy: int,
        Battery: str,
    ):
        self.device_name = DeviceName
        self.device_id = DeviceID
        self.date = datetime.strptime(Date, TIME_FMT_STR)
        self.latitude = Latitude
        self.longitude = Longitude
        self.type = Type
        self.speed_mph = Speedmph
        self.speed_kmh = Speedkmh
        self.direction = Direction
        self.altitude_ft = Altitudeft
        self.altitude_m = Altitudem
        self.accuracy = Accuracy
        self.battery = float(Battery.strip("%")) / 100.0
