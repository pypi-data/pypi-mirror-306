import requests
import json
import time
from kimi_craw.configs import header_config
from kimi_craw.utils import utils
import uuid


# 创建一个chat, 返回chat_id
def create_chat(access_token:str) -> str:
    
    url = "https://kimi.moonshot.cn/api/chat"
    headers=header_config.base_headers
    headers['Authorization'] = "Bearer " + access_token
    data = {
        "name": str(uuid.uuid4()),
        "is_example": False,
        "enter_method": "new_chat",
        "kimiplus_id": "kimi"
    }
    res = requests.post(url=url, headers=headers, data=json.dumps(data))
    data = res.json()
    # print(data)
    return data['id']

def chat(access_token: str, chat_id: str, query: str):
    url = f"https://kimi.moonshot.cn/api/chat/{chat_id}/completion/stream"
    headers=header_config.base_headers
    headers['Authorization'] = "Bearer " + access_token
    data = {
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ],
        "use_search": True,
        "extend": {
            "sidebar": True
        },
        "kimiplus_id": "kimi",
        "use_research": True,
        "refs": [],
        "refs_file": []
    }
    data = json.dumps(data)
    response = requests.post(url=url, headers=header_config.base_headers, data=data)
    temp_data = ""
    # print(response.text)
    # response.encoding = "utf-8"
    for chunk in response.iter_content(chunk_size=1):
        # print(chunk)
        temp_data += chunk.decode('utf-8', errors='replace')
        if temp_data.endswith('\n\n'):
            temp_data = temp_data.split('data:')[1]
            temp_json = json.loads(temp_data)
            # rec_data_list.append(temp_json)
            # print(temp_json)
            yield temp_data
            temp_data = ""
            