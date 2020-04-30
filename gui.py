# TODO:
#  默认下载文件夹设置（全局配置）
#  批量下载功能
#  版权及版本信息
#  错误处理
#  用户使用提示
import tkinter as tk
from tkinter import messagebox
from standard import HDB, GB
from standard.utils import filter_file
from queue import Queue
import threading


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.gb = GB()
        self.hb = HDB('hbba')
        self.db = HDB('dbba')

        self.master = master
        self.std_widget(master)

        self._job = None

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
        # 再开一个进程用来获取数据，另一个用来定时渲染
        q = Queue()
        p = threading.Thread(target=self.download, args=(t, key, data, q))
        p.start()

        top_level = tk.Toplevel(master)
        top_level.title("标准下载")
        self.center_window(top_level, 1200, 800)
        t = tk.Text(top_level, height=30)
        t.grid(row=0, column=0)
        self.render_text(top_level, t, q)

    def render_text(self, master, text, q: Queue, empty_time=0):
        self._job = master.after(4000, lambda: self.render_text(master, text, q, empty_time))
        if q.empty():
            print('空')
            empty_time += 4
            if empty_time > 14:
                pass

        # print(last_index, total)
        empty_time = 0
        index, size, name, status = q.get()
        if index < size:
            text.insert('end', f"{name}    {status}\n")
        elif index == size:
            text.insert('end', f"{name}    {status}\n")
            self.cancel()
            messagebox.showinfo(message="全部下载完毕")
        else:
            print("最后啥都没了")

    def cancel(self):
        if self._job is not None:
            root.after_cancel(self._job)
            self._job = None

    def download(self, t, key, data, q: Queue):
        msg = ""
        date_length = len(data['records'])
        for index, record in enumerate(data["records"], 1):
            # print(record)
            name = f'{record["code"]}({record["chName"]})'
            try:
                if t == '行标':
                    path = f"{filter_file(key)}_hb"
                    self.hb.download(pk=record['pk'], name=name, path=path)
                    msg = "下载成功"

                elif t == "地标":
                    path = f"{filter_file(key)}_db"
                    self.db.download(pk=record['pk'], name=name, path=path)
                    msg = "下载成功"

                elif t == "国标":
                    path = f"{filter_file(key)}_gb"
                    self.gb.download(f'http://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno={record["ccno"]}', path)
                    msg = "下载成功"

            except Exception as e:
                msg = "下载失败"

            finally:
                # print('download',[index, date_length, record["chName"], msg])
                q.put([index, date_length, record["chName"], msg])

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


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
