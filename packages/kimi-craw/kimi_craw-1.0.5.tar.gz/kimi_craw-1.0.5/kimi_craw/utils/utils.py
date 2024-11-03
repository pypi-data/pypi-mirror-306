import qrcode
from io import BytesIO
import random

def generate_qr(id: str) -> BytesIO:
    # id = "csj65ljmvq8nf5ct90b0"
    # device_id = "7431993851172124419"
    device_id = None
    url = f"https://kimi.moonshot.cn/wechat/mp/auth?id={id}&device_id={device_id}"    
    # 生成二维码
    img = qrcode.make(url)
    # 将二维码保存到BytesIO对象中
    buf = BytesIO()
    img.save(buf)
    buf.seek(0)
    print(type(buf))
    return buf

def test2():
    id = "7431993851172124419"
    print(len(id))

def gen_random_num(num_len: int):
    random_number = random.randint(10**(num_len-1), 10**num_len - 1)
    return random_number

if __name__ == "__main__":
    pass
    