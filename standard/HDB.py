from pathlib import Path
from typing import Union, Literal

import requests
from requests import Response

from .utils import filter_file

TYPE_MODE = Literal["hbba", "dbba"]
STATUS = Literal["", "现行", "有更新版", "废止"]


class HDBCore:
    def __init__(self, t: TYPE_MODE):
        """

        :param t: 区分行业或地区标准，参数，行业标准：hbba、地方标准：dbba
        """
        if t not in {'hbba', 'dbba'}:
            raise Exception("t参数错误，请查询文档")
        self.type = t

    def _search(self, key: str, status: STATUS = '', pubdate: str = '', ministry: str = '', industry: str = '',
                current: int = 1, size: int = 15) -> Response:
        """这个函数用来对地方标准进行搜索，当值为空时，则默认为全部

        :param key: 搜索关键词
        :param status: 标准的状态，有以下几个状态：''、'现行'、'有更新版'、'废止'，默认查询全部
        :param pubdate: 备案日期，''、'-1'、'-3'、'-6'、'-12'、'-24'。这里的数字是代表一个月，即一个月内备案的标准，默认查询全部
        :param ministry: 地区代号请参考文档，默认查询全部
        :param industry: 行业代号请参考文档，默认查询全部
        :param current:
        :param size:
        :return:
        """
        url = f"http://{self.type}.sacinfo.org.cn/stdQueryList"
        data = {
            'current': current,
            'size': size,
            'key': key,
            'status': status,
            'ministry': ministry,
            'industry': industry,
            'pubdate': pubdate,
            'date': ''
        }

        r = requests.post(url, data=data)
        return r

    def get_file_response(self, pk: str) -> Response:
        url = f'http://{self.type}.sacinfo.org.cn/attachment/downloadStdFile?pk={pk}'
        r = requests.get(url)
        return r


class HDB(HDBCore):
    def __init__(self, t: TYPE_MODE):
        """

        :param t: 区分行业或地区标准，参数，行业标准：hbba、地方标准：dbba
        """
        super(HDB, self).__init__(t)

        if t not in {'hbba', 'dbba'}:
            raise Exception("t参数错误，请查询文档")
        self.type = t

    def can_download(self, pk: str) -> bool:
        r = self.get_file_response(pk)

        if len(r.content) == 0:
            return False
        else:
            return True

    def download(self, pk: str, name: str, folder: Union[str, Path] = '.') -> Path:
        """

        :param pk:
        :param name:
        :param folder:
        :return:
        """
        name = filter_file(name)
        folder = Path(folder)
        try:
            folder.mkdir(exist_ok=True)
        except FileNotFoundError:
            print("请查看该文件的父目录是否已经被创建")

        file_path = folder / f'{name}.pdf'

        r = self.get_file_response(pk)

        if len(r.content) == 0:
            raise Exception("该文件源网页无法下载")

        with open(file_path, 'wb') as f:
            f.write(r.content)

        return file_path

    def search(self, key: str, status: STATUS = '', pubdate: str = '', ministry: str = '', industry: str = '',
               current: int = 1, size: int = 15):
        return self._search(key, status, pubdate, ministry, industry, current, size).json()

    def format_search_api(self, key: str, status: STATUS = '', pubdate: str = '', ministry: str = '', industry: str = '',
                          page: int = 1, size: int = 15):
        data = self.search(key, status, pubdate, ministry, industry, page, size)
        records = []
        for record in data['records']:
            d = {
                'status': record['status'],
                'key': record['pk'],
                'name': record['chName'],
                'standard_no': record['code'],
                'act_date': record['actDate']
            }
            records.append(d)
        return {
            'pages': page,
            'total_size': data['total'],
            'records': records
        }


class HDBTools(HDB):
    def __init__(self, t: TYPE_MODE):
        super(HDBTools, self).__init__(t)

    def download_all(self, records, total, path, key) -> object:
        """下载所有记录

        :param key:
        :param records:
        :param total:
        :param path:
        :return:
        """
        if path is None:
            path = filter_file(key)

        error_record = []
        for record in records:
            name = f'{record["code"]}({record["chName"]})'
            try:
                print(f"正在下载{name}")
                self.download(pk=record['pk'], name=name, folder=path)
            except Exception:
                print(f"{name}下载失败")
                error_record.append(record)

        print(f"共{len(records)}条记录，成功{len(records) - len(error_record)}条，失败{len(error_record)}条")
        print(error_record)
        return {
            'total': total,
            'error_code': error_record
        }

    def search_and_download(self, key: str, path=None):
        """搜索关键字并下载所有内容

        :param key: 关键字
        :param path: 路径
        :return:
        """
        total = self._search(key, current=1, size=100).json()['total']
        records = self._search(key, current=1, size=total).json()['records']
        if not records:
            return False

        return self.download_all(records, total, path, key)
