import sys,csv

try:
        import pandas as pd
        import numpy as np
except ImportError or ModuleNotFoundError:
        error = '00010'
        sys.exit()

'''
inside model
use class txt:
        def __all__(self):
                pass
        def none(self):
                pass

all right,let's start
'''

class txt:
        type = 'a+'
        lineEND = '\n'
        open_type = 'normal'

        def __init__(self,path,way = type,lineEND = lineEND,open_type = open_type):
                self.type = type
                self.lineEND = lineEND
                self.open_type = open_type
                self.path = path
                self.way = way

        def write(self,text,end = lineEND):
                text = str(text)
                with open(self.path,self.way) as f:
                        f.write(text+end)
                        f.close()

        def read_first_line(self):
                with open(self.path,self.way) as f:
                        return f.readline()

        def read_all_lines(self):
                with open(self.path,self.way) as f:
                        return f.readline()

        def read_all_txt(self):
                with open(self.path,self.way) as f:
                        return f.read()

        def change_txt_line(self,change,linenumber):
                linenumber = int(linenumber)-1

                # 打开txt文件
                with open(self.path, self.way) as file:
                        lines = file.readlines()

                # 遍历每一行，并修改第三行的内容
                for i, line in enumerate(lines):
                        if i == 2:  # 第三行
                                lines[i] = str(linenumber)+self.lineEND

                # 将修改后的内容写回文件
                with open(self.path, 'w') as file:
                        file.writelines(lines)

class csv(txt):
        def __init__(self,path):
                pass

class TxtPathError(FileNotFoundError):

        pass
