'''
import pkg_resources
 
installed_packages = pkg_resources.working_set
installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
 
print("\n".join(installed_packages_list))
'''

model = {'通用文件模块':'os',
         '正则表达式模块':'re',
         '系统模块':'sys',
         '关键字模块':'keyword',
         '海龟绘图':'turtle',
         '随机模块':'random',
         'tkinterGUI模块':'tkinter',
         'csv表格文件模块':'csv',
         '数学模块':'math',
         'time时间模块':'time',
         'datetime简易时间模块':'datetime',
         '日历模块':'calender',
         'pygame游戏引擎':'pygame',
         'numpy高效率运行':'numpy',
         'requests爬虫':'requests',
         'json网络模块':'json',
         'BeautifulSoup爬虫':'bs4',
         'pip安装第三方模块':'pip',
         'pillow图像处理模块':'PIL',
         'pandas高效文件处理模块':'pandas',
         'astropy天文模块':'astropy'
         }
