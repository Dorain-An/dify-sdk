import json
import logging

import requests
from pydantic import BaseModel
from sseclient import SSEClient

from .base import REQUEST_TIME_OUT, DifyApiError, DifySDK, ModelType
from .constants.base import HttpMethod
from .schema import AsyncWorkResultRequest, AsyncWorkResultResponse, WorkFlowResponse, WorkFlowStopRequest

logger = logging.getLogger(__name__)


class DifyWorkFlow(DifySDK):
    def _build_data(self, data: dict | ModelType) -> dict:
        if isinstance(data, BaseModel):
            return {"inputs": data.model_dump()}
        return {"inputs": data}

    def sync_run(self, user: str, data: dict | ModelType) -> WorkFlowResponse:
        data = self._build_data(data)
        response = self.request("workflows/run", user, data=data, stream=True, model=WorkFlowResponse)
        return response  # type: ignore

    def async_run(self, user: str, data: dict | ModelType) -> tuple[str, str]:
        """
        async run workflow
        @param user: user id
        @param data: workflow input
        @return: workflow_id, workflow_run_id
        """
        data = self._build_data(data)
        request_path = self._get_request_path("workflows/run")
        url = f"{self.api_url}/{request_path}"
        data = self._complete_data(data or {}, user, True)
        logger.info(f"[request]{self.app_name} POST, path: {request_path}, params: {data}, stream: {True}")
        response = requests.post(url, json=data, headers=self.headers, stream=True, timeout=REQUEST_TIME_OUT)
        for item in SSEClient(response).events():  # type: ignore
            event = json.loads(item.data)
            return (event["task_id"], event["workflow_run_id"])
        raise DifyApiError()

    def get_work_result(self, user: str, path_params: AsyncWorkResultRequest) -> AsyncWorkResultResponse:
        return AsyncWorkResultResponse.model_validate(
            self.request(
                "workflows/run/:workflow_run_id",
                user,
                path_params=path_params.model_dump(),
                http_method=HttpMethod.GET,
            )
        )

    def stop_work(self, user: str, path_params: WorkFlowStopRequest) -> None:
        self.request(
            "workflows/run/:task_id/stop",
            user,
            path_params=path_params.model_dump(),
            http_method=HttpMethod.POST,
        )
