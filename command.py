from standard.gb_downloader import *


def main():
    print("这是一个下载国家标准的软件，请根据提示完成相应操作，如果发生什么奇怪的bug，请联系作者进行修复\n")
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
    print("下载成功")
    input("按任意键退出...")
