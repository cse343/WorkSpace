import sys
import os
import time

sudoPassword = "kalyon556"
#TO DO proje birleştirildiğinde dosya yolları düzenlenecek
path  = "/home/mel/Desktop/proje1" 
clone = "git clone https://github.com/osmancetin10/deploy.git"  

os.chdir(path) # Specifying the path where the cloned project needs to be copied
os.system("if [ -d deploy ]; then rm -Rf deploy; fi")
#os.system("rm *.jar")

#os.system("sshpass -p your_password ssh user_name@your_localhost")
os.chdir(path) # Specifying the path where the cloned project needs to be copied
os.system(clone) # Cloning

time.sleep(3)

listRunningContainersCommand= 'sudo docker ps'
a=os.popen('echo %s|sudo -S sudo docker ps -a | grep "Up" | cut -d " " -f 1' % (sudoPassword)).read()
print(a)
preDeploy = len(a.split('\n'))

os.system("pwd")
deployCommand= 'sudo docker build -f Dockerfile -t deneme . '
deployCommand2 = 'sudo docker run -t deneme'

print("Creating Container...")
p= os.system('echo %s|sudo -S %s' % (sudoPassword, deployCommand))
print(p)

p= os.system('echo %s|sudo -S %s' % (sudoPassword, deployCommand2))
print(p)

p=os.popen('echo %s|sudo -S %s' % (sudoPassword, listRunningContainersCommand)).read()

a=os.popen('echo %s|sudo -S sudo docker ps -a | grep "Up" | cut -d " " -f 1' % (sudoPassword)).read()
print("Container ID of the Container Status is Up:")
print(a)