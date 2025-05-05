import json
import re
from typing import BinaryIO, Optional, Type, TypeVar

import requests
from pydantic import BaseModel  # pylint: disable=unused-import
from sseclient import SSEClient

from .config import settings
from .constants.base import HttpMethod
from .utils import info

REQUEST_TIME_OUT = 300
ModelType = TypeVar("ModelType", bound="BaseModel")  # pylint: disable=invalid-name


class DifyApiError(Exception):
    def __init__(self, code: int = 0, message: str = "unknown error", **kwargs: dict) -> None:
        super().__init__()
        self.code = code
        self.message = message
        self.kwargs = kwargs

    def __repr__(self) -> str:
        return self.message + f" -> {self.kwargs}"

    def __str__(self) -> str:
        return self.message + f" -> {self.kwargs}"


class DifySDK:
    def __init__(
        self,
        app_key: str,
        *,
        api_url: str = settings.DIFY_API_URL,
        app_name: str = "",
    ):
        self.api_url = api_url
        self.app_key = app_key
        self.app_name = app_name
        self.headers = {
            "Authorization": f"Bearer {self.app_key}",
            "Content-Type": "application/json",
        }
        self.path_comp = re.compile(r":[a-zA-Z\_]+")

    def _complete_data(self, data: dict, user: str, stream: Optional[bool]) -> dict:
        data["user"] = user
        if stream:
            data["response_mode"] = "streaming"
        elif stream is False:
            data["response_mode"] = "blocking"
        return data

    def _handle_error_response(self, resp: requests.Response) -> None:
        if resp.status_code != 200:
            try:
                err = json.loads(resp.text)
                code = err.pop("code", 0)
                message = err.pop("message", "unknown error")
                raise DifyApiError(code=code, message=message, **err)
            except json.JSONDecodeError as e:
                raise DifyApiError(message=f"request failed: {resp.status_code}") from e

    def _parse_stream_data(self, resp: requests.Response) -> dict:
        self._handle_error_response(resp)
        client = SSEClient(resp)  # type: ignore
        event = {}
        try:
            for item in client.events():
                event = json.loads(item.data)
                if event["event"] in {"workflow_finished"}:
                    return event
            raise DifyApiError(message=f"run failed: {event}")
        except json.JSONDecodeError as e:
            raise DifyApiError(message="load data from stream failed") from e

    def _parse_resp_data(self, resp: requests.Response) -> dict:
        self._handle_error_response(resp)
        try:
            resp_json = resp.json()
        except ValueError as e:
            raise DifyApiError(message="return content is not JSON data") from e
        return resp_json

    def _get_request_path(self, path: str, path_params: Optional[dict] = None) -> str:
        request_path = path
        for key in self.path_comp.findall(path):
            if path_params is None or key[1:] not in path_params:
                raise DifyApiError(message=f"missing path parameters: {key}")
            request_path = path.replace(key, str(path_params[key[1:]]))
        return request_path

    def request(  # pylint: disable=too-many-arguments
        self,
        path: str,
        user: str,
        *,
        data: Optional[dict] = None,
        files: Optional[dict] = None,
        path_params: Optional[dict] = None,
        http_method: HttpMethod = HttpMethod.POST,
        stream: Optional[bool] = None,
        model: Optional[Type[ModelType]] = None,
    ) -> dict | ModelType:
        request_path = self._get_request_path(path, path_params)
        url = f"{self.api_url}/{request_path}"
        data = self._complete_data(data or {}, user, stream)
        info(f"[request]{self.app_name} {http_method.value}, path: {request_path}, params: {data}, stream: {stream}")
        if http_method == "POST":
            if stream:
                response = requests.post(
                    url, json=data, headers=self.headers, files=files, stream=True, timeout=REQUEST_TIME_OUT
                )
            else:
                response = requests.post(url, json=data, headers=self.headers, files=files, timeout=REQUEST_TIME_OUT)
        else:
            response = requests.get(url, params=data, headers=self.headers, timeout=REQUEST_TIME_OUT)
        if stream:
            parsed_resp = self._parse_stream_data(response)
        else:
            parsed_resp = self._parse_resp_data(response)
        info(
            f"[response]{self.app_name} {http_method.value}, path: {request_path}, "
            f"params: {data}, stream: {stream}, response: {parsed_resp}"
        )
        if model:
            return model.model_validate(parsed_resp)
        return parsed_resp

    def system_request(
        self,
        path: str,
        *,
        data: Optional[dict] = None,
        path_params: Optional[dict] = None,
        http_method: HttpMethod = HttpMethod.GET,
    ) -> dict:
        request_path = self._get_request_path(path, path_params)
        url = f"{self.api_url}/{request_path}"
        info(f"[request] {self.app_name} {http_method.value}, path: {request_path}, params: {data}")
        if http_method == HttpMethod.POST:
            response = requests.post(url, json=data, headers=self.headers, timeout=REQUEST_TIME_OUT)
        elif http_method == HttpMethod.DELETE:
            response = requests.delete(url, json=data, headers=self.headers, timeout=REQUEST_TIME_OUT)
        elif http_method == HttpMethod.PUT:
            response = requests.put(url, json=data, headers=self.headers, timeout=REQUEST_TIME_OUT)
        else:
            response = requests.get(url, params=data, headers=self.headers, timeout=REQUEST_TIME_OUT)
        parsed_resp = self._parse_resp_data(response)
        info(
            f"[response] {self.app_name} {http_method.value}, path: {request_path}, "
            f"params: {data}, response: {parsed_resp}"
        )
        return parsed_resp

    def upload_file(self, user: str, file: dict[str, BinaryIO | tuple]) -> dict:
        """上传文件"""
        return self.request("files/upload", files=file, user=user)

    def get_app_info(self) -> dict:
        """获取应用信息"""
        return self.system_request("info", http_method=HttpMethod.GET)

    def get_app_parameters(self) -> dict:
        """获取应用参数"""
        return self.system_request("parameters", http_method=HttpMethod.GET)

    def get_app_tools(self) -> dict:
        """获取工具icon"""
        return self.system_request("meta", http_method=HttpMethod.GET)
