from pathlib import Path
from .config import BAN_LIST

import requests
from typing import Union


# TODO: 参考，不提供参考的文献：http://hbba.sacinfo.org.cn/stdDetail/068de47502bf8ba5e0bc3e3d27c75eef
def download(pk: str, t: str, name: str, path: Union[str, Path] = '.') -> Path:
    if t not in {'hbba', 'dbba'}:
        input("参数错误，请查询文档")
        raise Exception("t参数错误，请查询文档")
    for b in BAN_LIST:
        name = name.replace(b, " ")
    print("下载中...")
    url = f'http://{t}.sacinfo.org.cn/attachment/downloadStdFile?pk={pk}'
    r = requests.get(url)
    if len(r.content) == 0:
        raise Exception("该文件无法下载")
    with open(Path(path) / f'{name}.pdf', 'wb') as f:
        f.write(r.content)
    return Path(path) / f'{name}.pdf'


def search(key, t: str, status: str = '', pubdate: str = '', ministry: str = '', industry: str = '', current: int = 1,
           size: int = 15) -> dict:
    """这个函数用来对地方标准进行搜索，当值为空时，则默认为全部

    :param key: 搜索关键词
    :param t: 区分行业或地区标准，参数，行业标准：hbba、地方标准：dbba
    :param status: 标准的状态，有以下几个状态：''、'现行'、'有更新版'、'废止'
    :param pubdate: 备案日期，''、'-1'、'-3'、'-6'、'-12'、'-24'。这里的数字是代表一个月，即一个月内备案的标准
    :param ministry: 地区代号请参考文档
    :param industry: 行业代号请参考文档
    :param current:
    :param size:
    :return:
    """
    if t not in {'hbba', 'dbba'}:
        raise Exception("t参数错误，请查询文档")
    url = f"http://{t}.sacinfo.org.cn/stdQueryList"
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
    return r.json()
