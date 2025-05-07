import json
from typing import Optional

import requests
from pydantic import BaseModel
from sseclient import SSEClient

from .base import REQUEST_TIME_OUT, DifySDK, ModelType
from .constants.base import HttpMethod
from .schema import AsyncWorkResultResponse, WorkFlowResponse


class DifyWorkFlow(DifySDK):
    def _build_data(self, data: dict | ModelType | None) -> dict:
        if isinstance(data, BaseModel):
            return {"inputs": data.model_dump()}
        return {"inputs": data or {}}

    def run(self, user: str, data: dict | ModelType | None) -> WorkFlowResponse:
        """
        运行工作流(流式返回)
        @return: WorkFlowResponse
        """
        data = self._build_data(data)
        response = self.request("workflows/run", user, data=data, stream=True, model=WorkFlowResponse)
        return response  # type: ignore

    def sync_run(self, user: str, data: dict | ModelType | None) -> WorkFlowResponse:
        """
        运行工作流(同步返回)
        @return: WorkFlowResponse
        """
        data = self._build_data(data)
        response = self.request("workflows/run", user, data=data, model=WorkFlowResponse)
        return response  # type: ignore

    def async_run(self, user: str, data: dict | ModelType | None) -> tuple[str, str]:
        """
        以http回调的方式运行工作流
        @return: (task_id, workflow_run_id)
        """
        url = f"{self.api_url}/workflows/run"
        data = self._complete_data(self._build_data(data), user, True)
        resp = requests.post(url, json=data, headers=self.headers, stream=True, timeout=REQUEST_TIME_OUT)
        self._handle_error_response(resp)
        task_id = workflow_run_id = ""
        client = SSEClient(resp)  # type: ignore
        for item in client.events():
            event = json.loads(item.data)
            task_id = event.get("task_id", "")
            workflow_run_id = event.get("workflow_run_id", "")
            break
        return task_id, workflow_run_id

    def get_work_result(self, user: str, workflow_run_id: str) -> AsyncWorkResultResponse:
        """
        获取工作结果
        @return: AsyncWorkResultResponse
        """
        return AsyncWorkResultResponse.model_validate(
            self.request(
                "workflows/run/:workflow_run_id",
                user,
                path_params={"workflow_run_id": workflow_run_id},
                http_method=HttpMethod.GET,
            )
        )

    def stop_work(self, user: str, task_id: str) -> None:
        """停止工作流"""
        self.request(
            "workflows/run/:task_id/stop",
            user,
            path_params={"task_id": task_id},
            http_method=HttpMethod.POST,
        )

    def get_logs(self, page: int = 1, limit: int = 20, *, status: Optional[str] = None) -> dict:
        """获取workflow日志"""
        return self.system_request(
            "workflows/logs", data={"page": page, "limit": limit, "status": status}, http_method=HttpMethod.GET
        )
