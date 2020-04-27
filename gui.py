# TODO:
#  默认下载文件夹设置（全局配置）
#  批量下载功能
#  版权及版本信息
#  错误处理
#  用户使用提示
import tkinter as tk

from standard import HDB, GB
from prettytable import PrettyTable


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
        self.pack()
        self.center_window(self.master, 150, 180)
        self.create_main_widgets()

    def create_main_widgets(self):
        gb_button = tk.Button(self, text="国标下载", command=self.download_gb)
        gb_button.pack(side="top")

        hdb_button = tk.Button(self, text="行标、地标下载", command=lambda: self.hdb_widget(self.master))
        hdb_button.pack(side="bottom")

    def download_gb(self):
        pass

    def hdb_widget(self, master):
        """行标、地标的搜索与下载

        :return:
        """
        hdb_frame = tk.Toplevel(master)
        hdb_frame.title("行标、地标下载")
        self.center_window(hdb_frame, 600, 800)

        d_help = tk.Label(hdb_frame, text='请输入标准关键字来进行搜索，比如说标准名或标准号', bg='yellow')
        d_help.pack()

        tk.Label(hdb_frame, text="请选择行标还是地标").pack()
        var1 = tk.StringVar()
        var1.set(("行标", "地标"))
        tk.Listbox(hdb_frame, listvariable=var1, height=2).pack(pady=10)
        # tk.Checkbutton(hdb_frame, text='行标', variable=var2, onvalue=1, offvalue=0).pack()

        # 插入文本框输入框
        t = tk.Entry(hdb_frame)
        t.pack(side="top")

        tk.Button(hdb_frame, text="搜索", command=lambda: self.hdb_search(t.get(), 'hbba', hdb_frame)).pack(side="top")

    def hdb_search(self, text, t, master=None, page=1, size=50):
        """插入搜索内容

        :param master:
        :param text:
        :param t:
        :param page:
        :param size:
        :return:
        """
        if master is not None:
            hdb_search_frame = tk.Toplevel(master)
            hdb_search_frame.title("行标、地标下载")
        else:
            hdb_search_frame = master
        self.center_window(hdb_search_frame, 1200, 800)
        print(text, t)

        data = self.hb.search(text, current=page, size=size)
        print(data)
        # 插入表头
        tk.Label(hdb_search_frame, text="标准名称").grid(row=0, column=0)
        tk.Label(hdb_search_frame, text="标准编号").grid(row=0, column=1)
        tk.Label(hdb_search_frame, text="时间").grid(row=0, column=2)
        # tk.Label(hdb_search_frame, text=record['chName']).grid(row=0, column=3)

        last_row = 0
        # 插入内容
        scrollbar = tk.Scrollbar(master)
        scrollbar.pack(side='right', fill='Y')

        listbox_1 = tk.Listbox(hdb_search_frame, yscrollcommand=scrollbar.set)

        for index, record in enumerate(data['records'], 1):
            tk.Label(hdb_search_frame, text=record['chName']).grid(row=index, column=0)
            tk.Label(hdb_search_frame, text=record['code'].replace(' ', '')).grid(row=index, column=1)
            tk.Label(hdb_search_frame, text=record['actDate']).grid(row=index, column=2)

            last_row = index + 1

        if page >= 2:
            tk.Button(hdb_search_frame, text="上一页",
                      command=lambda: self.hdb_search(text, t, page=page - 1)).grid(row=last_row, column=0)
        tk.Button(hdb_search_frame, text="下一页",
                  command=lambda: self.hdb_search(text, t, page=page + 1)).grid(row=last_row, column=1)

    def center_window(self, frame, width, height):
        """使窗口居中

        :param frame:
        :param width:
        :param height:
        :return:
        """
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        frame.geometry(size)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
