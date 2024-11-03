import tkinter as tk
from tkinter import ttk

father_window=tk.Tk()
father_window.title("chyhon合成编译器")
father_window.geometry("800x800")
father_window.resizable(False, False)

word1=tk.Label(father_window,text="编译器输出窗口",font=("楷体",20),fg="black")
word1.grid(pady=10)

text1=tk.Text(father_window, width=60, height=20)
text1.insert(tk.INSERT, "")
text1.configure(state='disabled')

def change_text1(new_row):
        
        text1.configure(state='normal')
        text1.delete('1.0',tk.END)
        # 现在可以写入文本
        text1.insert('insert', new_row)
        # 重新设置为只读
        text1.configure(state='disabled')
 
text1.grid(row=1,column=0,pady=0,padx=10)

word2=tk.Label(father_window,text="选择功能区",font=("楷体",20),fg="black")
word2.grid(column=1, row=0)

number = tk.StringVar()
numberChosen = ttk.Combobox(father_window, width=12, textvariable=number)
numberChosen['values'] = ("函数","语句","模块","特殊")     # 设置下拉列表的值
numberChosen.grid(column=1, row=1)      # 设置其在界面中出现的位置  column代表列   row 代表行
numberChosen.current(0)

def started():
        pass

def del_button(m):
        '''
        try:
                button1.destroy()
                button2.destroy()
                button3.destroy()
                button4.destroy()
                button5.destroy()
                button6.destroy()
                button7.destroy()
                button8.destroy()
                button9.destroy()
                button0.destroy()
                button10.destroy()
                #button1.destroy()
        except:
                None
                print(1)
        '''
        if m==0:
                
                print(m)
                m+=1
        else:
                button1.destroy()
                button2.destroy()
                button3.destroy()
                button4.destroy()
                button5.destroy()
                button6.destroy()
                button7.destroy()
                button8.destroy()
                button9.destroy()
                button0.destroy()
                button10.destroy()
                print(m)
                m+=1
        '''
        button1.destroy()
        button2.destroy()
        button3.destroy()
        button4.destroy()
        button5.destroy()
        button6.destroy()
        button7.destroy()
        button8.destroy()
        button9.destroy()
        button0.destroy()
        button10.destroy()
'''
def show_button(event):
        m=0
        del_button(m)
        '''
        try:
                button1.destroy()
                button2.destroy()
                button3.destroy()
                button4.destroy()
                button5.destroy()
                button6.destroy()
                button7.destroy()
                button8.destroy()
                button9.destroy()
                button0.destroy()
                button10.destroy()
                #button1.destroy()
        except:
                None
        '''
        b=numberChosen.get()
        a=number.get()
        #return a,b
        if a=="函数":
                '''
                try:
                        button1.destroy()
                        button2.destroy()
                        button3.destroy()
                        button4.destroy()
                        button5.destroy()
                        button6.destroy()
                        button7.destroy()
                        button8.destroy()
                        button9.destroy()
                        button0.destroy()
                        button10.destroy()
                        #button1.destroy()
                except:
                        None
                '''
                b=1
                button1=tk.Button(father_window,text="输出",command=started)
                button1.grid(row=2,column=0)
                button2=tk.Button(father_window,text="输入",command=started)
                button2.grid(row=2,column=1)
                button3=tk.Button(father_window,text="字符串",command=started)
                button3.grid(row=2,column=2)
                button4=tk.Button(father_window,text="整数",command=started)
                button4.grid(row=3,column=0)
                button5=tk.Button(father_window,text="浮点数",command=started)
                button5.grid(row=3,column=1)
                button6=tk.Button(father_window,text="整数列表",command=started)
                button6.grid(row=3,column=2)
                button7=tk.Button(father_window,text="打开",command=started)
                button7.grid(row=4,column=0)
                button8=tk.Button(father_window,text="长度",command=started)
                button8.grid(row=4,column=1)
                button9=tk.Button(father_window,text="类型",command=started)
                button9.grid(row=4,column=2)
                button0=tk.Button(father_window,text="列表",command=started)
                button0.grid(row=5,column=0)
                button10=tk.Button(father_window,text="字典",command=started)
                button10.grid(row=5,column=1)
        elif a=="语句":
                '''
                try:
                        button1.destroy()
                        button2.destroy()
                        button3.destroy()
                        button4.destroy()
                        button5.destroy()
                        button6.destroy()
                        button7.destroy()
                        button8.destroy()
                        button9.destroy()
                        button0.destroy()
                        button10.destroy()
                        #button1.destroy()
                except:
                        None
                '''
                b=2
                button1=tk.Button(father_window,text="if判断语句",command=started)
                button1.grid(row=2,column=0)
                button2=tk.Button(father_window,text="for循环语句",command=started)
                button2.grid(row=2,column=1)
                button3=tk.Button(father_window,text="while循环语句",command=started)
                button3.grid(row=2,column=2)
                button4=tk.Button(father_window,text="删除语句",command=started)
                button4.grid(row=3,column=0)
                button5=tk.Button(father_window,text="通过语句",command=started)
                button5.grid(row=3,column=1)
                button6=tk.Button(father_window,text="尝试语句",command=started)
                button6.grid(row=3,column=2)
                button7=tk.Button(father_window,text="break退出循环语句",command=started)
                button7.grid(row=4,column=0)
                button8=tk.Button(father_window,text="continue退出循环语句",command=started)
                button8.grid(row=4,column=1)
                button9=tk.Button(father_window,text="返回语句",command=started)
                button9.grid(row=4,column=2)
                button0=tk.Button(father_window,text="布尔值语句",command=started)
                button0.grid(row=5,column=0)
                button10=tk.Button(father_window,text="with打开语句",command=started)
                button10.grid(row=5,column=1)
        elif a=="模块":
                '''
                try:
                        button1.destroy()
                        button2.destroy()
                        button3.destroy()
                        button4.destroy()
                        button5.destroy()
                        button6.destroy()
                        button7.destroy()
                        button8.destroy()
                        button9.destroy()
                        button0.destroy()
                        button10.destroy()
                        #button1.destroy()
                except:
                        None
                '''
                b=3
                button1=tk.Button(father_window,text="turtle绘图模块",command=started)
                button1.grid(row=2,column=0)
                button2=tk.Button(father_window,text="random随机模块",command=started)
                button2.grid(row=2,column=1)
                button3=tk.Button(father_window,text="sys系统模块",command=started)
                button3.grid(row=2,column=2)
                button4=tk.Button(father_window,text="re正则表达式模块",command=started)
                button4.grid(row=3,column=0)
                button5=tk.Button(father_window,text="resource爬虫模块",command=started)
                button5.grid(row=3,column=1)
                button6=tk.Button(father_window,text="csv文件模块",command=started)
                button6.grid(row=3,column=2)
                button7=tk.Button(father_window,text="os目录模块",command=started)
                button7.grid(row=4,column=0)
                button8=tk.Button(father_window,text="tkinter图形界面模块",command=started)
                button8.grid(row=4,column=1)
                button9=tk.Button(father_window,text="math数学模块",command=started)
                button9.grid(row=4,column=2)
                button0=tk.Button(father_window,text="pip第三方模块下载",command=started)
                button0.grid(row=5,column=0)
                button10=tk.Button(father_window,text="其它已安装模块（包）",command=started)
                button10.grid(row=5,column=1)
        else:
                '''
                try:
                        button1.destroy()
                        button2.destroy()
                        button3.destroy()
                        button4.destroy()
                        button5.destroy()
                        button6.destroy()
                        button7.destroy()
                        button8.destroy()
                        button9.destroy()
                        button0.destroy()
                        button10.destroy()
                        #button1.destroy()
                except:
                        None
                '''
                
                b=4
                button1=tk.Button(father_window,text="自定义函数",command=started)
                button1.grid(row=2,column=0)
                button2=tk.Button(father_window,text="类",command=started)
                button2.grid(row=2,column=1)
                button3=tk.Button(father_window,text="列表",command=started)
                button3.grid(row=2,column=2)
                button4=tk.Button(father_window,text="元组",command=started)
                button4.grid(row=3,column=0)
                button5=tk.Button(father_window,text="字典",command=started)
                button5.grid(row=3,column=1)
                button6=tk.Button(father_window,text="自定义模块",command=started)
                button6.grid(row=3,column=2)
                button7=tk.Button(father_window,text="自定义包",command=started)
                button7.grid(row=4,column=0)
                '''
                button8=tk.Button(father_window,text="长度",command=started)
                button8.grid(row=4,column=1)
                button9=tk.Button(father_window,text="类型",command=started)
                button9.grid(row=4,column=2)
                button0=tk.Button(father_window,text="列表",command=started)
                button0.grid(row=5,column=0)
                button10=tk.Button(father_window,text="字典",command=started)
                button10.grid(row=5,column=1)
                '''


numberChosen.bind("<<ComboboxSelected>>", show_button)
father_window.mainloop()
