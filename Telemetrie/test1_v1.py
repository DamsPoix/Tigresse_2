from tkinter import *
import time 

#Création de la fenêtre d'affichage

fenetre = Tk()
fenetre.title('Télémétrie de Tigresse')
fenetre.geometry("1000x750")
fenetre.iconbitmap('Tigresse-2-logo.ico')
fenetre.config(background='black')


fenetre.grid_columnconfigure(0, weight=1)
fenetre.grid_columnconfigure(1, weight=1)

fenetre.grid_rowconfigure(0, weight=1)
fenetre.grid_rowconfigure(1, weight=1)
fenetre.grid_rowconfigure(2, weight=1)
fenetre.grid_rowconfigure(3, weight=1)
fenetre.grid_rowconfigure(4, weight=1)
fenetre.grid_rowconfigure(5, weight=1)
fenetre.grid_rowconfigure(6, weight=1)
fenetre.grid_rowconfigure(7, weight=1)
fenetre.grid_rowconfigure(8, weight=3)
fenetre.grid_rowconfigure(9, weight=1)
fenetre.grid_rowconfigure(10, weight=1)
fenetre.grid_rowconfigure(11, weight=1)
fenetre.grid_rowconfigure(12, weight=1)
fenetre.grid_rowconfigure(13, weight=1)
fenetre.grid_rowconfigure(14, weight=1)


valeurtest = 3

def maj ():
    etatLiaisonGPS_de.set('Etat de la liaison GPS : ' + str(valeurtest))
    etatLiaisonTelem_de.set('Etat de la Liaison Telem : ' + str(valeurtest))
    Altitude_de.set('Altitude : ' + str(valeurtest))
    Vitesse_de.set('Vitesse : '+ str(valeurtest))
    distancefusee_de.set('Distance fusée - nous : ' + str(valeurtest))
    

etatLiaisonGPS_de = StringVar()
etatLiaisonTelem_de = StringVar()
Altitude_de = StringVar()
Vitesse_de = StringVar()
distancefusee_de = StringVar()

maj()

#Création frame Lanceur et Récup
frameLanceur = Frame(fenetre, bg='white', bd=1, relief=SUNKEN)# bd (bordure)
frameRecup = Frame(fenetre, bg='white', bd=1, relief=SUNKEN)# bd (bordure)

frameLanceur.grid(column=0, row=0, sticky="ns") # sticky="nswe"
frameRecup.grid(column=1, row=0, sticky="ns")



#### Données Lanceur
LanceurLabel = Label(frameLanceur, text=' Donnée du lanceur ', font=("Courrier", 20), bg='white', fg='Black') #font (police et taille), bg (couleur arrière font), fg (couleur de police)
LanceurLabel.grid(column=0, row=1, sticky="nswe", padx=10, pady=10)

LiaisonGPSLabel = Label(frameLanceur, textvariable=etatLiaisonGPS_de, anchor='w' , font=("Courrier", 15), bg='white', fg='Black') 
LiaisonGPSLabel.grid(column=0, row=2, columnspan=4,sticky="nswe", padx=10, pady=10)

LiaisonTelemLabel = Label(frameLanceur, textvariable=etatLiaisonTelem_de, anchor='w', font=("Courrier", 15), bg='white', fg='Black') 
LiaisonTelemLabel.grid(column=0, row=3, sticky="nswe", padx=10, pady=10)

BlancLabel = Label(frameLanceur, text='', font=("Courrier", 15), bg='white', fg='Black') 
BlancLabel.grid(column=0, row=4, sticky="nswe", padx=10, pady=10)

AltLabel = Label(frameLanceur, textvariable=Altitude_de, anchor='w', font=("Courrier", 15), bg='white', fg='Black') #font (police et taille), bg (couleur arrière font), fg (couleur de police)
AltLabel.grid(column=0, row=5, sticky="nswe", padx=10, pady=10)

