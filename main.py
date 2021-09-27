from standard import HDB, NatureStd


if __name__ == "__main__":
    hb = HDB('hbba')
    db = HDB('dbba')
    data = db.search('政务云工程评价指标体系及方法')
    print(data)
    # first_record = data["records"][0]
    # name = f'{first_record["code"]}({first_record["chName"]}'
    # db.download(pk=first_record['pk'], name=name)

    # std = NatureStd()
    # std.search("")
    # std.download("http://www.nrsis.org.cn/portal/stdDetail/211166", "乡（镇）土地利用总体规划制图规范.pdf")  # 行标

