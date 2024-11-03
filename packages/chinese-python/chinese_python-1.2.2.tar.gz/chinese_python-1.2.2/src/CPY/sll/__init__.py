'''
This is a model that write and run .py.
'''

import os
import subprocess
from pathlib import Path

class txt():
        def __init__(self,path='/',way='a+'):
                a=open(path,ways)
                a.close()
                pass
        def __new__(self):
                pass
        def writeline(self,text):
                text=str(text)
                with open(path,way) as a:
                        a.write(text+"\n")
        def write(self,text):
                text=str(text)
                with open(path,way) as a:
                        a.write(text)
        def read_oneline(self):
                with open(path,"w+") as f:
                        txt=f.readline()
                        f.close()
                        return txt

        def read_all_notlist(self):
                with open(path,"w+") as f:
                        txt=f.read()
                        f.close()
                        return txt

        def read_all_inlist(self):
                with open(path,"w+") as f:
                        txt=f.readlines()
                        f.close()
                        return txt

def movetxt(oldpath,newpath):
    if (os.path.exists(oldpath) and os.path.exists(newpath)):
        for a,b in os.path.split(oldpath):
            os.path.join(newpath,b)
        del a,b
        pass
    else:
        raise FileNotFoundError(f"Can not fond",oldpath,newpath)
        pass

def findfile(path,file):
    filelist=[]
    if os.path.exists(path):
        for f in os.listdir(path):
            temp_dir = os.path.join(path, f)
            if os.path.isfile(temp_dir) and temp_dir.endswith(file):
                for a,b in os.path.split(temp_dir):
                    filelist.append(b)
                '''
            elif os.path.isdir(temp_dir):
                get_file_list(temp_dir, file, filelist)
                '''
        return filelist
        del a,b
    else:
        raise FileNotFoundError(f"Can not fond",path)
        pass

def findallfile(path,file):
    filelist=[]
    if os.path.exists(path):
        for f in os.listdir(path):
            temp_dir = os.path.join(path, f)
            if os.path.isfile(temp_dir) and temp_dir.endswith(file):
                for a,b in os.path.split(temp_dir):
                    filelist.append(b)
            elif os.path.isdir(temp_dir):
                get_file_list(temp_dir, file, filelist)
        return filelist
        del a,b
    else:
        raise FileNotFoundError(f"Can not fond",path)
        pass

class path():
    def __init__(self,path):
        if os.path.exists(path):
            pass
        else:
            os.exit()
            raise FileNotFoundError(f"Can not fond",path)
            pass
    def readpath():
        for path,dirs,files in os.walk(path):
            list=[path,dirs,files]
        return list
    def readallfile(file):
        filelist=[]
        for f in os.listdir(path):
            temp_dir = os.path.join(path, f)
            if os.path.isfile(temp_dir) and temp_dir.endswith(file):
                for a,b in os.path.split(temp_dir):
                    filelist.append(b)
            elif os.path.isdir(temp_dir):
                get_file_list(temp_dir, file, filelist)
        return filelist
        del a,b
    def readwjj():
        wjj=[]
        a=os.listdir(path)
        if os.path.isdir(a):
            wjj.append(a)
        else:
            pass
        return a
    def newfile(newpath,file):
        if os.path.exists(newpath):
            os.mkdir(file)
        else:
            raise FileNotFoundError(f"Can not fond",newpath)
            pass
    def delfile(path,file,way='0'):
        if os.path.exists(path):
            if way=='0':
                os.rmdir(file)
                pass
            elif way=='1':
                try:
                    os.removedirs(file)
                except NameError or FileNotFoundError:
                    print("can not found",file)
            else:
                raise ValueError(f"way can only be 0 or 1")
        else:
            raise FileNotFoundError(f"Can not fond",newpath)
            pass
    def deltxt(path):
        if os.path.exists(path):
            os.remove(path)
            pass
        else:
            raise FileNotFoundError(f"Can not fond",newpath)
            pass
    def rename(path,old,new):
        if os.path.exists(path):
            try:
                from os import path
                old_path=path.join(path,old)
                new_path=path.join(path,new)
                os.rename(old_path,new_path)
            except:
                from os import path
                new_path=path.join(path,new)
                with open(new_path,"a") as f:
                    f.close
                    pass
        else:
            raise FileNotFoundError(f"Can not fond",newpath)
            pass
def change_extension(path,new='.py'):
        file_path=Path(path)
        new_file_path = file_path.with_suffix(new)
 
        # 重命名文件
        return file_path.rename(new_file_path)
