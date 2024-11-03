import requests
from json import JSONDecodeError
from ownerrezconnector.model import Result


from typing import List, Dict
import logging
import datetime
from ownerrezconnector.constants import BASEURL as hosturl
from ownerrezconnector.exeptions import OwerrezapiExeception

class RestAdapter(object):
    def __init__(self,username, token):
        """
        Initialize the RestAdapter object with the OwnerRez username and token
        :param username: OwnerRez username
        :param token: OwnerRez token
        
        """
        self.auth = username,token
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)

    def _do_request(self, http_method, endpoint, ep_params,data: Dict = None):
        """
        Make a request to the OwnerRez API
        :param http_method: HTTP method to use
        :param endpoint: API endpoint to call
        :param ep_params: Dictionary of parameters to pass to the endpoint
        :param data: Dictionary of data to pass in the request body
        :return: Result object
        """
        
        full_url = hosturl + endpoint
        headers = {'User-Agent':'OwerRezAPI','Content-Type':'application/json'}
        log_line_pre = f"method={http_method}, url={full_url}, params={ep_params}"
        log_line_post = ', '.join((log_line_pre, "success={}, status_code={}, message={}"))
        
        # Make the request
        try:
            self._logger.debug(msg = log_line_pre)
            response = requests.request(method=http_method,url=full_url,auth=self.auth,headers=headers,params=ep_params,json=data)
        
        # If the request fails, log the error and raise an exception
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise OwerrezapiExeception("Request failed") from e
        
        # Try to parse the response as JSON
        try:
            data_out = response.json()
        # If it fails, log the error and raise an exception
        except (ValueError, TypeError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise OwerrezapiExeception("Bad JSON in response") from e

        # If status_code in 200-299 range, return success Result with data, otherwise raise exception
        is_success = 299 >= response.status_code >= 200     # 200 to 299 is OK
        log_line = "success"
        
        # If the response is successful, log the response and return the Result object
        if is_success:
            self._logger.debug(msg=log_line)
            return Result(status= response.status_code, message=response.reason, data=data_out)
        
        # If the response is not successful, log the response and raise an exception
        self._logger.error(msg=log_line)
        raise OwerrezapiExeception(f"{response.status_code}: {response.reason}")

    def get(self, endpoint: str, ep_params: Dict = None) -> Result:
        """
        Make a GET request to the OwnerRez API
        :param endpoint: API endpoint to call
        :param ep_params: Dictionary of parameters to pass to the endpoint
        :return: Result object
        """
        return self._do_request(http_method='GET', endpoint=endpoint, ep_params=ep_params)