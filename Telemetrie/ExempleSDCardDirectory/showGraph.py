import matplotlib.pyplot as plt
import numpy as np

#reading file number
index = input("Entrez le nom du fichier a exploiter : ")
path = "LOGS/" + str(index) + ".csv"
pathOutputGPS = "" + str(index) + "GPS" + ".csv"

try :
	fileO = open(pathOutputGPS,"w")
except :
	print("erreur pendant l'ouverture du fichier output")

try :
	file = open(path,"r")
except :
	print("erreur pendant l'ouverture du fichier source")

tabed = []
lines = file.readlines()

for i in range(1,len(lines)):
	buff = lines[i].split(";")
	buff2 = []
	for i in buff :
		buff2.append(i)
	tabed.append(buff2)


#creation du fichier GPS
for i in range(1,len(tabed)-1):
	if(float(tabed[i][15]) != -1 and float(tabed[i][16]) != -1):
		buff = tabed[i][15] + ";" + tabed[i][16]
		fileO.write(buff);



try :
	fileO.close()
except :
	print("impossible de fermer le fichier output")

try :
	file.close()
except :
	print("impossible de fermer le fichier source")



#fig = plt.figure()
#ax = plt.axes(projection ='3d')

Px = []
Py = []
Pz = []

for i in range(len(tabed)):
	Px.append(tabed[i][7])
	Py.append(tabed[i][8])
	Pz.append(tabed[i][9])

#print(len(Px))
#print(len(Py))
#print(len(Pz))

# plotting
#ax.plot3D(np.array(Px), np.array(Py), np.array(Pz), 'green')
#ax.set_title('3D position view')
#plt.show()

