import builtins,re

# 使用dir()函数查看内置函数
#print("使用dir()函数查看内置函数:")
all_functions=dir(__builtins__)

#print(function)

length_all = len(all_functions)
'''
def find_str_in(fullstr,substr):
        if re.findall(substr,fullstr):
                return 1
        else:
                return 0
'''
'''
Inside obj.
thes modle and packegs are listed here.
check them
'''
'''
for a in function:
        if a == 'True' or 'False':
                function.remove(a)
        if ['E','r','r','o','r'] & set(a):
                function.remove(a)
        if ['W','a','r','n','i','n','g'] & set(a):
                function.remove(a)
        if '_' in a:
                function.remove(a)
'''
'''
for a in function:
        print(a)
        if a == ('True' or 'False') or 'None':
                try:
                        function.remove(a)
                except:
                        continue
        elif find_str_in(a,'Error'):
                try:
                        function.remove(a)
                except:
                        continue
        elif find_str_in(a,'Warning'):
                try:
                        function.remove(a)
                except:
                        continue
        elif find_str_in(a,'__'):
                try:
                        function.remove(a)
                except:
                        continue
        else:
                continue
'''
'''
list = ['True','False','None','Error','Warning','__','Exception','Ellipsis','Group','Exit','KeyboardInterrupt','NotImplemented','StopAsyncIteration','StopIteration']

out_long = 0
while length_start != out_long:
        for a in function:
                for t in list:
                        pattern = re.compile(t)
                        if re.search(pattern,a):
                                try:
                                        function.remove(a)
                                except ValueError:
                                        continue
                        else:
                                print(a)
                                continue
        length_start = len(function)
        break

print(function)
#del list,a,t
'''

function = ['abs',
            'aiter',
            'all',
            'anext',
            'any',
            'ascii',
            'bin',
            'bool',
            'breakpoint',
            'bytearray',
            'bytes',
            'callable',
            'chr',
            'classmethod',
            'compile',
            'complex',
            'copyright',
            'credits',
            'delattr',
            'dict',
            'dir',
            'divmod',
            'enumerate',
            'eval',
            'exec',
            'exit',
            'filter',
            'float',
            'format',
            'frozenset',
            'getattr',
            'globals',
            'hasattr',
            'hash',
            'help',
            'hex',
            'id',
            'input',
            'int',
            'isinstance',
            'issubclass',
            'iter',
            'len',
            'license',
            'list',
            'locals',
            'map',
            'max',
            'memoryview',
            'min',
            'next',
            'object',
            'oct',
            'open',
            'ord',
            'pow',
            'print',
            'property',
            'quit',
            'range',
            'repr',
            'reversed',
            'round',
            'set',
            'setattr',
            'slice',
            'sorted',
            'staticmethod',
            'str',
            'sum',
            'super',
            'tuple',
            'type',
            'vars',
            'zip']


functions = {
        "打印函数":"print",
        "输入函数":"input",
        "字符串":"str",
        "整数":"int",
        "小数（浮点数）":"float",
        "创建等差数列":"range",
        "打开文件":"open",
        "列表长短":"len",
        "查看数值类型":"type",
        "列表":"list",
        "查看现在全部数值名":"dir",
        "退出":"exit"
        }

error_functions=['ArithmeticError',
                 'AssertionError',
                 'AttributeError',
                 'BlockingIOError',
                 'BrokenPipeError',
                 'BufferError',
                 'ChildProcessError',
                 'ConnectionAbortedError',
                 'ConnectionError',
                 'ConnectionRefusedError',
                 'ConnectionResetError',
                 'EOFError',
                 'EnvironmentError',
                 'FileExistsError',
                 'FileNotFoundError',
                 'FloatingPointError',
                 'IOError',
                 'ImportError',
                 'IndentationError',
                 'IndexError',
                 'InterruptedError',
                 'IsADirectoryError',
                 'KeyError',
                 'LookupError',
                 'MemoryError',
                 'ModuleNotFoundError',
                 'NameError',
                 'NotADirectoryError',
                 'NotImplementedError',
                 'OSError',
                 'OverflowError',
                 'PermissionError',
                 'ProcessLookupError',
                 'RecursionError',
                 'ReferenceError',
                 'RuntimeError',
                 'SyntaxError',
                 'SystemError',
                 'TabError',
                 'TimeoutError',
                 'TypeError',
                 'UnboundLocalError',
                 'UnicodeDecodeError',
                 'UnicodeEncodeError',
                 'UnicodeError',
                 'UnicodeTranslateError',
                 'ValueError',
                 'WindowsError',
                 'ZeroDivisionError']

warnings_functions=['BytesWarning',
                    'DeprecationWarning',
                    'EncodingWarning',
                    'FutureWarning',
                    'ImportWarning',
                    'PendingDeprecationWarning',
                    'ResourceWarning',
                    'RuntimeWarning',
                    'SyntaxWarning',
                    'UnicodeWarning',
                    'UserWarning',
                    'Warning']

spe_attributes=['__build_class__',
                '__debug__',
                '__doc__',
                '__import__',
                '__loader__',
                '__name__',
                '__package__',
                '__spec__']

other_functions=['BaseException',
                 'BaseExceptionGroup',
                 'Ellipsis',
                 'Exception',
                 'ExceptionGroup',
                 'GeneratorExit',
                 'KeyboardInterrupt',
                 'NotImplemented',
                 'StopAsyncIteration',
                 'StopIteration',
                 ]

bool_type=['True',
           'False']

None_type=['None']

del re,builtins
