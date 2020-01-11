import sys
import os


#TO DO proje birleştirildiğinde dosya yolları düzenlenecek
path  = "/home/f/Desktop/proje1" 
path2  = "/home/f/Desktop/proje1/deploy" 
clone = "git clone https://github.com/osmancetin10/deploy.git" 

os.chdir(path) # Specifying the path where the cloned project needs to be copied
os.system("if [ -d deploy ]; then rm -Rf deploy; fi")
#os.system("rm *.jar")

#os.system("sshpass -p your_password ssh user_name@your_localhost")
os.chdir(path) # Specifying the path where the cloned project needs to be copied
os.system(clone) # Cloning