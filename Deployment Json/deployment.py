import json
import os
import requests 
import json
import subprocess

def jsonRequestParsing():

	global containerID,repoURL,targetIP,targetPswd,source,destination

	with open('/home/mel/Desktop/software/python/jsonRequest.json', 'r') as f:
		distros_dict = json.load(f)

	for distro in distros_dict:
		if(distro == "containerID"):
				containerID = distros_dict[distro]
		if(distro == "repoURL"):
			repoURL = distros_dict[distro]
		if(distro == "targetIP"):
			targetIP = distros_dict[distro]
		if(distro == "targetPswd"):
			targetPswd = distros_dict[distro]
		if(distro == "destination"):
			destination = distros_dict[distro]
		if(distro == "source"):
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

	print("\t\t\t-------------------  \n\t\t\t------- 1 ---------  \n\t\t\t-------------------  \n")
	p=os.popen('echo %s|sudo -S %s' % (sudoPassword, listRunningContainersCommand)).read()
	print("\t\t\tRunning Container list:")
	print(p)

	# Selects State up containers with this command sudo docker ps -a | grep "Up" | cut -d " " -f 1
	p=os.popen('echo %s|sudo -S sudo docker ps -a | grep "Up" | cut -d " " -f 1' % (sudoPassword)).read()
	print("\t\t\tState Up Container:")
	print(p)
	print("\t\t\tGiven Container ID:")
	print(containerID)

	containerlist = p.split('\n')
	
	# Check if there is a container that matches the containerID
	flag=0
	for i in range(0 , len(containerlist)):
		if containerlist[i] == containerID :
			flag =1 

	if flag == 1 :
		# There is a container that matches the containerID
		print("\t\t\t-------------------  \n\t\t\t------- 2 ---------  \n\t\t\t-------------------  \n")
		print("\t\t\tDeleting Container:")
		p=os.popen('echo %s|sudo -S %s' % (sudoPassword, undeployCommand)).read()
		print(p)

		print("\t\t\t-------------------  \n\t\t\t------- 3 ---------  \n\t\t\t-------------------  \n")
		a=None
		a=os.popen('echo %s|sudo -S sudo docker ps -a | grep "Up" | cut -d " " -f 1' % (sudoPassword)).read()
		print("\t\t\tRunning Container List:")
		print(a)
		#if there isn't any containers running it is succesfull
		print("##",a,"##")

		if (len(a) <= 2) :
			writeToJasonDeployed("success")
			sendJsonFile()
		else :
			writeToJasonDeployed("fail")
			sendJsonFile()
	else :
		# There is no container that matches the containerID
		writeToJasonDeployed("fail")
		sendJsonFile()

def deploy():
	"""
	TODO
	If the container should stay in state up:
	to fix the problem open a second terminal to see if there is a container created, 

	If the container is in state exited no need to open second terminal. Works fine.

	"""
	print("--------DEPLOY--------")
	global containerID,repoURL,targetIP,targetPswd,source,destination
	"""TODO"""	
	programName = "wordpress"
	"""TODO"""
	sudoPassword=targetPswd
	deployCommand= 'sudo docker run '+ str( programName)
	listRunningContainersCommand= 'sudo docker ps'
	
	p = os.popen('echo %s|sudo -S %s' % (sudoPassword, listRunningContainersCommand)).read()
	print("\t\t\t-------------------  \n\t\t\t------- 1 ---------  \n\t\t\t-------------------  \n")
	print("\t\t\tRunning Container list:")
	print(p)

#	p= os.popen('echo %s|sudo -S %s' % (sudoPassword, deployCommand)).read()
	print("\t\t\t-------------------  \n\t\t\t------- 2 ---------  \n\t\t\t-------------------  \n")
	print("\t\t\tCreating Container")
	print(p)

	p=os.popen('echo %s|sudo -S %s' % (sudoPassword, listRunningContainersCommand)).read()
	print("\t\t\t-------------------  \n\t\t\t------- 3 ---------  \n\t\t\t-------------------  \n")
	print("\t\t\tRunning Container List:")
	print(p)
	a=None
	a=os.popen('echo %s|sudo -S sudo docker ps -a | grep "Up" | cut -d " " -f 1' % (sudoPassword)).read()
	print("\t\t\t-------------------  \n\t\t\t------- 4 ---------  \n\t\t\t-------------------  \n")
	print("\t\tContainer ID of the Container Status is Up:")
	print(a)
	#If a isn't null there is a running container.
	containerID=None
	containerID = a.split('\n')[0]

	#change the condition
	if (containerID != None) :
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
	    	'State': 'Success',
	    	'Deployment':'Deploy', 
	    	'ContainerID' : containerID ,
			'destination':destination,
			'source':source
		})
	elif info == "fail" :
		data['Deployment'].append({
	    	'State': 'Failed',
	    	'Deployment':'Deploy', 
	    	'ContainerID' : containerID ,
			'destination':destination,
			'source':source
		})
	with open('/home/mel/Desktop/software/python/response.json', 'w') as outfile:
	    json.dump(data, outfile)

def writeToJasonUndeployed(info):
	data = {}
	data['Deployment'] = []
	if info == "success" :	
		data['Deployment'].append({
	    	'State': 'Success',
	    	'Deployment':'Undeploy', 
			'destination':destination,
			'source':source
		})
	elif info == "fail":
		data['Deployment'].append({
	    	'State': 'Failed',
	    	'Deployment':'Undeploy', 
			'destination':destination,
			'source':source
		})
	with open('/home/mel/Desktop/software/python/response.json', 'w') as outfile:
	    json.dump(data, outfile)


def sendJsonFile():
	jsonFile = open(r'/home/mel/Desktop/software/python/response.json', 'r')
	data = json.load(jsonFile)
	print (data)

	# sending post request and saving response as response object 
	r = requests.post(url = 'http://localhost:8080', data = json.dumps(data)) 
	# extracting response text 
	sent_json = r.headers
	print("\nResponse:%s"%sent_json)

containerID = 0
repoURL = ""
targetIP = ""
targetPswd =""
source = 0
destination =0
jsonRequestParsing()

#os.system("gnome-terminal --disable-factory")


""" TODO
container ID  = sudo docker ps -a | grep "Up" | cut -d " " -f 1
"""





