from standard.gb_download import is_download, get_hcno, get_pdf_name, BAN_LIST, get_bytes
from standard.db_download import search, download
from prettytable import PrettyTable
from colorama import Fore, init

init(autoreset=True)


def download_hdb(t: str, text: str, page: int = 1, size: int = 15):
    data = search(text, t=t, current=page, size=size)
    pages = data['pages']
    total = data['total']

    print(f"\n本次搜索共有{pages}页，目前是第{page}页，共{total}项")
    table = PrettyTable(['编号', '标准号', '名称'])
    for index, d in enumerate(data['records'], start=1):
        table.add_row([index, d['code'], d['chName']])

    if len(data['records']) == 0:
        print(f"{Fore.YELLOW}没有找到匹配的记录")
    else:
        print(table)

    num = int(input("请输入标准的编号来进行下载(向下翻页请输入-1，向上请输入0)："))  # 这里需要对其进行检测，以防不是int
    if len(data['records']) < num < -1:
        input("输入错误，退出")
        exit()
    elif num == -1:
        if page * size > total:
            print(f"{Fore.YELLOW}已经是最后一页了")
        else:
            page += 1
        download_hdb(t, text, page, size)
    elif num == 0:
        if page == 1:
            print(f"{Fore.YELLOW}已经是第一页了")
        else:
            page -= 1
        download_hdb(t, text, page, size)
    else:
        try:
            path = download(pk=data['records'][num - 1]['pk'],
                            name=f'{data["records"][num - 1]["code"]}（{data["records"][num - 1]["chName"]}）', t=t)
            print("下载成功")
            download_hdb(t, text, page, size)
        except Exception:
            print(f"{Fore.YELLOW}该文件源网页不支持下载")
            input("按任意键继续下载...")
            download_hdb(t, text, page, size)
        return path


def download_gb(url: str):
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


def main():
    print("这是一个下载国家标准的软件，请根据提示完成相应操作，如果发生什么奇怪的bug，请联系作者进行修复\n")
    standard_type = input("下载国家请输入gb，行业标准请输入hb，地方标准请输入db：")
    if standard_type == "gb":
        print(f"{Fore.YELLOW}请注意，您现在正准备下载国家标准，相应的url请在www.gb688.cn/bzgk/gb/index中寻找")
        url = input("请输入需要下载的url：").replace(" ", "")
        download_gb(url)

    elif standard_type == "hb":
        print(f"{Fore.YELLOW}请注意，您现在正准备下载行业标准")
        text = input("请输入标准关键字来进行搜索，比如说标准名或标准号：")
        path = download_hdb('hbba', text)
    elif standard_type == "db":
        print(f"{Fore.YELLOW}请注意，您现在正准备下载地方标准")
        text = input("请输入标准关键字来进行搜索，比如说标准名或标准号：")
        path = download_hdb('dbba', text)
    elif standard_type != "gb" or standard_type != "hy" or standard_type != "df":
        print(f"{Fore.RED}输入的代号错误")

    input("按任意键退出...")


if __name__ == '__main__':
    main()
