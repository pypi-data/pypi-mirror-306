'''
import pkg_resources
 
installed_packages = pkg_resources.working_set
installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
 
print("\n".join(installed_packages_list))
'''

model = ['os',
         're',
         'sys',
         'keyword',
         'turtle',
         'random',
         'tkinter',
         'csv',
         'math',
         'time',
         'datetime',
         'calender',
         'pygame',
         'numpy',
         'requests',
         'json',
         'BeautifulSoup',
         'pip',
         'pillow',
         'pandas',
         'astropy'
         ]
