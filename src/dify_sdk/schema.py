import json
from typing import Optional, Self

from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator

from .constants.base import WorkFlowStatus
from .constants.input import (
    AudioType,
    DocumentType,
    ImageType,
    TransferMethod,
    VideoType,
)


class FileInput(BaseModel):
    type: DocumentType | ImageType | AudioType | VideoType | str = Field(..., description="The type of the file")
    transfer_method: TransferMethod = Field(..., description="The transfer method of the file")
    url: Optional[str] = Field(None, description="The URL of the file")
    upload_file_id: Optional[str] = Field(None, description="The ID of the uploaded file")

    @model_validator(mode="after")
    def check_url_or_upload_file_id(self) -> Self:
        if self.transfer_method == TransferMethod.URL and self.url is None:
            raise ValidationError("url must be provided if transfer_method is remote_url")
        if self.transfer_method == TransferMethod.FILE and self.upload_file_id is None:
            raise ValidationError("upload_file_id must be provided if transfer_method is local_file")
        return self


class AsyncWorkResultRequest(BaseModel):
    workflow_run_id: str = Field(..., description="The ID of the workflow run")


class AsyncWorkResultResponse(BaseModel):
    id: str = Field(..., description="The ID of the workflow run")
    workflow_id: str = Field(..., description="The ID of the workflow")
    status: WorkFlowStatus = Field(..., description="The status of the workflow run")
    inputs: dict = Field(default={}, description="The input of the workflow run") 
    outputs: dict = Field(default={}, description="The output of the workflow run")
    error: Optional[str] = Field(default=None, description="The error of the workflow run")
    total_steps: int = Field(..., description="The total steps of the workflow run")
    total_tokens: int = Field(..., description="The total tokens of the workflow run")
    created_at: int = Field(..., description="The created timestamp of the workflow run")
    finished_at: Optional[int] = Field(..., description="The finished timestamp of the workflow run")
    elapsed_time: float = Field(..., description="The elapsed time of the workflow run")

    @field_validator("inputs", "outputs", mode="before")
    @classmethod
    def check(cls, value: str | dict) -> dict:
        if isinstance(value, str):
            return json.loads(value)
        return value
    

class WorkFlowResponse(BaseModel):
    task_id: str = Field(..., description="The ID of the workflow run")
    workflow_run_id: str = Field(..., description="The ID of the workflow run")
    data: AsyncWorkResultResponse = Field(..., description="The data of the workflow run")


class WorkFlowStopRequest(BaseModel):
    task_id: str = Field(..., description="The ID of the workflow run")
