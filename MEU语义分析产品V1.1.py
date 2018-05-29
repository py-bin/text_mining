# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 10:52:14 2018

@author: bin
"""
##############模块引入#############
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import tkinter.filedialog
from PIL import Image,ImageTk
import pandas as pd
import os
#自定义模块text_process，是文本处理的核心
from text_process import address_extract,structured_info_extract,products_extract
#数据源
global data
global file_path,rst1,rst2,rst3
rst1 = rst2 = rst3 = ''
imgDict = {}
#############用户界面基本属性########
top = tk.Tk()
top.title("Meu语义分析工具")
top.geometry('800x600')
top.resizable(False, False)

#############事件函数###############
#打开选择文件窗口
def choose_file():
    
    global file_path
    
    filename = tkinter.filedialog.askopenfilename()
    file_path = os.path.dirname(filename)
    
    if filename != '':
        lb_btm.config(text = "您选择的文件是："+filename)
        data_read(filename)
    else:
        lb_btm.config(text = "您没有选择任何文件")

#导出数据
def save_data():
    global file_path,rst1,rst2,rst3
    with pd.ExcelWriter(os.path.join(file_path,'文本处理结果.xlsx')) as writer:
        if isinstance(rst1,pd.core.frame.DataFrame):
            rst1.to_excel(writer, sheet_name='结构化信息提取',index=False)
        if isinstance(rst2,pd.core.frame.DataFrame):
            rst2.to_excel(writer, sheet_name='产品信息提取',index=False)
        if isinstance(rst3,pd.core.frame.DataFrame):
            rst3.to_excel(writer, sheet_name='地址信息提取',index=False)


#未完成功能
def edit_fun():
    
    lb_top.config(text = "敬请期待~")

#读入文件
def data_read(filename):
   
    global data,rst1,rst2,rst3
    data = pd.read_excel(filename)
    tree_display(data.head(),25,80)
    rst1 = rst2 = rst3 = ''
    
#数据预览
def tree_display(dataset,p_x,p_y):
    
    global top
    area = ttk.Treeview(top,columns=list(dataset.columns),show='headings',height = 6)
    cell_width = 750/len(dataset.columns)
    for col in dataset.columns:
        area.column(col,width = int(cell_width))
        area.heading(col, text=col)
        area.place(x=p_x,y=p_y)
    for i in range(len(dataset)):
        row = tuple(dataset.iloc[i,:])
        area.insert('','end',values=row)

#主功能1：结构化信息提取
def structed_process():
    
    result = structured_info_extract(data)
    tree_display(result.head(),25,280)
    global rst1
    rst1 = result

#主功能2：产品信息提取
def product_process():
    
    pdt_sheet = pd.read_excel('产品列表.xlsx')
    product_lst = pdt_sheet['产品名称']
    result = products_extract(data,product_lst)
    tree_display(result.head(),25,280)
    global rst2
    rst2 = result

#主功能3：地址信息提取
def address_process():
    
    result = address_extract(data)
    tree_display(result.head(),25,280)
    global rst3
    rst3 = result

#开发人员信息
def click():
    
    dvlp_info = '领衔主演： 吴梓栩、梁少红\n\n \
    主演：彭胜利、王焕荣、庞思亮\n黄诗雅、张月泉、卢晓玲、陈立文\n\n \
    导演：郑伟彬'
    tkinter.messagebox.showinfo('产品信息',dvlp_info)

###########窗体部件############

def lb_bt(top):
    
#label标签区
    global lb_btm,lb_top
    lb_btm = tk.Label(top)
    lb_btm.pack(side='bottom')
    lb_top = tk.Label(top)
    lb_top.pack(side='top')
    lb_scan1 = tk.Label(top,text='数据源预览区域')
    lb_scan1.place(x=60, y=40)
    lb_scan2 = tk.Label(top,text='处理后数据预览区域')
    lb_scan2.place(x=60, y=240)
    
#Button按钮区
    bt_export = tk.Button(top,text='导出结果数据',width=10,height=2,command=save_data)
    bt_export.place(x=650, y=450)

#目录
def my_menu(top):
    
    menubar = tk.Menu(top)
    filemenu = tk.Menu(menubar, tearoff=0)
    
    #文件目录
    menubar.add_cascade(label='  文件  ', menu=filemenu)
    filemenu.add_command(label='打开... ', command=choose_file)
    filemenu.add_command(label='导出结果', command=choose_file)
    filemenu.add_separator()
    filemenu.add_command(label='退出', command=top.quit)
    
    #编辑目录
    editmenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=' 文本处理 ', menu=editmenu)
    editmenu.add_command(label='结构化信息处理', command=structed_process)
    editmenu.add_command(label='匹配产品信息', command=product_process)
    editmenu.add_command(label='地址信息提取', command=address_process)
    
    #编辑目录
    funmenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=' 功能区 ', menu=funmenu)
    funmenu.add_command(label='TXT转CSV', command=edit_fun)
    funmenu.add_command(label='合并文件夹中数据', command=edit_fun)
    funmenu.add_command(label='批量修改文件名', command=edit_fun)
    
    #帮助目录
    infomenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=' 使用帮助 ', menu=infomenu)
    infomenu.add_command(label='说明文档', command=edit_fun)
    infomenu.add_command(label='关于...', command=click)
    top.config(menu=menubar)

#LOGO和copyright
def other_item(top):
    #LOGO
    img_open = Image.open('logo.png')
    img_png = ImageTk.PhotoImage(img_open)
    imgDict['LOGO'] = img_png#PYTHON会自动回收内存，如果不保存下来，图像会显示为空白框
    label_img = tk.Label(top, image = img_png,width=80,height=80) 
    label_img.place(x=720, y=0)
    #copyright
    lb_cpr = tk.Label(top)
    lb_cpr.pack(side='bottom')
    lb_cpr.config(text = "© MeU 2018")


#原始空白数据预览区
def preview_area(top):

    #数据源预览区
    col_list = ['列名1','列名2','列名3','列名4','列名5']
    data_preview = pd.DataFrame(columns = col_list)
    tree_display(data_preview,25,80)
    tree_display(data_preview,25,280)

###############程序主体#############
if __name__ =='__main__':
    my_menu(top)#目录
    lb_bt(top)#各种标签
    preview_area(top)#数据预览区域
    other_item(top)#LOGO和copyright
    top.mainloop()#窗体循环