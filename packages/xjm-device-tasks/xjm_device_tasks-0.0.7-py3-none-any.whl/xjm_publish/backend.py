import requests
from typing import List, Optional, Tuple, Literal, Dict, Any

from .logger import get_logger

Logger = get_logger()


def set_auth_header(token):
    with open('__auth.txt', 'w') as auth_file:
        auth_file.write(token)


def set_user_agent(ua):
    with open('__ua.txt', 'w') as ua_file:
        ua_file.write(ua)


def get_auth_header():
    try:
        with open('__auth.txt', 'r') as auth_file:
            return auth_file.read().strip()
    except FileNotFoundError:
        return None


def get_user_agent():
    try:
        with open('__ua.txt', 'r') as ua_file:
            return ua_file.read().strip()
    except FileNotFoundError:
        return None


def singleton(cls):
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance


@singleton
class Backend:
    def __init__(self, remote_url="http://entry.a0go.com:3838"):
        self.timeout = 10
        self.remote_url = remote_url

    def get_headers(self):
        return {
            "Authorization": get_auth_header(),
            "User-Agent": get_user_agent(),
        }

    def change_backend_url(self, url: str):
        self.remote_url = url

    def _request(self, method: str, endpoint: str, use_json=True, **kwargs):
        url = f"{self.remote_url}{endpoint}"
        response = requests.request(method, url, headers=self.get_headers(), timeout=self.timeout, **kwargs)
        if response == 500:
            response.raise_for_status()
            return
        if response.status_code != 200:
            body = ""
            try:
                body = response.json()
                if "detail" in body:
                    body = body["detail"]
            except Exception as e:
                body = response.text
            Logger.error(f"[请求]{endpoint} 失败{body} 响应码 {response.status_code}")
            raise Exception(body)
        if use_json:
            return response.json()
        return response.text

    def report_task_result(self, task_id: str, status: str, msg: str):
        data = {
            "task_id": task_id,
            "status": status,
            "msg": msg
        }
        return self._request("POST", "/report_client_task_result", json=data)

    def add_client_task(self, task_name: str,
                        task_params: Dict[str, Any],
                        device_serial: str,
                        system_user_id: Optional[int] = 0,
                        priority: Optional[int] = 3,
                        from_origin: Optional[str] = "",
                        foreign_id: Optional[str] = ""):
        data = {
            "task_name": task_name,
            "task_params": task_params,
            "device_serial": device_serial,
            "priority": priority,
            "from_origin": from_origin,
            "foreign_id": foreign_id,
            "system_user_id": system_user_id,
        }
        return self._request("POST", "/add_client_task", json=data)

    def retry_client_task(self, task_id: str):
        data = {
            "task_id": task_id
        }
        return self._request("POST", "/retry_client_task", json=data)

    def query_serial_task(self, device_serial: str, page: int = 1, page_size: int = 10, status: Optional[str] = None,
                          name: Optional[str] = None):
        params = {
            "device_serial": device_serial,
            "page": page,
            "page_size": page_size,
            "status": status,
            "name": name
        }
        return self._request("GET", "/query_serial_task", params=params)

    def add_device(self, device_serial: str, device_info: dict):
        data = {
            "device_serial": device_serial,
            "device_info": device_info
        }
        return self._request("POST", "/add_device", json=data)

    def get_device(self, device_serial: str):
        return self._request("GET", f"/get_device", params={"device_serial": device_serial})

    def have_device(self, device_serial: str):
        return self._request("GET", f"/have_device", params={"device_serial": device_serial})

    def get_bulk_device(self, device_serials: List[str]):
        data = {
            "device_serials": device_serials
        }
        return self._request("POST", "/get_bulk_device", json=data)

    def get_devices_can_run_task(self, device_serials: List[str]):
        data = {
            "device_serials": device_serials
        }
        return self._request("POST", "/get_devices_can_run_task", json=data)

    def get_all_tasks(self):
        return self._request("GET", "/get_all_tasks")

    def set_device_alias(self, device_serial: str, alias: str):
        data = {
            "device_serial": device_serial,
            "alias": alias
        }
        return self._request("POST", "/set_device_alias", json=data)

    # 返回的是 {"last_work_uid":""} 或报错
    def get_device_platform_last_video_id(self, device_serial: str, platform_name: str, platform_id=None):
        data = {
            "device_serial": device_serial,
            "platform_name": platform_name,
            "platform_id": platform_id
        }
        return self._request("GET", "/get_device_platform_last_video_id", params=data)

    def get_device_platform_video_ids(self, device_serial: str, platform_name: str, platform_id=None):
        """
        获取用户平台视频ids列表 第一页的
        :param device_serial:
        :param platform_name:
        :param platform_id:
        :return: {"aweme_ids": ["id1","id2"]}
        """
        data = {
            "device_serial": device_serial,
            "platform_name": platform_name,
            "platform_id": platform_id
        }
        return self._request("GET", "/get_device_platform_video_ids", params=data)

    def add_platform_account(self,
                             device_serial: str,
                             platform_name: str,
                             platform_id: str,
                             account_name: str,
                             fans: int = 0,
                             like: int = 0,
                             signature: Optional[str] = None,
                             work_count: int = 0,
                             uid: Optional[str] = "",
                             is_exception: Optional[bool] = False,
                             exception_msg: Optional[str] = "",
                             system_user_id: Optional[int] = 0,  # 系统空间用户id
                             ):
        data = {
            "device_serial": device_serial,
            "platform_name": platform_name,
            "platform_id": platform_id,
            "account_name": account_name,
            "fans": fans,
            "like": like,
            "signature": signature,
            "work_count": work_count,
            "uid": uid,
            "is_exception": is_exception,
            "exception_msg": exception_msg,
            "system_user_id": system_user_id,
        }
        return self._request("POST", "/add_platform_account", json=data)

    def report_platform_works_views(self, device_serial: str, platform_name: str, views: list, platform_id: str = None):
        data = {
            "device_serial": device_serial,
            "platform_name": platform_name,
            "platform_id": platform_id,
            "views": views,
        }
        return self._request("POST", "/report_platform_works_views", json=data)

    def delete_platform_account(self, device_serial: str, platform_name: str):
        data = {
            "device_serial": device_serial,
            "platform_name": platform_name
        }
        return self._request("POST", "/delete_platform_account", json=data)

    def device_task_files(self):
        return self._request("GET", "/device_task_files")

    def get_device_task_file(self, filename: str):
        params = {
            "filename": filename
        }
        return self._request("GET", "/device_task_file", use_json=False, params=params)


def get_backend() -> Backend:
    return Backend()
