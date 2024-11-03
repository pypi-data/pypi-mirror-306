import keyword, sys

__all__ = ['key_words_list',
           'out_put_key_words_list',
           'key_words'
           ]

key_words_list = keyword.kwlist

for key in ['False','None','True']:
        out_put_key_words_list = key_words_list.remove(key)
del key

key_words = {'引入模块':'import',
             '把...重命名为':'as',
             '从...中引入':'from',
             '和运算':'and',
             '或运算':'or',
             '在...中':'in',
             '无限制循环':'while',
             '遍历列表（限制循环）':'for',
             '退出本次循环':'continue',
             '结束循环':'break',
             'if判断语句(可单用)':'if',
             'elif判断语句（与if和else一起使用）':'elif',
             'else否则':'else',
             'try尝试语句':'try',
             'except接受错误语句（与try连用）':'except',
             '抛出错误':'raise',
             'with打开文件并自动关闭语句':'with',
             'del删除语句':'del',
             'return返回语句（截断函数）':'return',
             'pass替换函数语句':'pass'
             }

for keys,values in key_words.items():
        if values in (key_words_list or out_put_key_words_list):
                continue
        else:
                try:
                        del keys,key_words,key_words_list,out_put_key_words_list,keyword
                        raise SystemError("Modle keywords has an error.Try to connect programmer to deal with the problem")
                        sys.exit()
                except:
                        sys.exit()

del keys,keyword,sys
