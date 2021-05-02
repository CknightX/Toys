'''
图片归类（手动版）
by: ck

使用说明：
将该脚本置于待归类图片目录下，并设置好图片库目录，运行脚本后将根据图片库目录下的文件夹生成相应按钮，
并依次展示待归类图片。点击按钮即可将当前预览的图片移动至对应的文件夹。
'''

import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import os
import shutil


def is_imgfile(filename):
    img_hz = ('png', 'jpg','gif','JPG','jpeg','JPEG')
    for hz in img_hz:
        if filename.find(hz) != -1:
            return True
    return False


class App(tk.Tk):
    buttons = []
    class_path = r''   # 图片库目录
    img_files = list(filter(lambda file: os.path.isfile(file) and is_imgfile(file), os.listdir('./')))
    curr_filepath = '?'
    index = -1

    def __init__(self):
        super().__init__()
        self.set_window()
        self.create_imglabel()
        self.create_button_list(self.class_path)
        self.next_img()

    def set_window(self):
        self.title("图片归类")

    def create_imglabel(self):
        frame = ttk.Frame(self)
        self.info_var = tk.StringVar()
        info=ttk.Label(frame, textvariable=self.info_var)
        info.pack()
        self.label_img = tk.Label(frame, bitmap="info", height=500, width=500)
        self.label_img.pack()
        frame.pack(side=tk.LEFT)

    def create_button_list(self, path):
        frame = ttk.Frame(self)
        files_list = os.listdir(path)
        fold_list = filter(lambda file: os.path.isdir(path + '/' + file), files_list)
        ttk.Button(frame, text="跳过", command=self.next_img).pack()
        ttk.Button(frame, text="删除", command=self.del_img).pack()
        for fold in fold_list:
            button = ttk.Button(frame, text=fold, command=lambda fold=fold: self.move_img(
                '%s/%s/%s' % (self.class_path, fold, self.curr_filepath)))
            button.pack()
        frame.pack(side=tk.LEFT)

    def del_img(self):
        try:
            os.remove(self.curr_filepath)
        except Exception as e:
            print(e)
        self.next_img()

    def move_img(self, des_path):
        if self.curr_filepath == '?':
            return
        try:
            shutil.move(self.curr_filepath, des_path)
        except Exception as e:
            print(e)
        self.next_img()

    def next_img(self):
        if self.img_files is None or self.index>=len(self.img_files)-1:
            self.show_curr_img(not_show=True)
            self.info_var.set('归类完成')
            self.curr_filepath = '?'
            return
        self.index+=1

        self.curr_filepath = './%s' % self.img_files[self.index]
        self.info_var.set('已归类:%d张，还剩:%d张'%(self.index,len(self.img_files)-self.index))
        self.show_curr_img()

    def show_curr_img(self, not_show=False):
        if not_show:
            self.label_img.image = None
            return
        try:
            img = Image.open(self.curr_filepath)
            img = img.resize((500, 500), Image.ANTIALIAS)
            curr_image = ImageTk.PhotoImage(img)
        except Exception as e:
            print(e)
        else:
            self.label_img.configure(image=curr_image)
            self.label_img.image = curr_image


if __name__ == '__main__':
    app = App()
    app.mainloop()
