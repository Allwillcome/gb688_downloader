import base64
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests
from requests import Response

from .utils import filter_file


class GBCore:
    def get_bytes(self, hcno: str) -> bytes:
        """
        这部分代码可以在对 http://openstd.samr.gov.cn/bzgk/gb/index 网站的手机版预览模式下抓包获得
        :param hcno:
        :return:
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
        }
        text = ""
        for i in range(0, 10):
            if i == 0:
                url = f"http://c.gb688.cn/bzgk/gb/viewGb?type=online&hcno={hcno}"
            else:
                url = f"http://c.gb688.cn/bzgk/gb/viewGb?type=online&hcno={hcno}.00{i}"
            time.sleep(1)

            text += requests.get(url, headers=headers).text
        pdf_bytes = base64.standard_b64decode(text)
        return pdf_bytes

    def _search(self, key: str, page: int = 1, size: int = 25, sort_name: str = 'circulation_date',
                sort_type: str = 'desc') -> Response:
        """国标的下载

        :param key: 搜索内容
        :param page: 当前页数，默认为1
        :param size: 大小，默认为25，仅支持10,25,50三个选项
        :param sort_name: 排序列，默认为 circulation_date（发布日期），还有以下几个参数
            1. standard_no：标准号
            2. caibiao_status：采标状态
            3. cn_name：标准名称
            4. standard_type：类别
            5. status：状态
            6. circulation_date：发布日期
            7. implement_date：实施日期
        :param sort_type: 排序，默认为正序
        :return:
        """
        url = "http://openstd.samr.gov.cn/bzgk/gb/std_list"
        params = {
            "p.p1": 0,
            "p.p90": sort_name,  # 排序列
            "p.p91": sort_type,  # 正序还是倒序
            "p.p2": key,
            'page': page,
            'pageSize': size
        }

        r = requests.get(url, params=params)
        return r

    def search(self, key: str, page: int = 1, size: int = 25, sort_name: str = 'circulation_date',
               sort_type: str = 'desc'):
        """国标的下载

        :param key: 搜索内容
        :param page: 当前页数，默认为1
        :param size: 大小，默认为25，仅支持10,25,50三个选项
        :param sort_name: 排序列，默认为 circulation_date（发布日期），还有以下几个参数
            1. standard_no：标准号
            2. caibiao_status：采标状态
            3. cn_name：标准名称
            4. standard_type：类别
            5. status：状态
            6. circulation_date：发布日期
            7. implement_date：实施日期
        :param sort_type: 排序，默认为正序
        :return:
        """
        r = self._search(key, page, size, sort_name, sort_type)

        total_size = int(re.findall(r'<span class="badge">(\d+)</span>', r.text)[0])

        items = re.findall(r"<tr>([\s\S]*?)</tr>", r.text.replace('\r\n', '').replace('\t', ''))
        records = []
        for item in items[5:-2]:
            data = re.findall(r"<td([\s\S]*?)</td>", item)
            records.append({
                'hcno': re.findall(r"showInfo\('(.+?)'\);", data[1])[0],
                'caibiao_status': data[2] if data[2] != ">  " else "不采标",
                'standard_no': re.findall(r'\);">(.*?)</a>', data[1])[0],
                'cn_name': re.findall(r'\);">(.*?)</a>', data[3])[0],
                'standard_type': data[4].replace('>', ''),
                'status': re.findall('[\u4e00-\u9fa5]{2,4}', data[5])[0],
                'circulation_date': datetime.fromisoformat(data[6][:-2].replace(">", '')),
                'implement_date': datetime.fromisoformat(data[7][:-2].replace(">", ''))
            })
        return {
            'total_size': total_size,
            'records': records
        }


class GB(GBCore):
    def __init__(self):
        super().__init__()

    def save(self, hcno: str, path: Path, pdf_name: str):
        pdf_bytes = self.get_bytes(hcno)

        file_path = path / f"{pdf_name}"
        with open(file_path, "wb") as f:
            f.write(pdf_bytes)
        return file_path

    def get_hcno(self, url: str) -> str:
        """获取hcno

        :param url:
        :return:
        """
        hcno = url.split("?hcno=")[1]
        return hcno

    def can_download(self, hcno: str) -> bool:
        """判断能否下载pdf

        :param hcno:
        :return:
        """
        r = requests.get(f"http://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno={hcno}")
        if "在线预览" in r.text:
            return True
        else:
            return False

    def get_pdf_name(self, hcno: str) -> tuple:
        """获取pdf的名称

        :param hcno: 标准的hcno值
        :return: 返回(标准号，标准名)
        """
        r = requests.get(f"http://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno={hcno}")
        g_name = re.findall(r"标准号：(.*?) </h1></td>", r.text)
        if not g_name:
            g_name = re.findall(r"标准号：(.*?) <span", r.text)

        c_name = re.findall(r"中文标准名称：<b>(.*?)</b></td>", r.text)
        if len(g_name) == 0 or len(c_name) == 0:
            raise Exception("未找到标准号和标准名称")
        return g_name[0], c_name[0]

    def download(self, url: str, folder: Optional[str, Path] = '', name: str = None):
        """下载国标

        :param name:
        :param url:
        :param folder:
        :return:
        """
        try:
            hcno = self.get_hcno(url)
        except IndexError:
            raise Exception("请关注您输入的网站是否包含hcno信息")

        if not self.can_download(hcno):
            raise Exception("该文件源网页无法在线预览，故无法进行下载，请自行打开网页进行查询")

        # 文件处理
        folder = Path(folder)
        try:
            folder.mkdir(exist_ok=True)
        except FileNotFoundError:
            print("请查看该文件的父目录是否已经被创建")

        if name is None:
            g_name, c_name = self.get_pdf_name(hcno)
            name = f"{g_name}({c_name}).pdf"

        pdf_name = filter_file(name)

        path = self.save(hcno, folder, pdf_name)
        return path

    # 说实话这个函数不该放到这个类中
    def format_search_api(self, key: str, page: int = 1, size: int = 25, sort_name: str = 'circulation_date',
                          sort_type: str = 'desc'):
        data = self.search(key, page, size, sort_name, sort_type)
        records = []
        for record in data['records']:
            d = {
                'status': record['status'],
                'key': record['hcno'],
                'name': record['cn_name'],
                'standard_no': record['standard_no'],
                'act_date': record['implement_date'].timestamp() * 1000
            }
            records.append(d)
        return {
            'total_size': data['total_size'],
            'records': records
        }


class GBTools(GB):
    def __init__(self):
        super().__init__()

    def search_and_download(self, key: str, folder):
        """搜索并进行下载

        :param key: 关键词
        :param folder: 保存文件夹
        :return:
        """

        size = 10
        records = self.search(key, page=1, size=10)
        total_size = records['total_size']
        error_record = []

        if total_size == 0:
            print("未找到相关标准")
            exit()

        print(f"共搜索到{total_size}项，开始下载")
        for page in range(1, (total_size // size + 2)):
            print(f"现在正在下载{page}页")
            for record in records['records']:
                try:
                    self.download(f"http://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno={record['hcno']}", folder)
                except Exception as e:
                    print(e)
                    error_record.append(record)
                    continue
