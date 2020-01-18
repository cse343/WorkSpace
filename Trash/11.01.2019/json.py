import json
import os
import requests 
import subprocess
import threading
import time

def jsonRequestParsing():

	global containerID,repoURL,targetIP,targetPswd,source,destination

	f =  open('/home/mel/AnypointStudio/workspace/deploy/jsonRequest.json', 'r')
	if f.mode == 'r':
		distros_dict = json.load(f)

	for distro in distros_dict:
		if(distro == "ContainerID"):
				containerID = distros_dict[distro]
		if(distro == "RepoURL"):
			repoURL = distros_dict[distro]
		if(distro == "TargetIP"):
			targetIP = distros_dict[distro]
		if(distro == "TargetPswd"):
			targetPswd = distros_dict[distro]
		if(distro == "Destination"):
			destination = distros_dict[distro]
		if(distro == "Source"):
			source = distros_dict[distro]
	
	if(distros_dict["Deployment"]=="Undeploy"):
		undeploy()
	elif (distros_dict["Deployment"]=="Deploy"):
		deploy()


def undeploy():
	print("--------UNDEPLOY--------")
	global containerID,repoURL,targetIP,targetPswd,source,destination
	sudoPassword = targetPswd
	undeployCommand= 'sudo docker rm -f ' + str( containerID)
	listRunningContainersCommand= 'sudo docker ps'

	p=os.popen('echo %s|sudo -S %s' % (sudoPassword, listRunningContainersCommand)).read()
	print("Running Container list:")
	print(p)

	# Selects State up containers with this command sudo docker ps -a | grep "Up" | cut -d " " -f 1
	p=os.popen('echo %s|sudo -S sudo docker ps -a | cut -d " " -f 1' % (sudoPassword)).read()
	print("State Up Container :",p)
	print("Given Container ID :", containerID)

	containerlist = p.split('\n')
	
	# Check if there is a container that matches the containerID
	flag=0
	for i in range(0 , len(containerlist)):
		if containerlist[i] == containerID :
			flag = 1 

	if flag == 1 :
		# There is a container that matches the containerID
		print("Deleting Container:")
		p=os.popen('echo %s|sudo -S %s' % (sudoPassword, undeployCommand)).read()
		#print(p)

		a=None
		a=os.popen('echo %s|sudo -S sudo docker ps -a | cut -d " " -f 1' % (sudoPassword)).read()
		print("Container List:") 
		print(a)

		if (flag == 1) :
			writeToJasonUndeployed("success")
			sendJsonFile()
		else :
			writeToJasonUndeployed("fail")
			sendJsonFile()
	else :
		# There is no container that matches the containerID
		writeToJasonUndeployed("fail")
		sendJsonFile()


def deploy():
	global containerID,repoURL,targetIP,targetPswd,source,destination
	sudoPassword=targetPswd

	print("--------DEPLOY--------")

	os.system("sudo")
	path  = "/home/mel/AnypointStudio/workspace/deploy"
	clone = "git clone " + repoURL 
	os.system('if [ -d deploy ]; then rm -Rf deploy; fi')
	#os.system("rm *.jar")

	#os.system("sshpass -p your_password ssh user_name@your_localhost")
	p=os.popen('echo %s|sudo -S %s' % (sudoPassword,clone)).read()
	print(p)

	time.sleep(2)
	#checking containers that status is UP before deployment.
	listRunningContainersCommand= 'sudo docker ps'
	a=os.popen('echo %s|sudo -S sudo docker ps -a | grep "Up" | cut -d " " -f 1' % (sudoPassword)).read()
	print(a)
	preDeploy = len(a.split('\n'))


	deployCommand= 'sudo docker build -f Dockerfile -t deneme . '
	deployCommand2 = 'sudo docker run -it  -p 8080:8080 deneme'
	p= os.popen('echo %s|sudo -S %s' % (sudoPassword, deployCommand)).read()
	print("Creating Container...")
	print(p)

	p= os.popen('echo %s|sudo -S %s' % (sudoPassword, deployCommand2)).read()
	

	p=os.popen('echo %s|sudo -S %s' % (sudoPassword, listRunningContainersCommand)).read()
	a=None

	a=os.popen('echo %s|sudo -S sudo docker ps -a | grep "Up" | cut -d " " -f 1' % (sudoPassword)).read()
	print("Container ID of the Container Status is Up:")
	print(a)

	
	#checking containers that status is UP after deployment then deployment is success or not.
	containerID = a.split('\n')[0]
	if( preDeploy + 1 == len(a.split('\n'))):
		writeToJasonDeployed("success")
		sendJsonFile()
	else :
		writeToJasonDeployed("fail")
		sendJsonFile()	

		
	

def writeToJasonDeployed(info):
	data = {}
	data['Deployment'] = []
	if info == "success" :		
		data['Deployment'].append({
			'Title':'Deploy',
	    	'Status': 'Success',
	    	'ContainerID' : containerID ,
			'Destination':destination,
			'Source':source
		})
	elif info == "fail" :
		data['Deployment'].append({
	    	'Title':'Deploy',
	    	'Status': 'Failed', 
	    	'ContainerID' : "",
			'Destination':destination,
			'Source':source
		})
	with open('/home/mel/AnypointStudio/workspace/deploy/response.json', 'w') as outfile:
	    json.dump(data, outfile)

def writeToJasonUndeployed(info):
	data = {}
	data['Deployment'] = []
	if info == "success" :	
		data['Deployment'].append({
	    	'Title':'Undeploy', 
	    	'Status': 'Success',
			'Destination':destination,
			'Source':source
		})
	elif info == "fail":
		data['Deployment'].append({
			'Title':'Undeploy',
	    	'Status': 'Failed', 
			'Destination':destination,
			'Source':source
		})
	with open('/home/mel/AnypointStudio/workspace/deploy/response.json', 'w') as outfile:
	    json.dump(data, outfile)


def sendJsonFile():
	jsonFile = open(r'/home/mel/AnypointStudio/workspace/deploy/response.json', 'r')
	data = json.load(jsonFile)
	print (data)

	# sending post request and saving response as response object 
	r = requests.post(url = 'http://localhost:8080', data = json.dumps(data)) 
	# extracting response text 
	sent_json = r.headers
	print("\nResponse:%s"%sent_json)


def main():
	containerID = 0
	repoURL = ""
	targetIP = ""
	targetPswd =""
	source = 0
	destination =0
	jsonRequestParsing()


if  __name__ == "__main__":
	main()





