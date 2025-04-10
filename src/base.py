import json
import re
from typing import Optional, BinaryIO, Any
from pydantic import BaseModel
import requests
import logging
from sseclient import SSEClient

from src.schema import AsyncWorkResultRequest
from .config import settings
from .constants.base import HttpMethod

logger = logging.getLogger(__name__)


class DifyApiError(Exception):
    def __init__(self, code: int = 0, message: str = "", **kwargs: dict) -> None:
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
        api_url: str = settings.API_URL,
        app_key: str = settings.APP_KEY,
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
            except json.JSONDecodeError:
                raise DifyApiError(msg=f"request failed: {resp.status_code}")

    def _parse_stream_data(self, resp: requests.Response) -> dict:
        self._handle_error_response(resp)
        client = SSEClient(resp)
        event = {}
        try:
            for item in client.events():
                event = json.loads(item.data)
                if event["event"] in {"workflow_finished", "workflow_failed", ""}:
                    return event["data"]["outputs"]
            else:
                raise DifyApiError(msg=f"run failed: {event}")
        except json.JSONDecodeError as e:
            raise DifyApiError(msg="load data from stream failed") from e

    def _parse_resp_data(self, resp: requests.Response) -> dict:
        self._handle_error_response(resp)
        try:
            resp_json = resp.json()
        except ValueError as e:
            raise DifyApiError(msg="接口错误: 返回内容非JSON数据") from e
        if resp_json.get("success") is not True:
            raise DifyApiError(msg=resp_json.get("errorMsg", ""))
        return resp_json.get("data")

    def _get_request_path(self, path: str, path_params: Optional[dict] = None) -> str:
        request_path = path
        for key in self.path_comp.findall(path):
            if path_params is None or key[1:] not in path_params:
                raise DifyApiError(msg=f"路径参数{key}未设置")
            request_path = path.replace(key, str(path_params[key[1:]]))
        return request_path

    def _parse_error(self, resp: dict) -> None:
        pass

    def request(
        self,
        path: str,
        user: str,
        *,
        data: Optional[dict] = None,
        files: Optional[dict] = None,
        path_params: Optional[dict] = None,
        http_method: HttpMethod = HttpMethod.POST,
        stream: bool = None,
    ) -> Any:
        request_path = self._get_request_path(path, path_params)
        url = f"{self.api_url}/{request_path}"
        data = self._complete_data(data or {}, user, stream)
        logger.info(
            f"[request]{self.app_name} {http_method.value}, path: {request_path}, params: {data}, stream: {stream}"
        )
        if http_method == "POST":
            if stream:
                response = requests.post(
                    url, json=data, headers=self.headers, files=files, stream=True
                )
            else:
                response = requests.post(
                    url, json=data, headers=self.headers, files=files
                )
        else:
            response = requests.get(url, params=data, headers=self.headers)
        if stream:
            parsed_resp = self._parse_stream_data(response)
        else:
            parsed_resp = self._parse_resp_data(response)
        logger.info(
            f"[response]{self.app_name} {http_method.value}, path: {request_path}, params: {data}, stream: {stream}, response: {parsed_resp}"
        )
        self._parse_error(parsed_resp)
        return parsed_resp

    def upload_file(self, user: str, file: dict[str, BinaryIO | tuple]) -> dict:
        return self.request("files/upload", files=file, user=user)


class DifyWorkFlow(DifySDK):
    def _build_data(self, data: dict | BaseModel) -> dict:
        if isinstance(data, BaseModel):
            return {"inputs": data.model_dump()}
        return {"inputs": data}

    def sync_run(self, user: str, data: dict | BaseModel) -> dict:
        data = self._build_data(data)
        return self.request("workflows/run", user, data=data, stream=True)

    def async_run(self, user: str, data: dict | BaseModel) -> str:
        data = self._build_data(data)
        request_path = self._get_request_path("workflows/run")
        url = f"{self.api_url}/{request_path}"
        data = self._complete_data(data or {}, user, True)
        logger.info(
            f"[request]{self.app_name} POST, path: {request_path}, params: {data}, stream: {True}"
        )
        response = requests.post(url, json=data, headers=self.headers, stream=True)
        for event in SSEClient(response).events():
            event = json.loads(event.data)
            return event["workflow_run_id"]

    def get_work_result(self, user: str, path_params: AsyncWorkResultRequest) -> dict:
        return self.request(
            "workflows/run/:workflow_run_id",
            user,
            path_params=path_params.model_dump(),
            http_method=HttpMethod.GET,
        )
