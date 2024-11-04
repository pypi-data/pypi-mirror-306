import asyncio

from hssp.logger.log import Logger
from hssp import Net


async def main():
    net = Net()
    url = "http://5yqmu9zt.z88gvbz02msvjwe2.ph.faypb.cn/api/v1/app/votes?stage_code=BM8ffv5we6"
    headers = {
        "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC81eXFtdTl6dC56ODhndmJ6MDJtc3Zqd2UyLnBoLmZheXBiLmNuXC9hcHBcL2F1dGhcLzk1ODk0MDciLCJpYXQiOjE3Mjg5NjQzMjUsImV4cCI6MTczMTU1NjMyNSwibmJmIjoxNzI4OTY0MzI1LCJqdGkiOiJXOEdSeWVla0FFbXA0OEZvIiwic3ViIjo5NTg5NDA3LCJwcnYiOiI1ODkzZWZlMTc4ZmJiNGVhZmI5ODRkMzE5NjA3N2MzNDQxMjI0MzYzIiwiYXBwaWQiOiJ3eGJiMjA2NzY1YjI0Y2UxZDkiLCJndWFyZCI6ImFwcCJ9.3RTgBecTI2tHwAVo5jcYHQbblWG-2gqIfHbpU83dw48",
        "origin": "http://5yqmu9zt.z88gvbz02msvjwe2.ph.faypb.cn",
        "host": "5yqmu9zt.z88gvbz02msvjwe2.ph.faypb.cn",
        "user-agent": "Mozilla/5.0 (Linux; Android 14; V2172A Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.188 Mobile Safari/537.36 XWEB/1260183 MMWEBSDK/20240501 MMWEBID/172 MicroMessenger/8.0.50.2701(0x2800325B) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64"
    }
    data = {
        "player_ids": ["453706"]
    }
    params = {
        "stage_code": "BM8ffv5we6"
    }

    proxy = 'http://a01c69ff:6ff0572c7455417fa81cb2577ca817ef@cellular.proxy.acedata.cloud:30000'

    resp = await net.post(url, headers=headers, json_data=data, params=params, proxy=proxy)
    logger.info(resp.json)
    await net.close()


if __name__ == '__main__':
    Logger.init_logger()
    logger = Logger.get_logger("test")
    asyncio.run(main())
