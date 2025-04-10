from typing import Optional
from pydantic import BaseModel, Field, field_validator, ValidationError
from .constants.input import (
    DocumentType,
    ImageType,
    AudioType,
    VideoType,
    TransferMethod,
)


class FileInput(BaseModel):
    type: DocumentType | ImageType | AudioType | VideoType | str = Field(
        ..., description="The type of the file"
    )
    transfer_method: TransferMethod = Field(
        ..., description="The transfer method of the file"
    )
    url: Optional[str] = Field(None, description="The URL of the file")
    upload_file_id: Optional[str] = Field(
        None, description="The ID of the uploaded file"
    )

    @field_validator("url", "upload_file_id", mode="before")
    @classmethod
    def check_url_or_upload_file_id(cls, v, values):
        if values.get("transfer_method") == TransferMethod.URL and v is None:
            raise ValidationError(
                "url must be provided if transfer_method is remote_url"
            )
        if values.get("transfer_method") == TransferMethod.FILE and v is None:
            raise ValidationError(
                "upload_file_id must be provided if transfer_method is local_file"
            )


class AsyncWorkResultRequest(BaseModel):
    workflow_run_id: str = Field(..., description="The ID of the workflow run")
