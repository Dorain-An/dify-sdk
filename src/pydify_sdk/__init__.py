import importlib
import inspect

from pydify_sdk.chatflow import DifyChatFlow  # noqa: F401
from pydify_sdk.constants.base import ChatFlowEvent  # noqa: F401
from pydify_sdk.constants.input import AudioType, DocumentType, ImageType, TransferMethod, VideoType  # noqa: F401
from pydify_sdk.wokeflow import DifyWorkFlow  # noqa: F401

schema_module = importlib.import_module("pydify_sdk.schema")
all_schemas = [
    name for name, obj in inspect.getmembers(schema_module, inspect.isclass) if obj.__module__ == schema_module.__name__
]

# 动态导入所有类
for name in all_schemas:
    globals()[name] = getattr(schema_module, name)


__all__ = [
    # sdk
    "DifyWorkFlow",
    "DifyChatFlow",
    # constants
    "ChatFlowEvent",
    "DocumentType",
    "ImageType",
    "VideoType",
    "AudioType",
    "TransferMethod",
] + all_schemas
