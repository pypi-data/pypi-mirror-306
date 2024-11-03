import requests
import json
import time
from kimi_craw.configs import header_config
from kimi_craw.utils import utils
# 获取游客模式的token
def get_visitor_token():

    # todo
    # 限制太大，没必要写。
    # 还是要写一下，因为后续要做登录需要使用到该接口生成的临时token
    '''
    =======该接口返回=========
    {
        access_token: "ey...",
        refresh_token: "ey...",
    }
    =========================
    只是临时token,可用于游客模式
    '''
    url = "https://kimi.moonshot.cn/api/device/register"
    # headers['Authorization'] = "Bearer "
    res = requests.post(url=url, headers=header_config.base_headers, data=json.dumps({}))
    data = res.json()
    # print(data)
    return data['access_token'] # 只返回access_token就可以

# 生成登录id
# url = https://kimi.moonshot.cn/api/user/wx/register_login POST
# 返回: {"id":"csjdmf0967u4nqsk45vg"}
def get_login_id() -> dict:
    url = "https://kimi.moonshot.cn/api/user/wx/register_login"
    res = requests.post(url=url, headers=header_config.base_headers)
    # print(res.text)
    data = res.json()
    return data['id']

# 获取登录二维码
def get_qrcode(login_id):
    # 1. 获取登录id 
    # login_id = get_login_id()

    # 2. 获取登录二维码
    qr_img = utils.generate_qr(login_id)

    # 3. 返回
    return qr_img

    
# 检查用户是否登录，结合轮询使用
def check_login(login_id: str, tmp_access_token: str) -> dict:
    url = f"https://kimi.moonshot.cn/api/user/wx/register_login/{login_id}"
    headers = header_config.base_headers
    headers['Authorization'] = "Bearer " + tmp_access_token
    res = requests.get(url=url, headers=header_config.base_headers)
    data = res.json()
    return data


if __name__ == '__main__':
    get_login_id()
    