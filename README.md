# dify skd

## Examples
### Work Flow
```
from pydify_sdk import DifyWorkFlow

app = DifyWorkFlow("your_app_key", app_name="xxx")
user = "me" 
data = {"q1": "text"}  # workflow inputs
app.run(user, data)
```
### Chat Flow
```
from pydify_sdk import DifyChatFlow

app = DifyChatFlow("your_app_key", app_name="xxx")
user = "me"
query = "hello"  # Chat content
app.chat(user, query)
```
## Environment Variable Configuration
- DIFY_API_URL: Configure the global dify server address.
- DIFY_LOGGER_ON: Configure whether to print logs when initiating requests.
