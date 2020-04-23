from standard import GB, HDB

if __name__ == '__main__':
    gb = GB()
    gb.download('http://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=D8AB02F0141FE11A4976E0E94FCF58B4')
    gb.search_and_download('养老')

    hb = HDB('hbba')
    db = HDB('dbba')
    data = db.search('政务云工程评价指标体系及方法')
    first_record = data["records"][0]
    name = f'{first_record["code"]}({first_record["chName"]}'
    db.download(pk=first_record['pk'], name=name)

    db.search_and_download("电子政务")
