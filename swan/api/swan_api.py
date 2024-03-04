import logging
import os
import uuid
import traceback

from swan.api_client import APIClient
from swan.api.mcs_api import MCSAPI
from swan.common.constant import *
from swan.common.utils import list_repo_contents
from swan.object import HardwareConfig, Task

class SwanAPI(APIClient):
  
    def __init__(self, api_key: str, login: bool = True, environment: str = ""):
        """Initialize user configuration and login.

        Args:
            api_key: SwanHub API key, generated through website
            login: Login into Swanhub or Not
            environment: Selected server 'production/calibration'
        """
        self.token = None
        self.api_key = api_key
        self.environment = environment
        if login:
            self.api_key_login()

    def api_key_login(self):
        """Login with SwanHub API Key.

        Returns:
            A str access token for further SwanHub API access in
            current session.
        """
        params = {"api_key": self.api_key}
        try:
            result = self._request_with_params(
                POST, SWAN_APIKEY_LOGIN, SWAN_API, params, None, None
            )
            self.token = result["data"] 
            logging.info("Login Successfully!")
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
    
    def prepare_source_uri(self, mcs_client: MCSAPI, bucket_name: str, obj_name: str, folder_dir: str):
        """Prepare source uri for task deployment using MCS.

        Args:
            mcs_client: MCSAPI object for mcs connection.
            bucket_name: bucket_name to upload files to.
            obj_name: object/folder name on MCS.
            folder_dir: folder/repo directory for deployment.

        Returns
        """
        try:
            # Upload file to MCS
            mcs_client.upload_folder(bucket_name=bucket_name, object_name=obj_name, folder_path=folder_dir)
            return None
        except Exception as e:
            logging.error(str(e) + '\n' + traceback.format_exc())
            return None
              
    def get_hardware_config(self):
        """Query current hardware list object.
        
        Returns:
            list of HardwareConfig object.
            e.g. obj.to_dict() -> 
            {
                'id': 0, 
                'name': 'C1ae.small', 
                'description': 'CPU only · 2 vCPU · 2 GiB', 
                'type': 'CPU', 
                'reigion': ['North Carolina-US'], 
                'price': '0.0', 
                'status': 'available'
            }
        """
        try:
            response = self._request_without_params(GET, GET_CP_CONFIG, SWAN_API, self.token)
            self.all_hardware = [HardwareConfig(hardware) for hardware in response["data"]["hardware"]]
            return self.all_hardware
        except Exception:
            logging.error("Failed to fetch hardware configurations.")
            return None
        
    def deploy_task(self, cfg_name: str, region: str, start_in: int, duration: int, job_source_uri: str, paid: int = 0.0):
        """Sent deploy task request via orchestrator.

        Args:
            cfg_name: name of cp/hardware configuration set.
            region: region of hardware.
            start_in: unix timestamp of starting time.
            duration: duration of service runtime in unix time.
            job_source_uri: source uri for space.

        Returns:
            JSON response from backend server including 'task_uuid'.
        """
        try:
            if self._verify_hardware_region(cfg_name, region):
                params = {
                    "paid": paid,
                    "duration": duration,
                    "cfg_name": cfg_name,
                    "region": region,
                    "start_in": start_in,
                    "tx_hash": None,
                    "job_source_uri": job_source_uri
                }
                result = self._request_with_params(POST, DEPLOY_TASK, SWAN_API, params, self.token, None)
                return result
            else:
                raise Exception
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None
        
    def deploy_task_obj(self, task: Task):
        """Deploy task requestion using Task object. For easy local task info management.

        Args:
            task: Task object with task details.
        """
        pass
        
    def get_deployment_info(self, task_uuid: str):
        """Retrieve deployment info of a deployed space with task_uuid.

        Args:
            task_uuid: uuid of space task, in deployment response.

        Returns:
            Deployment info.
        """
        try:
            response = self._request_without_params(GET, DEPLOYMENT_INFO+task_uuid, SWAN_API, self.token)
            return response
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None

    def get_payment_info(self):
        """Retrieve payment information from the orchestrator after making the payment.
        """
        try:
            payment_info = self._request_without_params(
                GET, PROVIDER_PAYMENTS, SWAN_API, self.token
            )
            return payment_info
        except:
            logging.error("An error occurred while executing get_payment_info()")
            return None

    def _verify_hardware_region(self, hardware_name: str, region: str):
        """Verify if the hardware exist in given region.

        Args:
            hardware_name: cfg name
            region: geological regions.

        Returns:
            True when hardware exist in given region.
            False when hardware does not exist or do not exit in given region.
        """
        hardwares = self.get_hardware_config()
        for hardware in hardwares:
            if hardware.name == hardware_name:
                if region in hardware.region:
                    return True
                return False
        return False
