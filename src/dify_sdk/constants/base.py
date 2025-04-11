from .const_basic import DocStrEnum


class HttpMethod(DocStrEnum):
    GET = ("GET", "GET")
    POST = ("POST", "POST")


class WorkFlowStatus(DocStrEnum):
    RUNNING = ("running", "运行中")
    SUCCEEDED = ("succeeded", "成功")
    FAILED = ("failed", "失败")
    STOPPED = ("stopped", "中止")
