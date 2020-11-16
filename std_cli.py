from pathlib import Path

from cleo import Application, Command
from colorama import Fore, init
from prettytable import PrettyTable

from standard import GB, HDB, NatureStd
from standard.errors import DownloadError

init(autoreset=True)


# TODO: 文件命名，要对 detail_url 进行解析
class DownloadCommand(Command):
    """
    下载某个标准

    download
        {url : 需要下载标准的网址}
        {path : 保存的路径}
        {--o|over : 如果路径已存在，是否覆盖？}
    """

    def handle(self):
        url = self.argument("url")
        path = Path(self.argument("path"))
        over = self.option("over")
        if path.is_file() and over is False:
            if not self.confirm("该文件已存在，是否继续？", False):
                return 0

        if "hbba" in url:  # 行标
            std = HDB("hbba")
        elif "dbba" in url:  # 地标
            std = HDB("dbba")
        elif "openstd.samr" in url:  # 国标
            std = GB()
        elif "nrsis.org.cn" in url:  # 自然标准
            std = NatureStd()
        else:
            self.info("目前暂不支持此标准")
            return 1

        self.line("开始下载，请稍等")
        std.download(url, path)
        self.line("下载完成了")
        return 0

    def error(self, text):
        self.line(Fore.RED + text)

    def info(self, text):
        self.line(Fore.YELLOW + text)


class SearchCommand(Command):
    """
    search

    search
        {query : 查询关键字}
        {--p|platform= : 查询的平台}
        {--f|folder= : 保存的文件夹}
        {--m|mkdir : 则找不到的父级目录会导致 FileNotFoundError 被抛出。}
        {--e|exist : 则在目标已存在的情况下抛出 FileExistsError。详情参照：https://docs.python.org/zh-cn/3/library/pathlib.html#pathlib.Path.mkdir} # noqa
    """

    def handle(self):
        page = 1
        size = {"gb": 10, "hb": 15, "db": 15, "natureStd": 20}
        q = self.argument("query")
        platform = self.option("platform")
        mkdir = self.option("mkdir")

        if folder := self.option("folder"):
            folder = Path(folder)

            if mkdir is False:
                if not folder.exists():
                    self.error("folder 文件夹不存在")
                    return 0
                if folder.is_file():
                    self.error("folder 不是文件夹")
                    return 0
            else:
                folder.mkdir(parents=mkdir, exist_ok=self.option("exist"))
        else:
            folder = Path(".")

        if not platform:
            platform = self.choice("选择你要搜索的平台", ["gb", "hb", "db", "natureStd"])

        if platform not in {"hb", "db", "gb", "natureStd"}:
            self.error('请输入正确的platform参数，支持 "hb", "db", "gb", "natureStd" 这四种参数')
            platform = self.choice("选择你要搜索的平台", ["gb", "hb", "db", "natureStd"])

        if platform == "hb":
            std = HDB("hbba")
        elif platform == "db":
            std = HDB("dbba")
        elif platform == "gb":
            std = GB()
        elif platform == "natureStd":
            std = NatureStd()
        else:
            return 0

        data = self._search(std, platform, q, page, size)
        self._handle(std, platform, q, folder, page, size, data)

    def _search(self, std, platform, q, page, size):  # noqa
        if platform == "hb":
            data = std.search(q, page=page, size=size["hb"])
        elif platform == "db":
            data = std.search(q, page=page, size=size["db"])
        elif platform == "gb":
            data = std.search(q, page=page, size=size["gb"])
        elif platform == "natureStd":
            data = std.search(q, page=page, size=size["natureStd"])
        else:
            return 0
        return data

    def _handle(
        self, std, platform, q: str, folder: Path, page: int, size: dict, data
    ) -> int:
        self.line(f"共找到{data.total_size}条数据")
        if data.total_size == 0:
            self.error("啥都没找到，那就退出了")
            return 1

        tb = PrettyTable()
        tb.field_names = ["序号", "标准名", "标准号"]
        for index, stdItem in enumerate(data.data, 1):
            tb.add_row([index, stdItem.name, stdItem.code])
        self.line(tb.get_string())
        value = self.ask("请选择要下载的标准序号，比如1，也可以是1-4，也可以输入0向下翻页，-1向上翻页 >: ")

        try:
            start = int(value)
            end = start
        except ValueError:
            if len(value.split("-")) == 2:
                try:
                    start, end = int(value.split("-")[0]), int(value.split("-")[1])
                except ValueError:
                    raise ValueError("参数错误")
            else:
                raise ValueError("参数错误")
        if start == 0:
            if page * size[platform] <= data.total_size:
                page += 1
                self.line(f"向下翻页, 现在是第{page}页")
                data = self._search(std, platform, q, page, size)
            else:
                page = page
                self.info(f"现在已经是最大页数，不能再翻页了")
                data = data

            self._handle(std, platform, q, folder, page, size, data)
            return 1
        if start == -1:
            if page == 1:
                page = page
                self.info(f"现在已经是最小页数了，不能再翻页了")
                data = data
            else:
                page -= 1
                self.line(f"向上翻页, 现在是第{page}页")
                data = self._search(std, platform, q, page, size)

            self._handle(std, platform, q, folder, page, size, data)
            return 1

        self.line(f"共有{end - start + 1}个标准需要下载\n")
        for index, stdItem in enumerate(data.data[start - 1 : end], 1):
            self.line(f"正在下载第{index}个标准")
            try:
                std.download(stdItem.url, path=folder / f"{stdItem.name}.pdf")
            except DownloadError:
                self.line(f"第{index}个文件下载失败，大概率是源文件不支持下载")

        self.line(f"标准都下载完成了，保存在 {folder.absolute()} 文件下")

    def error(self, text):
        self.line(Fore.RED + text)

    def info(self, text):
        self.line(Fore.YELLOW + text)


application = Application("std_cli", "2.1")
application.add(DownloadCommand())
application.add(SearchCommand())

if __name__ == "__main__":
    application.run()
