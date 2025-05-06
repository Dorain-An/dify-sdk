from .const_basic import DocStrEnum


class HttpMethod(DocStrEnum):
    GET = ("GET", "GET")
    POST = ("POST", "POST")
    DELETE = ("DELETE", "DELETE")
    PUT = ("PUT", "PUT")


class WorkFlowStatus(DocStrEnum):
    RUNNING = ("running", "运行中")
    SUCCEEDED = ("succeeded", "成功")
    FAILED = ("failed", "失败")
    STOPPED = ("stopped", "中止")


class ChatFlowEvent(DocStrEnum):
    MESSAGE = ("message", "LLM 返回文本块事件")
    MESSAGE_FILE = ("message_file", "文件事件，表示有新文件需要展示")
    MESSAGE_END = ("message_end", "消息结束事件，收到此事件则代表流式返回结束")
    TTS_MESSAGE = ("tts_message", "TTS 音频流事件，即：语音合成输出。")
    TTS_MESSAGE_END = ("tts_message_end", "TTS 音频流结束事件")
    MESSAGE_REPLACE = ("message_replace", "消息内容替换事件")
    WORKFLOW_START = ("workflow_start", "开始事件")
    NODE_START = ("node_start", "节点开始事件")
    NODE_FINISHED = ("node_finished", "节点结束事件")
    WORKFLOW_FINISHED = ("workflow_finished", "结束事件")
    ERROR = ("error", "异常事件")
