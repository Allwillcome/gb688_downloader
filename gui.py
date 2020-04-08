from gooey import Gooey, GooeyParser
from standard.gb_downloader import download


# TODO:
#  默认下载文件夹设置（全局配置）
#  批量下载功能
#  版权及版本信息
#  错误处理
#  用户使用提示
@Gooey(language='chinese',
       program_name="国标下载器",
       program_description="这是一个下载国家标准的软件，请根据提示完成相应操作，如果发生什么奇怪的bug，请联系作者进行修复")
def main():
    parser = GooeyParser(description="请输入")
    parser.add_argument('url', widget="TextField", help="请在http://openstd.samr.gov.cn/查询国标并输入相应国标url")
    args = parser.parse_args()  # 接收界面传递的参数

    url = args.url
    path = download(url)

    return path


if __name__ == '__main__':
    main()
