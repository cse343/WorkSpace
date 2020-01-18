import os
import json

path = "/home/mel/AnypointStudio/workspace/deploy/"
targetPswd=""
f =  open( path  + 'jsonRequest.json', 'r')
if f.mode == 'r':
	distros_dict = json.load(f)
for distro in distros_dict:
		if( distro == "targetPswd" ):
			targetPswd = distros_dict[distro]

print(targetPswd)
command2= 'python3 test.py'
p=os.popen('echo %s|sudo -S %s' % (targetPswd, command2)).read()

print(p)
