import os

command2= 'python3 test.py'
sudoPassword = 'kalyon556'
p=os.popen('echo %s|sudo -S %s' % (sudoPassword, command2)).read()
print(p)
