import json
import os
import requests 
"""proje ismi küçük harfler ile yazılmalı"""

"""
requests 	7 test (deploy)
			2 plan (undeploy)

response 2 plan (deploy success)
		 2 plan (undeploy success)
		 2 plan (deploy unsuccesful)
		 2 plan (undeploy unsuccesful)
		 5 monitor (deploy success)
		 5 monitor (undeploy success)
		 5 monitor (deploy unsuccesful)
		 5 monitor (undeploy unsuccesful)
"""

def jsonRequestParsing():

	global projectName,repoURL,targetPswd, path 

	f =  open( path  + 'jsonRequest.json', 'r')
	if f.mode == 'r':
		distros_dict = json.load(f)
	for distro in distros_dict:
		if ( distro == "projectName" ) :
			projectName = distros_dict[distro]
		if( distro == "repoURL" ):
			repoURL = distros_dict[distro]
		if( distro == "targetPswd" ):
			targetPswd = distros_dict[distro]

	if(distros_dict[ "deployment" ] == "undeploy" and distros_dict[ "origin" ] == "2" and distros_dict[ "destination" ] == "3" ):
		undeploy()
	elif (distros_dict[ "deployment" ] == "deploy" and  distros_dict[ "origin" ] == "7" and distros_dict[ "destination" ] == "3"):
		deploy()
	if distros_dict[ "destination" ] != "3":
		print("ERROR Invalid Request! destination:",distros_dict[ "destination" ]," is incorrect.")
	if (distros_dict[ "deployment" ] == "deploy" and  distros_dict[ "origin" ] != "7"):
		print("ERROR Invalid Request! origin: ",distros_dict[ "origin" ], "deployment: deploy")
	elif(distros_dict[ "deployment" ] == "undeploy" and distros_dict[ "origin" ] != "2"):
		print("ERROR Invalid Request! origin: ",distros_dict[ "origin" ], "deployment: undeploy ")


def undeploy():

	global projectName, repoURL, targetPswd ,path
	sudoPassword = targetPswd
	deleteContainerCommand = 'sudo docker rm -f ' + str( projectName)
	displayContainerListCommand = 'sudo docker ps -a '
	displayUpContainerListCommand = 'sudo docker ps -a | grep "Up" | cut -d " " -f 1'

	a=os.popen('echo %s|sudo -S %s' % (sudoPassword, displayUpContainerListCommand )).read()
	preDeployContainerNumber = len(a.split('\n'))

	os.popen('echo %s|sudo -S %s' % (sudoPassword, deleteContainerCommand)).read()
	a=os.popen('echo %s|sudo -S %s' % (sudoPassword, displayUpContainerListCommand )).read()

	if( preDeployContainerNumber - 1 == len(a.split('\n'))):
		writeToJasonUndeployed("success",2) #plan 2
		sendJsonFile()
		writeToJasonUndeployed("success",5) #monitor  5
		sendJsonFile()
	else :
		writeToJasonUndeployed("fail",2)
		sendJsonFile()
		writeToJasonUndeployed("fail",5) 
		sendJsonFile()

def deploy():
	global projectName, repoURL, targetPswd, path
	sudoPassword = targetPswd

	imageName = projectName + "image"
	clone = "git clone " + repoURL

	os.system("if [ -d deploy ]; then rm -Rf deploy; fi")
	os.system("rm *.jar")
	os.system(clone)

	createImageCommand= 'sudo docker build -t ' + imageName + ' . '
	createContainerCommand = 'sudo docker run -d -it --name ' + projectName + ' ' + imageName
	displayContainerListCommand = 'sudo docker ps -a '
	runContainerCommand = 'gnome-terminal -e \' sh -c \"sudo docker exec -i '+ projectName + ' java -jar  settings.jar\"\''
	displayUpContainerListCommand = 'sudo docker ps -a | grep "Up" | cut -d " " -f 1'

	a=os.popen('echo %s|sudo -S %s' % (sudoPassword, displayUpContainerListCommand )).read()
	preDeployContainerNumber = len(a.split('\n'))
	
	os.system('echo %s|sudo -S %s' % (sudoPassword, createImageCommand))
	os.system('echo %s|sudo -S %s' % (sudoPassword, createContainerCommand))
	os.system('echo %s|sudo -S %s' % (sudoPassword, displayContainerListCommand))
	a=os.popen('echo %s|sudo -S %s' % (sudoPassword, displayUpContainerListCommand )).read()

	if( preDeployContainerNumber + 1 == len(a.split('\n'))):
		os.system('echo %s|sudo -S %s' % (sudoPassword, runContainerCommand))
		writeToJasonDeployed("success",2 )
		sendJsonFile()
		writeToJasonDeployed("success",5 )
		sendJsonFile()
	else :
		writeToJasonDeployed("fail",2 )
		sendJsonFile()
		writeToJasonDeployed("fail",5 )
		sendJsonFile()

def writeToJasonDeployed(info, dest ):
	global projectName ,path

	if info == "success" :		
		data= {
			'deployment':'deploy',
	    	'status': 'success',
	    	'projectName' : projectName,
			'destination': dest ,
			'origin':'3'
		}
		with open(path + 'response.json', 'w') as outfile:
			json.dump(data, outfile)

	elif info == "fail" :
		data= {
	    	'deployment':'deploy',
	    	'status': 'failed', 
	    	'projectName' : projectName,
			'destination':dest,
			'origin':'3'
		}
		with open(path + 'response.json', 'w') as outfile:
			json.dump(data, outfile)


def writeToJasonUndeployed(info, dest):
	global projectName, path
	if info == "success" :	
		data = {
			'deployment':'undeploy', 
	    	'status': 'success',
			'destination':dest,
			'projectName' : projectName,
			'origin':'3'
		}
		with open(path + 'response.json', 'w') as outfile:
			json.dump(data, outfile)

	elif info == "fail":
		data={
			'deployment':'undeploy',
	    	'status': 'failed', 
			'destination':dest ,
			'projectName' : projectName,
			'origin':'3'
		}
		with open(path + 'response.json', 'w') as outfile:
			json.dump(data, outfile)

def sendJsonFile():
	global path
	jsonFile = open(path +'response.json', 'r')
	data = json.load(jsonFile)
	print (data)
	r = requests.post(url = 'http://localhost:8080', data = json.dumps(data)) 
	sent_json = r.headers

def main():
	global projectName, repoURL, targetPswd, path
	projectName = ""
	repoURL = ""
	targetPswd = ""
	path = "/home/mel/AnypointStudio/workspace/deploy/"
	jsonRequestParsing()

if  __name__ == "__main__":
	main()

"""
requests 	7 test (deploy)
			2 plan (undeploy)

response 2 plan (deploy success)
		 2 plan (undeploy success)
		 2 plan (deploy unsuccesful)
		 2 plan (undeploy unsuccesful)
		 5 monitor (deploy success)
		 5 monitor (undeploy success)
		 5 monitor (deploy unsuccesful)
		 5 monitor (undeploy unsuccesful)
"""
