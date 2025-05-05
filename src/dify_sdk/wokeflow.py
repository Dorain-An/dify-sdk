from typing import Optional

from pydantic import BaseModel

from .base import DifySDK, ModelType
from .constants.base import HttpMethod
from .schema import AsyncWorkResultResponse, WorkFlowResponse


class DifyWorkFlow(DifySDK):
    def _build_data(self, data: dict | ModelType) -> dict:
        if isinstance(data, BaseModel):
            return {"inputs": data.model_dump()}
        return {"inputs": data}

    def run(self, user: str, data: dict | ModelType) -> WorkFlowResponse:
        data = self._build_data(data)
        response = self.request("workflows/run", user, data=data, stream=True, model=WorkFlowResponse)
        return response  # type: ignore

    def sync_run(self, user: str, data: dict | ModelType) -> WorkFlowResponse:
        data = self._build_data(data)
        response = self.request("workflows/run", user, data=data, model=WorkFlowResponse)
        return response  # type: ignore

    def get_work_result(self, user: str, workflow_run_id: str) -> AsyncWorkResultResponse:
        """获取工作结果"""
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
