from pathlib import Path

from cleo import Application, Command
from prettytable import PrettyTable

from standard import GB, HDB, NatureStd


class DownloadCommand(Command):
    """
    下载某个标准

    download
        {url : 需要下载的标准网址}
        {--p|path=? : 保存的路径}
    """

    def handle(self):
        url = self.argument("url")
        if path := self.option("path"):
            path = Path(path)
            if not path.parent.is_dir():
                raise FileNotFoundError("没有找到该文件夹")
        else:
            path = Path(".") / "aa.pdf"

        self.line("开始下载，请稍等")
        if "hbba" in url:  # 行标
            std = HDB("hbba")
        elif "dbba" in url:  # 地标
            std = HDB("dbba")
        elif "openstd.samr" in url:  # 国标
            std = GB()
        elif "nrsis.org.cn" in url:  # 自然标准
            std = NatureStd()
        else:
            self.line("<info>目前暂不支持此标准</info>")
            return 1

        std.download(url, path)
        self.line("下载完成了")
        return 0


# TODO: 翻页功能实现
# TODO: 几种标准的适配，现在只支持 natureStd
# TODO: 三个平台下文件创建问题
class SearchCommand(Command):
    """
    search

    search
        {query : 查询关键字}
        {--p|platform= : 查询的平台}
        {--f|folder= : 保存的文件夹}
        {--m|mkdir : 则找不到的父级目录会导致 FileNotFoundError 被抛出。}
        {--e|exist : 则在目标已存在的情况下抛出 FileExistsError。详情参照：https://docs.python.org/zh-cn/3/library/pathlib.html#pathlib.Path.mkdir}
    """

    def handle(self):
        page = 1
        size = {
            "gb": 10,
            "hdb": 15,
            "natureStd": 20
        }
        q = self.argument("query")
        platform = self.option("platform")
        if not platform:
            platform = self.choice("选择你要搜索的平台", ["hb", "db", "gb", "natureStd"])

        if platform not in {"hb", "db", "gb", "natureStd"}:
            self.line('请输入正确的platform参数，支持 "hb", "db", "gb", "natureStd" 这四种参数')
            platform = self.choice("选择你要搜索的平台", ["hb", "db", "gb", "natureStd"])

        if folder := self.option("folder"):
            folder = Path(folder)
            if not folder.is_dir():
                raise FileExistsError("folder不是一个文件夹")
            else:
                if mkdir := self.option("mkdir"):
                    folder.mkdir(parents=mkdir, exist_ok=self.option("exist"))
        else:
            folder = Path(".")

        if platform == "hb":
            std = HDB("hbba")
            data = std.search(q)
        elif platform == "db":
            std = HDB("dbba")
            data = std.search(q)
        elif platform == "gb":
            std = GB()
            data = std.search(q)
        elif platform == "natureStd":
            std = NatureStd()
            data = std.search(q)
        else:
            return 0

        self.line(f"共找到{data.total_size}条数据")

        tb = PrettyTable()
        tb.field_names = ['序号', '标准名', '标准号']
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
            self.line("向下翻页")
            return 1
        if start == -1:
            self.line("向上翻页")
            return 1

        self.line(f"共有{end - start + 1}个标准需要下载")
        for index, stdItem in enumerate(data.data[start - 1:end], 1):
            self.line(f"正在下载第{index}个标准")
            std.download(stdItem.url, path=folder / f"{stdItem.name}.pdf")
        self.line(f"{end - start + 1}10个标准都下载完成了，保存在{folder.absolute()}文件下")


application = Application()
application.add(DownloadCommand())
application.add(SearchCommand())

if __name__ == "__main__":
    application.run()
