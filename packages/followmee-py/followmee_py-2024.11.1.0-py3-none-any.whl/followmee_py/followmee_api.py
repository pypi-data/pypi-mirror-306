import datetime
import logging
from typing import Dict, List

from followmee_py.exceptions import FollowMeeApiException
from followmee_py.models import DeviceInfo, LocationData
from followmee_py.rest_adapter import RestAdapter


def strip_non_alphabetic(input: str):
    return "".join(c for c in input if c.isalpha())


def clean_dict_keys(d: Dict) -> Dict:
    new_d = {}
    for k in d:
        if "(" in k or ")" in k or "/" in k:
            new_k = strip_non_alphabetic(k)
            new_d[new_k] = d[k]
        else:
            new_d[k] = d[k]
    return new_d

def data_has_error(d):
    return "Error" in d

def error_is_no_data(e):
    return "No data returned for your query" in e


class FollowMeeApi:
    def __init__(
        self,
        api_key: str,
        username: str,
        hostname: str = "www.followmee.com",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
    ):
        self._rest_adapter = RestAdapter(
            api_key, username, hostname, ssl_verify, logger
        )

    def get_all_devices(self) -> List[DeviceInfo]:
        ep_params = {"function": "devicelist"}
        result = self._rest_adapter.get(endpoint="info.aspx", ep_params=ep_params)

        if data_has_error(result.data):
            error_msg = result.data["Error"]
            if error_is_no_data(error_msg):
                return []
            raise FollowMeeApiException(error_msg)
        return [DeviceInfo(**raw_data) for raw_data in result.data["Data"]]

    def get_current_location_for_devices(
        self,
        device_ids: List[str],
        include_address: bool = False,
    ) -> List[LocationData]:
        ep_params = {
            "function": "currentfordevice",
            "output": "json",
            "deviceid": ",".join(device_ids),
            "address": 1 if include_address else 0,
        }
        result = self._rest_adapter.get(endpoint="tracks.aspx", ep_params=ep_params)
        if data_has_error(result.data):
            error_msg = result.data["Error"]
            if error_is_no_data(error_msg):
                return []
            raise FollowMeeApiException(error_msg)
        return [
            LocationData(**(clean_dict_keys(raw_data)))
            for raw_data in result.data["Data"]
        ]

    def get_current_location_for_all_devices(
        self,
        include_address: bool = False,
        group_ids: List[str] = [],
    ) -> List[LocationData]:
        ep_params = {
            "function": "currentforalldevices",
            "output": "json",
            "address": 1 if include_address else 0,
        }

        if len(group_ids) != 0:
            ep_params["groupid"] = ",".join(group_ids)

        result = self._rest_adapter.get(endpoint="tracks.aspx", ep_params=ep_params)
        if data_has_error(result.data):
            error_msg = result.data["Error"]
            if error_is_no_data(error_msg):
                return []
            raise FollowMeeApiException(error_msg)
        return [
            LocationData(**(clean_dict_keys(raw_data)))
            for raw_data in result.data["Data"]
        ]

    def get_recent_history_for_device(
        self,
        device_id: str,
        number_hours: int,
        include_address: bool = False,
        include_visit_info: bool = False,
    ) -> List[LocationData]:
        ep_params = {
            "function": "historyfordevice",
            "output": "json",
            "history": number_hours,
            "deviceid": device_id,
            "address": 1 if include_address else 0,
            "visit": 1 if include_visit_info else 0,
        }

        result = self._rest_adapter.get(endpoint="tracks.aspx", ep_params=ep_params)
        if data_has_error(result.data):
            error_msg = result.data["Error"]
            if error_is_no_data(error_msg):
                return []
            raise FollowMeeApiException(error_msg)
        return [
            LocationData(**clean_dict_keys(raw_data))
            for raw_data in result.data["Data"]
        ]

    def get_recent_history_for_all_devices(
        self,
        number_hours: int,
        include_address: bool = False,
        include_visit_info: bool = False,
    ) -> List[LocationData]:
        ep_params = {
            "function": "historyforalldevices",
            "output": "json",
            "history": number_hours,
            "address": 1 if include_address else 0,
            "visit": 1 if include_visit_info else 0,
        }

        result = self._rest_adapter.get(endpoint="tracks.aspx", ep_params=ep_params)
        if data_has_error(result.data):
            error_msg = result.data["Error"]
            if error_is_no_data(error_msg):
                return []
            raise FollowMeeApiException(error_msg)
        return [
            LocationData(**clean_dict_keys(raw_data))
            for raw_data in result.data["Data"]
        ]

    def get_data_in_range_for_device(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        device_id: str,
        include_address: bool = False,
        include_visit_info: bool = False,
    ) -> List[LocationData]:
        ep_params = {
            "function": "daterangefordevice",
            "output": "json",
            "from": start_date.strftime("%Y-%m-%d"),
            "to": end_date.strftime("%Y-%m-%d"),
            "deviceid": device_id,
            "address": 1 if include_address else 0,
            "visit": 1 if include_visit_info else 0,
        }

        result = self._rest_adapter.get(endpoint="tracks.aspx", ep_params=ep_params)
        if data_has_error(result.data):
            error_msg = result.data["Error"]
            if error_is_no_data(error_msg):
                return []
            raise FollowMeeApiException(error_msg)
        
        return [
            LocationData(**clean_dict_keys(raw_data))
            for raw_data in result.data["Data"]
        ]

    def get_data_in_range_for_all_devices(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        include_address: bool = False,
        include_visit_info: bool = False,
        group_ids: List[str] = [],
    ) -> List[LocationData]:
        ep_params = {
            "function": "daterangeforalldevices",
            "output": "json",
            "from": start_date.strftime("%Y-%m-%d"),
            "to": end_date.strftime("%Y-%m-%d"),
            "address": 1 if include_address else 0,
            "visit": 1 if include_visit_info else 0,
        }

        if len(group_ids) != 0:
            ep_params["groupid"] = ",".join(group_ids)

        result = self._rest_adapter.get(endpoint="tracks.aspx", ep_params=ep_params)
        
        if data_has_error(result.data):
            error_msg = result.data["Error"]
            if error_is_no_data(error_msg):
                return []
            raise FollowMeeApiException(error_msg)
        
        return [
            LocationData(**clean_dict_keys(raw_data))
            for raw_data in result.data["Data"]
        ]
