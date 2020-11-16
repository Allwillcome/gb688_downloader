from typing import Literal

import requests
from requests import Response

from .errors import DownloadError
from .models import HDBModel, HDBSearchModel

TYPE_MODE = Literal["hbba", "dbba"]
STATUS = Literal["", "现行", "有更新版", "废止"]


class HDBCore:
    def __init__(self, t: TYPE_MODE):
        """

        :param t: 区分行业或地区标准，参数，行业标准：hbba、地方标准：dbba
        """
        if t not in {"hbba", "dbba"}:
            raise Exception("参数错误，只支持 hbba 和 dbba 两种参数")
        self.type = t

    def _search(
        self,
        key: str,
        status: STATUS = "",
        pubdate: str = "",
        ministry: str = "",
        industry: str = "",
        page: int = 1,
        size: int = 15,
    ) -> Response:
        """这个函数用来对地方标准进行搜索，当值为空时，则默认为全部

        :param key: 搜索关键词
        :param status: 标准的状态，有以下几个状态：''、'现行'、'有更新版'、'废止'，默认查询全部
        :param pubdate: 备案日期，''、'-1'、'-3'、'-6'、'-12'、'-24'。这里的数字是代表一个月，即一个月内备案的标准，默认查询全部
        :param ministry: 地区代号请参考文档，默认查询全部
        :param industry: 行业代号请参考文档，默认查询全部
        :param page:
        :param size:
        :return:
        """
        url = f"http://{self.type}.sacinfo.org.cn/stdQueryList"
        data = {
            "current": page,
            "size": size,
            "key": key,
            "status": status,
            "ministry": ministry,
            "industry": industry,
            "pubdate": pubdate,
            "date": "",
        }

        r = requests.post(url, data=data)
        return r

    def get_file_response(self, pk: str) -> Response:
        url = f"http://{self.type}.sacinfo.org.cn/attachment/downloadStdFile?pk={pk}"
        r = requests.get(url)
        if len(r.content) == 0:
            raise DownloadError("该文件不支持下载")
        return r


class HDB(HDBCore):
    def __init__(self, t: TYPE_MODE):
        """

        :param t: 区分行业或地区标准，参数，行业标准：hbba、地方标准：dbba
        """
        super(HDB, self).__init__(t)

        if t not in {"hbba", "dbba"}:
            raise Exception("t参数错误，请查询文档")
        self.type = t

    def download(self, url, path):
        pk = url.split("/")[-1]
        r = self.get_file_response(pk)

        with open(path, "wb") as f:
            f.write(r.content)

        return path

    def search(
        self,
        key: str,
        status: STATUS = "",
        pubdate: str = "",
        ministry: str = "",
        industry: str = "",
        page: int = 1,
        size: int = 15,
    ):
        r = self._search(key, status, pubdate, ministry, industry, page, size).json()
        records = []
        for record in r["records"]:
            records.append(
                HDBModel(
                    name=record["chName"],
                    code=record["code"],
                    pub_time=record["issueDate"],  # TODO:需要修改为date类型，现在是13位时间戳
                    act_time=record["actDate"],
                    status=record["status"],
                    pk=record["pk"],
                    url=f"http://{self.type}.sacinfo.org.cn/stdDetail/{record['pk']}",
                    charge_department=record["chargeDept"],
                    industry=record["industry"],
                    std_type=self.type,
                )
            )
        return HDBSearchModel(total_size=r["total"], data=records)


# TODO:加入 tutorial
# def download_all(self, records, total, path, key) -> object:
#     """下载所有记录
#
#     :param key:
#     :param records:
#     :param total:
#     :param path:
#     :return:
#     """
#     if path is None:
#         path = filter_file(key)
#
#     error_record = []
#     for record in records:
#         name = f'{record["code"]}({record["chName"]})'
#         try:
#             print(f"正在下载{name}")
#             self.download(pk=record['pk'], name=name, folder=path)
#         except Exception:
#             print(f"{name}下载失败")
#             error_record.append(record)
#
#     print(f"共{len(records)}条记录，成功{len(records) - len(error_record)}条，失败{len(error_record)}条")
#     print(error_record)
#     return {
#         'total': total,
#         'error_code': error_record
#     }
#
# def search_and_download(self, key: str, path=None):
#     """搜索关键字并下载所有内容
#
#     :param key: 关键字
#     :param path: 路径
#     :return:
#     """
#     total = self._search(key, current=1, size=100).json()['total']
#     records = self._search(key, current=1, size=total).json()['records']
#     if not records:
#         return False
#
#     return self.download_all(records, total, path, key)
