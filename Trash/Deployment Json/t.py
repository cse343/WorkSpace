import os
command2= 'python3 test.py'

sudoPassword = 'kalyon556'


print("--------6--------")
p=os.popen('echo %s|sudo -S %s' % (sudoPassword, command2)).read()
print("\t\t\tRunning Container list:")
print(p)
