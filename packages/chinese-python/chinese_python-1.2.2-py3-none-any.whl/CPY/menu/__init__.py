import tkinter,sys,os,re
from tkinter import ttk
from tkinter import messagebox
from tkinter import Menu


_path = os.path.realpath(__file__)
_file_path = sys.argv[-2]

import function
import model
import keywords

def windou_in_run():
        father_window=tk.Tk()
        father_window.title("新建文件")
        father_window.geometry("800x800")
        father_window.resizable(False, False)

        '''
        #创建菜单
        menu1 = Menu(father_window)
        menu2 = Menu(menu1,tearoff=False)
        menu3 = Menu(menu1,tearoff=False)
        menu4 = Menu(menu1,tearoff=False)
        menu5 = Menu(menu1,tearoff=False)
        menu1.add_cascade(label = '程序',menu = menu2)
        menu1.add_cascade(label = '运行',menu = menu3)
        menu1.add_cascade(label = '画面',menu = menu4)
        menu1.add_cascade(label = '帮助',menu = menu5)

        menu2.add_command(label = '新建',command = lambda:None)
        menu2.add_command(label = '打开',command = lambda:None)
        menu2.add_command(label = '保存',command = lambda:None)
        menu2.add_command(label = '另存为',command = lambda:None)
        menu2.add_command(label = '打开python',command = lambda:None)
        #menu1.add_command(label='程序')
        menu3.add_command(label = '直接运行',command = lambda:None)
        menu3.add_command(label = '保存并运行',command = lambda:None)
        menu3.add_command(label = '检查错误（不运行）',command = lambda:None)
        menu3.add_command(label = '使用IDLE运行',command = lambda:None)
        menu4.add_command(label = '修改界面长宽',command = lambda:None)
        menu4.add_command(label = '修改字体大小',command = lambda:None)
        menu5.add_command(label = '启动pip',command = lambda:None)
        menu5.add_command(label = '查看教程',command = lambda:None)
        menu5.add_command(label = '查看说明',command = lambda:None)
        menu5.add_command(label = '进入开发者模式',command = lambda:None)
        father_window.config(menu=menu1) #注意最好不要menu=menu
        '''

        word1=tk.Label(father_window,text="编译器输出窗口",font=("楷体",20),fg="black")
        word1.grid(pady=10)

        text=tk.Text(father_window, width=60, height=20)
        text.insert(tk.INSERT, "")
        text.configure(state='disabled')

        def change_text(new_row):
                
                text.configure(state='normal')
                text.delete('1.0',tk.END)
                # 现在可以写入文本
                text.insert('insert', new_row)
                # 重新设置为只读
                text.configure(state='disabled')

        def change_text_but_not_clear(new_text):
                text.configure(state='normal')
                text.insert('insert', new_row)
                # 重新设置为只读
                text.configure(state='disabled')
         
        text.grid(row = 1,column = 0,pady = 0,padx = 10)

        word2 = tk.Label(father_window,text="选择功能区",font=("楷体",20),fg="black")
        word2.grid(column=1, row=0)

        number = tk.StringVar()
        numberChosen = ttk.Combobox(father_window, width=12, textvariable=number)
        numberChosen['values'] = ("示例选项","函数","语句","模块","特殊")     # 设置下拉列表的值
        numberChosen.grid(column=1, row=1)      # 设置其在界面中出现的位置  column代表列   row 代表行
        numberChosen.current(0)

        lb_lang = tk.Listbox(father_window, listvariable=[])
        lb_lang.grid(column=2, row=1)

        def show_Listbox(event):
                b = numberChosen.get()
                a = number.get()
                del b

                lb_lang.delete(0,tk.END)

                if a == "示例选项":
                        show_list = ['示例1','示例2','示例3']
                        sv_list = tk.StringVar()
                        sv_list.set(tuple(show_list))
                        for item in show_list:
                                lb_lang.insert(tk.END, item)
                        #item = lb_lang.curselection()
                        del show_list,item
                        
                elif a == "函数":
                        sv_list = tk.StringVar()
                        sv_list.set(tuple(list(function.functions.keys())))
                        for item in list(function.functions.keys()):
                                lb_lang.insert(tk.END, item)
                        #item = lb_lang.curselection()
                        del item
                        
                elif a == "语句":
                        sv_list = tk.StringVar()
                        sv_list.set(tuple(list(keywords.key_words.keys())))
                        for item in list(keywords.key_words.keys()):
                                lb_lang.insert(tk.END, item)
                        #item = lb_lang.curselection()
                        del item
                        
                elif a == "模块":
                        sv_list = tk.StringVar()
                        sv_list.set(tuple(list(model.model.keys())))
                        for item in list(model.model.keys()):
                                lb_lang.insert(tk.END, item)
                        #item = lb_lang.curselection()
                        del item

                elif a == "特殊":
                        show_list = ['赋值','自定义函数','使用类','创建列表','创建元组','创建字典']
                        sv_list = tk.StringVar()
                        sv_list.set(tuple(show_list))
                        for item in show_list:
                                lb_lang.insert(tk.END, item)
                        #item = lb_lang.curselection()
                        del show_list,item

        numberChosen.bind("<<ComboboxSelected>>", show_Listbox)

        def _clear():
                result = messagebox.askyesno("确认清屏", "确认文件是否保存")
                if result:
                        # 执行保存操作
                        change_text(' ')
                        messagebox.showinfo("完成", "成功清屏")
                else:
                        messagebox.showwarning("取消", "用户取消了清屏")

        def _get():
                b = numberChosen.get()
                a = number.get()
                del b
                
                if a == "示例选项":
                        item = lb_lang.get(lb_lang.curselection())
                        print(item)
                        if item == '示例1':
                                open_mode = 'eg1.py'
                        elif item == '示例2':
                                open_model = 'eg2.py'
                        else:
                                open_model = 'eg3.py'
                        
                elif a == "函数":
                        item = lb_lang.get(lb_lang.curselection())
                        print(item)
                        return function.functions.get(item)
                        
                elif a == "语句":
                        item = lb_lang.get(lb_lang.curselection())
                        print(item)
                        return keywords.key_words.get(item)
                        
                elif a == "模块":
                        item = lb_lang.get(lb_lang.curselection())
                        print(item)
                        return model.model.get(item)

                elif a == "特殊":
                        pass
                
                

        button1=tk.Button(father_window,text="清屏",command=_clear)
        button1.grid(row=2,column=0)

        button2=tk.Button(father_window,text="添加",command=_get)
        button2.grid(row=2,column=1)

        father_window.mainloop()
