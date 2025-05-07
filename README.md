# dify sdk
A dify sdk package wrapped with pydantic

English | [简体中文](README.zh_CN.md)

## Best Practices
Pass the request_id as a parameter in the node settings of the Dify app. Then, use the async_run or async_chat method to record the corresponding ID. After a single call ends, send back both the request_id and the operation result through an HTTP callback. This way, you can avoid waiting for the resources occupied by the large model.

### Examples
#### Work Flow
```
from pydify_sdk import DifyWorkFlow

app = DifyWorkFlow("your_app_key", app_name="your_app_name")
user = "user_id" 
data = {"request_id": "XXX", "param": "some words"}  # workflow inputs
app.async_run(user, data)
```
#### Chat Flow
```
from pydify_sdk import DifyChatFlow

app = DifyChatFlow("your_app_key", app_name="your_app_name")
user = "user_id"
query = "some words"  # Chat content
data = {"request_id": "XXX"}
app.async_chat(user, query)
```

## Public API
- upload_file: upload file to dify server
- get_app_info: get the app info
- get_app_parameters: get the app parameters
- get_app_tools: get the tools' icon that the app can use

## Work Flow API
- run: run the workflow with stream response
- sync_run: run the workflow as a regular request(maybe timeout!)
- async_run: run the workflow via http callback(best practices)
- get_work_result: get the work flow run result by task_id
- stop_work: stop the work flow by task_id
- get_logs: get the work flow app logs 

## Chat Flow API
- chat: chat with stream response
- sync_chat: chat as a regular request(maybe timeout!)
- async_chat: chat via http callback(best practices)
- stop_chat: stop the chat by task_id
- feedback_chat: feedback the chat result by message_id
- get_suggested: get next question suggestions by message_id
- get_chat_history: get the chat history by conversation_id
- get_conversations: get the conversations
- delete_conversation: delete the conversation by conversation_id
- delete_chat_history: delete the chat history by conversation_id
- rename_conversation: rename the conversation by conversation_id
- create_annotation: create an annotation
- update_annotation: update the annotation by annotation_id
- delete_annotation: delete the annotation by annotation_id

## Environment Variable Configuration
- DIFY_API_URL: Configure the global dify server address
- DIFY_LOGGER_ON: Configure whether to print logs when initiating requests
