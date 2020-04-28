# TODO:
#  默认下载文件夹设置（全局配置）
#  批量下载功能
#  版权及版本信息
#  错误处理
#  用户使用提示
import tkinter as tk
from tkinter import messagebox
from standard import HDB, GB
from prettytable import PrettyTable
from standard.utils import filter_file


#
# def download_hdb(t: str, text: str, page: int = 1, size: int = 15):
#     data = search(text, t=t, current=page, size=size)
#     pages = data['pages']
#     total = data['total']
#
#     print(f"\n本次搜索共有{pages}页，目前是第{page}页，共{total}项")
#     table = PrettyTable(['编号', '标准号', '名称'])
#     for index, d in enumerate(data['records'], start=1):
#         table.add_row([index, d['code'], d['chName']])
#
#     if len(data['records']) == 0:
#         print(f"没有找到匹配的记录")
#     else:
#         print(table)
#
#     num = int(input("请输入标准的编号来进行下载(向下翻页请输入-1，向上请输入0)："))  # 这里需要对其进行检测，以防不是int
#     if len(data['records']) < num < -1:
#         input("输入错误，退出")
#         exit()
#     elif num == -1:
#         if page * size > total:
#             print(f"已经是最后一页了")
#         else:
#             page += 1
#         download_hdb(t, text, page, size)
#     elif num == 0:
#         if page == 1:
#             print(f"已经是第一页了")
#         else:
#             page -= 1
#         download_hdb(t, text, page, size)
#     else:
#         try:
#             path = download(pk=data['records'][num - 1]['pk'],
#                             name=f'{data["records"][num - 1]["code"]}（{data["records"][num - 1]["chName"]}）', t=t)
#             print("下载成功")
#             download_hdb(t, text, page, size)
#         except Exception:
#             print(f"该文件源网页不支持下载")
#             input("按任意键继续下载...")
#             download_hdb(t, text, page, size)
#         return path


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.gb = GB()
        self.hb = HDB('hbba')
        self.db = HDB('dbba')

        self.master = master
        self.std_widget(master)

    def std_widget(self, master):
        """标准的搜索与下载

        :return:
        """
        hdb_frame = master
        hdb_frame.title("标准下载")
        self.center_window(hdb_frame, 600, 800)

        d_help = tk.Label(hdb_frame, text='请输入标准关键字来进行搜索，比如说标准名或标准号', bg='yellow')
        d_help.pack()

        tk.Label(hdb_frame, text="请选择标准").pack()

        var1 = tk.StringVar()
        hdb_set = ("国标", "行标", "地标")
        var1.set(hdb_set)
        lb = tk.Listbox(hdb_frame, listvariable=var1, height=3)
        lb.pack(pady=10)
        lb.select_set(0)

        # 插入文本框输入框
        t = tk.Entry(hdb_frame)
        t.pack(side="top")
        tk.Button(hdb_frame, text="搜索",
                  command=lambda: self.hdb_search_create(t.get(), lb.get(lb.curselection()[0]), hdb_frame)).pack(
            side="top")

    def hdb_search_create(self, text, t, master, page=1, size=25):
        hdb_search_frame = tk.Toplevel(master)
        hdb_search_frame.title("标准搜索")
        self.center_window(hdb_search_frame, 1200, 800)

        frame = tk.Frame(hdb_search_frame)
        frame.pack()

        self.hdb_search(text, t, frame, page=page, size=size)

    def hdb_search(self, text, t, master, page=1, size=25):
        """插入搜索内容

        :param master:
        :param text:
        :param t:
        :param page:
        :param size:
        :return:
        """
        # 清除Frame
        self.clear_frame(master)
        if t == "行标" or t == "地标":
            # 插入通用表头
            tk.Label(master, text="标准名称").grid(row=0, column=0)
            tk.Label(master, text="标准编号").grid(row=0, column=1)
            tk.Label(master, text="状态").grid(row=0, column=3)

            # 行标
            if t == "行标":
                data = self.hb.search(text, current=page, size=size)
                tk.Label(master, text="行业领域").grid(row=0, column=2)

            elif t == "地标":
                data = self.db.search(text, current=page, size=size)
                tk.Label(master, text="省市区").grid(row=0, column=2)
            else:
                raise Exception("奇怪的报错")

            last_row = 0
            for index, record in enumerate(data['records'], 1):
                tk.Label(master, text=record['chName'].replace('\n', ' ')).grid(row=index, column=0)
                tk.Label(master, text=record['code'].replace(' ', '')).grid(row=index, column=1)
                tk.Label(master, text=record['industry']).grid(row=index, column=2)
                tk.Label(master, text=record['status']).grid(row=index, column=3)

                last_row = index + 1
        elif t == "国标":
            data = self.gb.search(text, page=page, size=25)
            # 插入通用表头
            tk.Label(master, text="标准名称").grid(row=0, column=0)
            tk.Label(master, text="标准编号").grid(row=0, column=1)
            tk.Label(master, text="状态").grid(row=0, column=2)

            last_row = 0
            for index, record in enumerate(data['records'], 1):
                tk.Label(master, text=record['cn_name'].replace('\n', ' ')).grid(row=index, column=0)
                tk.Label(master, text=record['standard_no'].replace(' ', '')).grid(row=index, column=1)
                tk.Label(master, text=record['status']).grid(row=index, column=2)

                last_row = index + 1

        else:
            raise Exception("奇怪的错误")
        tk.Button(master, text="下载本页", background="yellow",
                  command=lambda: self.std_download(data, t, text, master)).grid(row=0, column=4)
        # print(data)

        if page >= 2:
            tk.Button(master, text="上一页", command=lambda: self.hdb_search(text, t, master, page=page - 1),
                      background="yellow").grid(row=last_row, column=0)
        if data['pages'] >= 2 and page < data['pages']:
            tk.Button(master, text="下一页",
                      command=lambda: self.hdb_search(text, t, master, page=page + 1), background="yellow").grid(
                row=last_row, column=1, )

    def std_download(self, data, t, key, master):
        top_level = tk.Toplevel(master)
        top_level.title("标准下载")
        self.center_window(top_level, 1200, 800)

        if t == '行标':
            path = f"{filter_file(key)}_hb"
            for index, record in enumerate(data["records"]):
                name = f'{record["code"]}({record["chName"]})'
                try:
                    self.hb.download(pk=record['pk'], name=name, path=path)
                    msg = "下载成功"
                except Exception:
                    msg = "下载失败"
                finally:
                    tk.Label(top_level, text=record["chName"]).grid(row=index, column=0)
                    tk.Label(top_level, text=msg).grid(row=index, column=1)

        elif t == "地标":
            path = f"{filter_file(key)}_db"
            self.db.download_all(data['records'], data['total'], None, f"{key}_db")
        elif t == "国标":
            path = f"{filter_file(key)}_gb"
            self.gb.download_all(data['records'], None, f"{key}_gb")

    @staticmethod
    def clear_frame(frame):
        """清除frame中的部件

        :param frame:
        :return:
        """
        for widget in frame.winfo_children():
            widget.destroy()

    def center_window(self, master, width, height):
        """使窗口居中

        :param master:
        :param width:
        :param height:
        :return:
        """
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        master.geometry(size)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
