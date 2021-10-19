"""用来顶部工具栏的状态恢复设置，通过记录前个对象，并在新对象进入时，恢复前对象的qss常态样式，同时改变新对象的激活样式实现"""


import shlex
import subprocess

if __name__ == '__main__':
    shell_cmd = 'python sub_process.py'
    cmd = shlex.split(shell_cmd)
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while p.poll() is None:
        line = p.stdout.readline()
        line = line.strip()
        if line:
            print('Subprogram output: [{}]'.format(line))
    if p.returncode == 0:
        print('Subprogram success')
    else:
        print('Subprogram failed')
