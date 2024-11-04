import asyncio
import json
from base64 import b64encode, b64decode
from urllib.parse import quote

from hssp.logger.log import Logger, hssp_logger
from hssp.network import Net
from hssp.network.response import Response
from hssp.utils import crypto


def url_encode_to_bytes(s):
    encoded = quote(s)
    bytes_arr = []
    i = 0
    while i < len(encoded):
        char = encoded[i]
        if char == '%':
            hex_value = encoded[i + 1:i + 3]
            byte = int(hex_value, 16)
            bytes_arr.append(byte)
            i += 3
        else:
            bytes_arr.append(ord(char))
            i += 1
    return bytes(bytes_arr)


def decrypt_resp(response_data: Response):
    """
    解密响应数据
    Args:
        response_data: 响应数据

    Returns:

    """
    data = response_data.json.get('data')
    key_string = 'vEukA&w15z4VAD3kAY#fkL#rBnU!WDhN'
    prefix_length = 12
    data_byte = b64decode(data)

    data_prefix = data_byte[:prefix_length]
    key_string_encode = url_encode_to_bytes(key_string) + data_prefix
    u = len(key_string_encode) // 2

    hash_value = crypto.sha256_hash(key_string_encode, "bytes")[8:8 + 16]

    g = hash_value + key_string_encode[:u]
    y = crypto.sha256_hash(g, "bytes")

    b = key_string_encode[22:44] + hash_value
    e = crypto.sha256_hash(b, "bytes")

    key = y[:8] + e[8: 8 + 16] + y[8 + 16:8 + 16 + 24]
    iv = e[:4] + y[12:12 + 8] + e[-4:]

    data = crypto.decrypt_aes_256_cbc_pad7(data_byte[prefix_length:], key, iv)
    response_data.json['data'] = json.loads(data)


async def main():
    category = {
        17847: "萝莉少女-娇喘连连易推倒",
        23042: "真实破处",
        17972: "猎奇请进",
        17860: "麻豆传媒",
    }

    net = Net()
    net.response_after_signal.connect(decrypt_resp)
    resp = await net.post(
        "https://h5dfsg.anwangjd1.com/api/app/media/topic/details",
        headers={
            'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJwdWJsaWMiLCJleHAiOjE3Mjc0OTkzOTgsImlzc3VlciI6ImNvbS5idXR0ZXJmbHkiLCJzdWIiOiJhc2lnbiIsInVzZXJJZCI6Nzc2NDczNX0.c6I3SzQemjhgt-FTAh1XDto5Jwi6mnBEPXU6SWFz0OQ'
        },
        json_data={"id": 17860, "mediaType": 1, "pageNum": 1, "pageSize": 50, "sort": 0}
    )
    logger.info(f"data: {resp.json}")
    await net.close()


if __name__ == '__main__':
    Logger.init_logger()
    logger = hssp_logger.getChild("极乐禁地")
    asyncio.run(main())
