from standard.db_download import search, download

if __name__ == '__main__':
    t = 'dbba'
    data = search('政务云工程评价指标体系及方法', t=t)
    name = f'{data["records"][0]["code"]}({data["records"][0]["chName"]}'
    download(pk=data['records'][0]['pk'], name=name, t=t)
