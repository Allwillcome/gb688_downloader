from standard.gb_download import is_download, get_hcno, get_pdf_name, BAN_LIST, get_bytes
from standard.db_download import search, download
from prettytable import PrettyTable


def download_hgb(t, text):
    data = search(text, t=t)
    # TODO: 需要对翻页进行处理
    pages = data['pages']
    size = data['total']

    table = PrettyTable(['编号', '标准号', '名称'])
    for index, d in enumerate(data['records']):
        table.add_row([index, d['code'], d['chName']])
    print(table)

    num = int(input("请输入标准的编号来进行下载："))  # 这里需要对其进行检测，以防不是int
    if num > len(data['records']):
        input("输入错误，退出")
        exit()
    path = download(pk=data['records'][num]['pk'],
                    name=f'{data["records"][num]["code"]}({data["records"][num]["chName"]}', t=t)
    return path


def main():
    print("这是一个下载国家标准的软件，请根据提示完成相应操作，如果发生什么奇怪的bug，请联系作者进行修复\n")
    standard_type = input("下载国家请输入gb，行业标准请输入hb，地方标准请输入db：")
    if standard_type == "gb":
        print("请注意，您现在正准备下载国家标准")
        url = input("请输入需要下载的url：").replace(" ", "")
        if not is_download(url):
            input("这个文件展示不支持下载，原页面没有在线预览，请自行打开网页进行查询")
            raise Exception("这个文件展示不支持下载，原页面没有在线预览，请自行打开网页进行查询")

        hcno = get_hcno(url)
        g_name, c_name = get_pdf_name(url)
        pdf_name = f"{g_name}({c_name})"

        for b in BAN_LIST:
            pdf_name = pdf_name.replace(b, " ")

        pdf_bytes = get_bytes(hcno)

        with open(f"{pdf_name}.pdf", "wb") as f:
            f.write(pdf_bytes)

    elif standard_type == "hb":
        print("请注意，您现在正准备下载行业标准")
        text = input("请输入标准关键字来进行搜索，比如说标准名或标准号：")
        path = download_hgb('hbba', text)
    elif standard_type == "db":
        print("请注意，您现在正准备下载地方标准")
        text = input("请输入标准关键字来进行搜索，比如说标准名或标准号：")
        path = download_hgb('dbba', text)
    elif standard_type != "gb" or standard_type != "hy" or standard_type != "df":
        print("输入的代号错误")

    print("下载成功")
    input("按任意键退出...")


if __name__ == '__main__':
    main()
