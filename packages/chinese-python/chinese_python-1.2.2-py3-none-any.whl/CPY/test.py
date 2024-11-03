from tkinter import *
#import gjutil

# 初始化窗口
root = Tk()
root.title('listbox demo')
root.geometry("600x800")

# 初始化数据
array_lang_data = ['python', 'golang', 'kotlin', 'dart', 'rust']
sv_lang_list = StringVar()
sv_lang_list.set(tuple(array_lang_data))

# 初始化控件
lb_lang = Listbox(root, listvariable=sv_lang_list)
lb_lang.pack()



def get_select_item():
    try:
        item = lb_lang.get(lb_lang.curselection())
        print(item)
        label_select_display.config(text=item)
    except:
        mb.showerror(message="未选中任何选项")

#root = Tk()

label_select_display = Label(root)
btn_get_select = Button(root, text='获取数据', command=get_select_item)
        
label_select_display.pack()
btn_get_select.pack()

root.mainloop()
