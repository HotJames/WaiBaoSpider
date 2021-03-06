# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/3/23
# @File: proxy_deal.py
# @Software: PyCharm

import json
import redis
from mitmproxy import ctx

rediser = redis.Redis(host='127.0.0.1', port='6379', db=2, )

def response(flow):
    ctx.log.info('>>>>>>>>>>><<<<<<<<<<<<<<<<<')
    url = flow.request.url
    # 网易新闻
    if 'www.ele.me/restapi/v2/pois' in url:
        ctx.log.info('>>>>>>>>>>><<<<<<<<<<<<<<<<<')
        content = flow.response.content
        content_dict = json.loads(content)
        for info in content_dict:
            dl = []
            if info["city_id"] == 1:
                dl.append(str(info["count"]))
                dl.append(info["geohash"])
                dl.append(str(info["longitude"]))
                dl.append(str(info["latitude"]))
                str_add = "#$#$".join(dl)
                rediser.sadd("shanghaiaddr", str_add)
