fp = open("test.py", "r")
line = fp.readline()

cnt = 0
lines = []
while line:
	if(not(line[0] == '#' or (len(line)==1 or (len(line)==2 and line[0]=='\t')))):
		cnt += 1
		lines.append(line)
	line = fp.readline()
   

print "Lines Of Code :", cnt