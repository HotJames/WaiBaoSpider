# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/1/7
# @File: base.py
# @Software: PyCharm

import scrapy
from scrapy import Request
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os


class DeYangSpider(scrapy.Spider):
    name = "deyang"
    base_url = "http://www.deyang.gov.cn/appeal/list.jsp?model_id=1&cur_page={}&tm_id=595"
    data_path = os.getcwd() + "/WaiBaoSpider/data/"
    if os.path.exists(data_path):
        pass
    else:
        os.mkdir(data_path)
    dump_list = CSVDumper(data_path + "%s_list.csv" % name)
    dump_detail = CSVDumper(data_path + "%s_detail.csv" % name)
    custom_settings = {
        # 'DOWNLOAD_DELAY': 1,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }

    def start_requests(self):
        for i in range(1, 539):
            # for i in range(1, 2):
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//tr[@class='onmousemove']")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"信件主题"] = info.xpath(".//th[@class='thCss']/a/text()")[0].strip() if info.xpath(
                ".//th[@class='thCss']/a/text()") else ""
            item[u"处理状态"] = info.xpath("./th[2]/text()")[0].strip() if info.xpath("./th[2]/text()") else ""
            item[u"来信人"] = info.xpath("./th[3]/text()")[0].strip() if info.xpath("./th[3]/text()") else ""
            item[u"办结日期"] = info.xpath(".//th[@class='oneDate']/text()")[0].strip() if info.xpath(
                ".//th[@class='oneDate']/text()") else ""
            item[u"写信日期"] = info.xpath(".//th[@class='twoDate']/text()")[0].strip() if info.xpath(
                ".//th[@class='twoDate']/text()") else ""
            item[u"链接"] = "http://www.deyang.gov.cn{}".format(
                info.xpath(".//th[@class='thCss']/a/@href")[0].strip() if info.xpath(
                    ".//th[@class='thCss']/a/@href") else "")
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers, meta={"url": item[u"链接"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"信件主题"] = html.xpath("//div[@class='title']/h1/text()")[0].strip() if html.xpath(
            "//div[@class='title']/h1/text()") else ""
        item[u"来信人"] = html.xpath("//div[@class='form']/table/tr[2]/td[2]/text()")[0].strip() if html.xpath(
            "//div[@class='form']/table/tr[2]/td[2]/text()") else ""
        item[u"来信日期"] = html.xpath("//div[@class='form']/table/tr[2]/td[4]/text()")[0].strip() if html.xpath(
            "//div[@class='form']/table/tr[2]/td[4]/text()") else ""
        item[u"类型"] = html.xpath("//div[@class='form']/table/tr[3]/td[2]/text()")[0].strip() if html.xpath(
            "//div[@class='form']/table/tr[3]/td[2]/text()") else ""
        item[u"编号"] = html.xpath("//div[@class='form']/table/tr[3]/td[4]/text()")[0].strip() if html.xpath(
            "//div[@class='form']/table/tr[3]/td[4]/text()") else ""
        item[u"来信内容"] = html.xpath("//div[@class='form']/table/tr[4]/td[2]//text()") if html.xpath(
            "//div[@class='form']/table/tr[4]/td[2]//text()") else []
        item[u"来信内容"] = deal_ntr("".join(item[u"来信内容"]))
        item[u"回复部门"] = html.xpath("//div[@class='form']/table/tr[6]/td[2]/text()")[0].strip() if html.xpath(
            "//div[@class='form']/table/tr[6]/td[2]/text()") else ""
        item[u"回复时间"] = html.xpath("//div[@class='form']/table/tr[7]/td[2]/text()")[0].strip() if html.xpath(
            "//div[@class='form']/table/tr[7]/td[2]/text()") else ""
        item[u"答复内容"] = html.xpath("//div[@class='form']/table/tr[8]/td[2]//text()") if html.xpath(
            "//div[@class='form']/table/tr[8]/td[2]//text()") else []
        item[u"答复内容"] = deal_ntr("".join(item[u"答复内容"]))
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
