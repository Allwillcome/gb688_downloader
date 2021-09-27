import base64
import re
from io import BytesIO
from typing import List, Iterator

import requests
from PyPDF4 import PdfFileReader, PdfFileWriter
from bs4 import BeautifulSoup
from requests import Response
from tqdm import trange

from .GB import GB
from .models import NatureStdModel, NatureStdSearchModel


class NatureStd:
    def __init__(self):
        pass

    def _search(
        self,
        key: str,
        level: str = "",
        status: str = "",
        zxd: str = "",
        pub_std_nature_id: str = "",
        tm_id: int = "",
        page: int = 1,
        size: int = 20,
    ) -> Response:
        """

        :param key: 搜索关键字
        :param level: 标准层级，GB：国家标准，HB：行业标准
        :param status: 标准状态，即将实施，现行，废止
        :param zxd: 制修订，制定，修订
        :param pub_std_nature_id: 标准性质，推荐性，强制性，指导性技术文件
        :param tm_id:归口单位，
            [{
              "text": "自然资源与国土空间规划(TC93)",
              "value": 346
            }, {
              "text": "地理信息(TC230)",
              "value": 757
            }, {
              "text": "海洋(TC283)",
              "value": 874
            }, {
              "text": "珠宝玉石(TC298)",
              "value": 911
            }, {
              "text": "地质矿产调查评价(TC93SC1)",
              "value": 347
            }, {
              "text": "地质灾害防治(TC93SC2)",
              "value": 348
            }, {
              "text": "勘查技术与实验测试(TC93SC3)",
              "value": 349
            }, {
              "text": "国土空间规划(TC93SC4)",
              "value": 350
            }, {
              "text": "土地资源利用(TC93SC5)",
              "value": 351
            }, {
              "text": "自然资源调查监测(TC93SC6)",
              "value": 352
            }, {
              "text": "保护与修复(TC93SC7)",
              "value": 353
            }, {
              "text": "矿产资源利用(TC93SC8)",
              "value": 354
            }, {
              "text": "海域使用及海洋能开发利用(TC283SC1)",
              "value": 875
            }, {
              "text": "海洋调查观测监测(TC283SC2)",
              "value": 876
            }, {
              "text": "海洋生物资源开发与保护(TC283SC3)",
              "value": 877
            }, {
              "text": "海水淡化与综合利用(TC283SC4)",
              "value": 878
            }, {
              "text": "滨海湿地(TC468SC2)",
              "value": 1150
            }, {
              "text": "信息化(TC230SC1)",
              "value": 1561
            }, {
              "text": "测绘(TC230SC2)",
              "value": 1562
            }, {
              "text": "卫星应用(TC230SC3)",
              "value": 1563
            }]
        :param page:
        :param size:
        :return:
        """
        params = {
            "key": key,
            "level": level,
            "pageNo": page,
            "pageSize": size,
            "tmId": tm_id,
            "pubStdNutureId": pub_std_nature_id,
            "repeFlag": status,
            "zxd": zxd,
        }
        r = requests.get("http://www.nrsis.org.cn/portal/xxcx/std", params=params)
        return r

    def parse(self, value) -> Iterator[NatureStdModel]:
        table = BeautifulSoup(value, "html.parser").find(class_="table")
        std_items = []
        for tr in table.find("tbody").find_all("tr"):
            data = tr.find_all("td")
            std_items.append(
                NatureStdModel(
                    code=data[1].text,
                    name=data[2].text,
                    url=f'http://www.nrsis.org.cn{data[2].find("a")["href"]}',
                    pub_time=data[3].text,
                    act_time=data[4].text,
                    status=data[5].text,
                )
            )
        return std_items

    def get_total_size(self, value: str) -> int:
        return int(re.findall(r"共(.*?)条数据，每页显示", value)[0])

    def search(
        self,
        key: str,
        level: str = "",
        status: str = "",
        zxd: str = "",
        pub_std_nuture_id: str = "",
        tm_id: int = "",
        page: int = 1,
        size: int = 20,
    ) -> NatureStdSearchModel:
        """

        :param key: 搜索关键字
        :param level: 标准层级，GB：国家标准，HB：行业标准
        :param status: 标准状态，即将实施，现行，废止
        :param zxd: 制修订，制定，修订
        :param pub_std_nuture_id: 标准性质，推荐性，强制性，指导性技术文件
        :param tm_id:归口单位，
            [{
              "text": "自然资源与国土空间规划(TC93)",
              "value": 346
            }, {
              "text": "地理信息(TC230)",
              "value": 757
            }, {
              "text": "海洋(TC283)",
              "value": 874
            }, {
              "text": "珠宝玉石(TC298)",
              "value": 911
            }, {
              "text": "地质矿产调查评价(TC93SC1)",
              "value": 347
            }, {
              "text": "地质灾害防治(TC93SC2)",
              "value": 348
            }, {
              "text": "勘查技术与实验测试(TC93SC3)",
              "value": 349
            }, {
              "text": "国土空间规划(TC93SC4)",
              "value": 350
            }, {
              "text": "土地资源利用(TC93SC5)",
              "value": 351
            }, {
              "text": "自然资源调查监测(TC93SC6)",
              "value": 352
            }, {
              "text": "保护与修复(TC93SC7)",
              "value": 353
            }, {
              "text": "矿产资源利用(TC93SC8)",
              "value": 354
            }, {
              "text": "海域使用及海洋能开发利用(TC283SC1)",
              "value": 875
            }, {
              "text": "海洋调查观测监测(TC283SC2)",
              "value": 876
            }, {
              "text": "海洋生物资源开发与保护(TC283SC3)",
              "value": 877
            }, {
              "text": "海水淡化与综合利用(TC283SC4)",
              "value": 878
            }, {
              "text": "滨海湿地(TC468SC2)",
              "value": 1150
            }, {
              "text": "信息化(TC230SC1)",
              "value": 1561
            }, {
              "text": "测绘(TC230SC2)",
              "value": 1562
            }, {
              "text": "卫星应用(TC230SC3)",
              "value": 1563
            }]
        :param page:
        :param size:
        :return:
        """
        text = self._search(
            key=key,
            level=level,
            status=status,
            zxd=zxd,
            pub_std_nature_id=pub_std_nuture_id,
            tm_id=tm_id,
            page=page,
            size=size,
        ).text
        total_size = self.get_total_size(text)
        if total_size == 0:
            data = []
        else:
            data = self.parse(text)
        return NatureStdSearchModel(total_size, data)

    def get_pdf_info(self, url: str) -> dict:
        text = requests.get(url).text
        target_url = re.findall(r"readPdf\('(.*?)'\)", text)[0]
        is_gb = False
        if "gb688" in target_url:
            is_gb = True
        return {
            "target_url": target_url,  # 目标地址，如果是国标则为gb688，否则就是pdf的地址
            "is_gb": is_gb,  # 是否为国标
        }

    def _get_pdf_page_size(self, url: str) -> int:
        r = requests.get(url)
        page = re.findall(r"size : parseInt\('(.*?)'\)", r.text)[0]
        return int(page)

    def _get_one_page_pdf(self, code: str, page: int) -> BytesIO:
        data = {
            "code": code,
            "page": page,
        }
        r = requests.post("http://www.nrsis.org.cn/mnr_kfs/file/readPage", data=data)
        return BytesIO(base64.standard_b64decode(r.text))

    def _download(self, url, path):
        code = url.split("/")[-1]
        page_size = self._get_pdf_page_size(url)

        pdf_writer = PdfFileWriter()

        for page in trange(1, page_size + 1):
            first_page_io = self._get_one_page_pdf(code, page)
            pdf_reader = PdfFileReader(first_page_io)
            page_r = pdf_reader.getPage(0)
            pdf_writer.addPage(page_r)

        with open(path, "wb") as f:
            pdf_writer.write(f)
        return path

    def download(self, url: str, path):
        print(url)
        pdf_info = self.get_pdf_info(url)

        if pdf_info["is_gb"]:
            gb = GB()
            path = gb._download(pdf_info["target_url"], path)
        else:
            path = self._download(pdf_info["target_url"], path)

        return path
