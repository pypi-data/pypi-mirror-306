from json import JSONDecodeError
import logging
from typing import Dict

import requests
import requests.packages

from followmee_py.exceptions import FollowMeeApiException
from followmee_py.models import Result


class RestAdapter:
    def __init__(
        self,
        api_key: str,
        username: str,
        hostname: str = "www.followmee.com",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
    ):
        """
        :param api_key: string used for authentication
        :param username: FollowMee username
        :param hostname: Normally, www.followmee.com
        :param ssl_verify: Normally set to True, but if having SSL/TLS cert validation issues, can turn off with False
        :param logger: (optional) If your app has a logger, pass it in here
        """
        self.url = f"https://{hostname}/api/"
        self._api_key = api_key
        self._username = username
        self._ssl_verify = ssl_verify
        self._logger = logger or logging.getLogger(__name__)
        if not ssl_verify:
            requests.packages.urllib3.disable_warnings()

    def _do(
        self, http_method: str, endpoint: str, ep_params: Dict = None, data: Dict = None
    ) -> Result:
        full_url = self.url + endpoint
        ep_params["key"] = self._api_key
        ep_params["username"] = self._username
        log_line_pre = f"method={http_method}, url={full_url}, params={ep_params}"
        # Log HTTP params and perform an HTTP request, catching and re-raising any exceptions

        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(
                method=http_method,
                url=full_url,
                verify=self._ssl_verify,
                params=ep_params,
                json=data,
            )
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise FollowMeeApiException("Request failed") from e
        # Deserialize JSON output to Python object, or return failed Result on exception
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            log_line = (
                f"{log_line_pre}, success={False}, status_code={None}, message={e}"
            )
            self._logger.error(log_line)
            raise FollowMeeApiException("Bad JSON in response") from e

        is_success = 200 <= response.status_code <= 299
        log_line = f"{log_line_pre}, success={is_success}, status_code={response.status_code}, message={response.reason}"

        if is_success:
            self._logger.debug(msg=log_line)
            return Result(response.status_code, message=response.reason, data=data_out)
        self._logger.error(msg=log_line)
        raise FollowMeeApiException(f"{response.status_code}: {response.reason}")

    def get(self, endpoint: str, ep_params: Dict = None) -> Result:
        return self._do(http_method="GET", endpoint=endpoint, ep_params=ep_params)

    def post(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        return self._do(
            http_method="POST", endpoint=endpoint, ep_params=ep_params, data=data
        )