VitesseLabel = Label(frameLanceur, textvariable=Vitesse_de, anchor='w', font=("Courrier", 15), bg='white', fg='Black') #font (police et taille), bg (couleur arrière font), fg (couleur de police)
VitesseLabel.grid(column=0, row=6, sticky="nswe", padx=10, pady=10)

BlancLabel = Label(frameLanceur, text='', font=("Courrier", 15), bg='white', fg='Black') 
BlancLabel.grid(column=0, row=7)

EtapeLanceLabel = Label(frameLanceur, text='  Etape du lancement  ', font=("Courrier", 15), bg='white', fg='Black') 
EtapeLanceLabel.grid(column=0, row=8)



# Etape du lancement : case cochée

Standby = Checkbutton(frameLanceur, text='Standby', height = 1, width = 20, variable = 1)
Lift = Checkbutton(frameLanceur, text='Lift off', height = 1, width = 20)
MECO = Checkbutton(frameLanceur, text='MECO', height = 1, width = 20)
Chute = Checkbutton(frameLanceur, text='Chute deployment', height = 1, width = 20)
Landing = Checkbutton(frameLanceur, text='Landing', height = 1, width = 20)

Standby.select() # case cochée

Standby.grid(column=0, row=9)
Lift.grid(column=0, row=10)
MECO.grid(column=0, row=11)
Chute.grid(column=0, row=12)
Landing.grid(column=0, row=13)




#### Données Récupération
RecupLabel = Label(frameRecup, text='Donnée de récupération', font=("Courrier", 20), bg='white', fg='Black')
RecupLabel.grid(column=1, row=1, sticky="nswe", padx=10, pady=10)

Blanc1Label = Label(frameRecup, text=' ', font=("Courrier", 15), bg='white', fg='Black')
Blanc1Label.grid(column=1, row=2)

TrajectLabel = Label(frameRecup, text='  Trajectoire de vol  ', font=("Courrier", 15), bg='white', fg='Black') 
TrajectLabel.grid(column=1, row=3)

# Trajectoire de la fusée 
hauteur=200
largeur=200
canvas_traj = Canvas(fenetre, width=largeur, height=hauteur, borderwidth=5, highlightthickness=0, bg="white")
canvas_traj.create_text(largeur/2,15+hauteur/2, text= "Départ", fill="Black")

canvas_traj.create_oval(5,5,largeur,hauteur, outline="black", width=1)
canvas_traj.create_line(largeur/2-5,hauteur/2-5, largeur/2+5, hauteur/2+5, fill="black", width=1)
canvas_traj.create_line(largeur/2-5,hauteur/2+5, largeur/2+5, hauteur/2-5, fill="black", width=1)
#canvas_traj.grid(column=1, row=4)


DistanceLabel = Label(frameRecup, textvariable=distancefusee_de, font=("Courrier", 15), bg='white', fg='Black') 
DistanceLabel.grid(column=1, row=5)

BlancLabel = Label(frameRecup, text='', font=("Courrier", 15), bg='white', fg='Black')
BlancLabel.grid(column=1, row=6)

OrientationLabel = Label(frameRecup, text='  Orientation ', font=("Courrier", 15), bg='white', fg='Black') 
OrientationLabel.grid(column=1, row=7)

# Orientation entre la fusée et nous
hauteur=200
largeur=200
canvas_orientation = Canvas(fenetre, width=largeur, height=hauteur, borderwidth=5, highlightthickness=0, bg="white")
canvas_orientation.create_text(largeur/2,15+hauteur/2, text= "Nous", fill="Black")

canvas_orientation.create_oval(5,5,largeur,hauteur, outline="black", width=1)
canvas_orientation.create_line(largeur/2-5,hauteur/2-5, largeur/2+5, hauteur/2+5, fill="black", width=1)
canvas_orientation.create_line(largeur/2-5,hauteur/2+5, largeur/2+5, hauteur/2-5, fill="black", width=1)

canvas_orientation.grid(column=1, row=8)


#Afficher la fenetre
fenetre.mainloop()
