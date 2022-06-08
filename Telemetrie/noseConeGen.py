#Genere le dxf pour le nose cone vu qu autodesk c est de la merde pour les equations
import ezdxf
import numpy as np


doc = ezdxf.new('R2010') #cree un dessin dxf au format R2010
msp = doc.modelspace() #ajoute une nouvelle entite dans le modelspace

Radius = 0.05 #rayon a la base du cone
Length = 0.45 #longueur de l ogive
n = 1/2 # type de puissance : 0 = cylindrique, 1/2 = demi-parabole, 3/4 = ?, 1 = cone
pas = 0.0005 #resolution

def powerSerie(x):
	return Radius*(x/Length)**(n)


x_list = np.arange(0, Length, 0.00001) #modele tres fin qui sera ajuste a la resolution decrite plus haut apres
polyline_temp = []
for x in x_list :
	polyline_temp.append((x,powerSerie(x),0))

#on cree en suite la polyline avec la resolution qui va bien
polyline_final = [polyline_temp[0]]
start_index = 0
for i in range(len(polyline_temp)):
	start = polyline_temp[start_index]
	end = polyline_temp[i]
	dx = end[0]-start[0]
	dy = end[1]-start[1]
	dz = end[2]-start[2]
	distance = np.sqrt(dx**2 + dy**2 + dz**2)

	if(distance > pas):
		polyline_final.append(polyline_temp[i])
		start_index = i

print(polyline_final)


#on genere le dxf
msp.add_lwpolyline(polyline_final)

"""
for pts_id in range(1,len(polyline_final)):
	msp.add_line(polyline_final[pts_id-1], polyline_final[pts_id])
doc.saveas('noseCone.dxf')
"""




"""
#exemple creation polyline
polyline = [(0,0,0),(10,0,0),(10,10,0)] #Attention les valeurs sont en metres 

for pts_id in range(1,len(polyline)):
	msp.add_line(polyline[pts_id-1], polyline[pts_id])
doc.saveas('noseCone.dxf')
"""

