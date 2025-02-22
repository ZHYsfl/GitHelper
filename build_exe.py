import os
import subprocess

# 定义要打包的Python文件和输出的exe文件名
script_name = 'GitHelper.py'  # 修改为正确的文件名
output_name = 'GitHelper.exe'

# 使用PyInstaller打包，添加图标和窗口模式
cmd = [
    'pyinstaller',
    '--onefile',  # 打包成单个文件
    '--noconsole',  # 不显示控制台窗口
    '--name', output_name,
    script_name
]

# 执行打包命令
subprocess.run(cmd)

# 清理并移动生成的exe文件到当前目录
if os.path.exists('dist/' + output_name):
    # 如果当前目录已存在同名文件，先删除
    if os.path.exists(output_name):
        os.remove(output_name)
    # 移动新生成的文件
    os.rename('dist/' + output_name, output_name)
    print(f'{output_name} 已成功生成！')
    
    # 清理临时文件和目录
    if os.path.exists('build'):
        subprocess.run(['rd', '/s', '/q', 'build'], shell=True)
    if os.path.exists('dist'):
        subprocess.run(['rd', '/s', '/q', 'dist'], shell=True)
    if os.path.exists(output_name.replace('.exe', '.spec')):
        os.remove(output_name.replace('.exe', '.spec'))
else:
    print('打包失败，请检查错误信息。') 