# 打开txt文件
with open('example.txt', 'r') as file:
    lines = file.readlines()

# 遍历每一行，并修改第三行的内容
for i, line in enumerate(lines):
    if i == 2:  # 第三行
        lines[i] = 'This is the modified line\n'

# 将修改后的内容写回文件
with open('example.txt', 'w') as file:
    file.writelines(lines)
