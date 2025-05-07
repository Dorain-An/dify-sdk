# dify sdk
一个用pydantic封装的 Dify 软件开发工具包

[English](README.md) | 简体中文

## 最佳实践
dify app节点设置参数传入request_id，并结合async_run或者async_chat方法记录对应的id，在一次调用结束后，以http回调的方式同时传回request_id和运行结果，以会免于等待大模型占用的资源

### 例子
#### Work Flow
```
from dify_sdk import DifyWorkFlow

app = DifyWorkFlow("your_app_key", app_name="your_app_name")
user = "user_id" 
data = {"request_id": "XXX", "param": "some words"}  # workflow inputs
app.async_run(user, data)
```
#### Chat Flow
```
from dify_sdk import DifyChatFlow

app = DifyChatFlow("your_app_key", app_name="your_app_name")
user = "user_id"
query = "some words"  # Chat content
data = {"request_id": "XXX"}
app.async_chat(user, query)
```

## 通用API
- upload_file: 上传文件到dify服务器
- get_app_info: 获取app信息
- get_app_parameters: 获取app参数
- get_app_tools: 获取app可以使用的工具icon

## Work Flow API
- run: 以流式请求运行workflow
- sync_run: 常规请求方式运行workflow(可能超时!)
- async_run: 以http回调的方式运行workflow(最佳实践)
- get_work_result: 通过task_id获取workflow运行结果
- stop_work: 通过task_id停止workflow
- get_logs: 获取workflow运行日志

## Chat Flow API
- chat: 以流式请求对话
- sync_chat: 常规请求方式对话(可能超时!)
- async_chat: 以http回调的方式进行对话(最佳实践)
- stop_chat: 通过task_id停止对话
- feedback_chat: 通过message_id反馈对话结果
- get_suggested: 通过message_id获取下一个问题建议
- get_chat_history: 通过conversation_id获取对话历史
- get_conversations: 获取对话列表
- delete_conversation: 通过conversation_id删除对话
- delete_chat_history: 通过conversation_id删除对话历史
- rename_conversation: 通过conversation_id重命名对话
- create_annotation: 创建标注
- update_annotation: 通过annotation_id更新标注
- delete_annotation: 通过annotation_id删除标注

## 环境变量设置
- DIFY_API_URL: 配置全局的 Dify 服务器地址
- DIFY_LOGGER_ON: 配置发起请求时是否打印日志
