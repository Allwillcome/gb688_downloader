from standard.db_download import search, download
from standard.gb_download import search as gb_search, download as gb_download
from pathlib import Path


def download_all_hdb(text, t, path='file'):
    all_size = search(text, t=t, current=1, size=100)['total']
    records = search(text, t=t, current=1, size=all_size)['records']
    if not records:
        return

    failed_num = 0
    for record in records:
        name = f'{record["code"]}({record["chName"]})'
        try:
            print(f"正在下载  {name}")
            download(pk=record['pk'], name=name, t=t, dir=path)
        except Exception:
            print(f"{name}下载失败")
            failed_num += 1

    print(f"共{len(records)}条记录，成功{len(records) - failed_num}条，失败{failed_num}条")


def download_all_gb(text, path):
    records = gb_search(text)
    if records['total_size'] == 0:
        print("未找到相关标准")
    for record in records['records']:
        print(record)
        gb_download(f"http://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno={record['hcno']}", path)


if __name__ == '__main__':
    download_all_hdb('政务', 'dbba', Path('aa'))
    download_all_gb('养老', Path('aa'))
    # t = 'dbba'
    # data = search('政务云工程评价指标体系及方法', t=t)
    # name = f'{data["records"][0]["code"]}({data["records"][0]["chName"]}'
    # download(pk=data['records'][0]['pk'], name=name, t=t)
