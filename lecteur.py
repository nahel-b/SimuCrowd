from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import tkinter.font as tkFont
from classe import *
import json
from classe import*
import os
import time






affichage_personne = []

change = []
zoom = 10 #10 pix = 1m

def lancer_lecteur(dataFichier1,taille_fenetre1):
    global dataFichier 
    dataFichier = dataFichier1
    global taille_fenetre
    taille_fenetre = taille_fenetre1
    global fenetre 
    fenetre = Tk()     
    fenetre.title("Lecteur")
    fenetre.geometry(str(taille_fenetre[0]+200) + "x" + str(taille_fenetre[1]))
    global frameExp
    frameExp = Frame(master=fenetre, width=taille_fenetre[0], height=taille_fenetre[1], bg="#F5F5F5")
    frameExp.pack(fill=BOTH, side=LEFT, expand=True) 
    global CanvasExp
    CanvasExp = Canvas(frameExp,width = taille_fenetre[0], height = taille_fenetre[1] ,  bg="white")
    CanvasExp.pack(fill=BOTH, side=LEFT)
    global frameMenue
    frameMenue = Frame(master=fenetre, width=200, height=taille_fenetre[1], bg="#F5F5F5")
    frameMenue.pack(fill=BOTH, side=RIGHT, expand=True)
    global l1
    l1 = LabelFrame(frameMenue, text="Informations", padx=20, width=200, pady=100, bg="#F5F5F5", relief="raised")
    l1.pack(fill="both")
    global multTemps
    multTemps = 1
    global coord
    coord = CanvasExp.create_text(30,8,text = "",font = ('Helvetica','12','normal'))


    initVisionnage()
    initialisation_immeuble_affichage()
    CanvasExp.bind("<Motion>",refresh)

    fenetre.mainloop()

def initialisation_immeuble_affichage():
    nb_etage = dataFichier.scene.batiment.nb_etage
    forme_etage = dataFichier.scene.batiment.forme_etage
    taille_max = dataFichier.scene.batiment.taille_max
    liste_escalier_descendant = dataFichier.scene.batiment.liste_escalier_descendant
    liste_obstacle = dataFichier.scene.batiment.liste_obstacle
    for i in range (nb_etage):
        decalage = ((i*taille_max[0])%taille_fenetre[0],taille_max[1]*math.floor((i*taille_max[0])/taille_fenetre[0]))
        CanvasExp.create_polygon(plus_liste(decalage,forme_etage),fill="",outline='black')
        #affiche entree/sortie
        for fleche in liste_escalier_descendant[i]:
            if i!=0 :
                #affiche entree etage i-1
                decalageBis = (((i-1)*taille_max[0])%taille_fenetre[0],taille_max[1]*math.floor(((i-1)*taille_max[0])/taille_fenetre[0]))
                milieu = (decalageBis[0]+(taille_max[0]/2),decalageBis[1]+(taille_max[1]/2))
                direction = (normal(fleche,milieu)[0]*13,normal(fleche,milieu)[1]*13)
                CanvasExp.create_line(decalageBis[0]+fleche[0],decalageBis[1]+fleche[1],decalageBis[0]+fleche[0]+direction[0],decalageBis[1]+fleche[1]+direction[1],arrow='last',fill ='blue')
                #affiche sortie etage i
                milieu = (decalage[0]+(taille_max[0]/2),decalage[1]+(taille_max[1]/2))
                direction2 = (normal(milieu,fleche)[0]*13,normal(milieu,fleche)[1]*13)
                CanvasExp.create_line(decalage[0]+fleche[0],decalage[1]+fleche[1],decalage[0]+fleche[0]+direction[0],decalage[1]+fleche[1]+direction[1],arrow='first',fill ='red')
            else :
                rayon = 5
                CanvasExp.create_oval(fleche[0]-rayon,fleche[1]-rayon,fleche[0]+rayon,fleche[1]+rayon,fill = 'green')
        #affiche obstacles
        for obstacle in liste_obstacle[i]:
                CanvasExp.create_polygon(plus_liste(decalage,obstacle),fill="black",outline='black')


def get_etage(id,temps):
    liste_etage = dataFichier.scene.liste_personne[id].liste_etage
    res = liste_etage[0][1]
    for i in range(len(liste_etage)):
        if(len(liste_etage) == i+1):
            return liste_etage[i][1]
        if(liste_etage[i+1][0] > temps):
            return liste_etage[i][1]


def ScaleMouse(e):
    global play
    play = False
    playbtn.config(text = ">")

def update_pos():
    temps = round(float(scaleObj.get()))
    indaff = 0
    taille_max = dataFichier.scene.batiment.taille_max
    for p in dataFichier.scene.liste_personne:
        i = get_etage(p.id,temps)
        decalage = ((i*taille_max[0])%taille_fenetre[0],taille_max[1]*math.floor((i*taille_max[0])/taille_fenetre[0]))
        print("decalage : "  + str(decalage))

        CanvasExp.coords(affichage_personne[indaff],
        ((p.positions[temps][0]-(p.largeur/2))*zoom+decalage[0]), 
        ((p.positions[temps][1]-(p.largeur/2))*zoom+decalage[1]),
        ((p.positions[temps][0]+(p.largeur/2))*zoom+decalage[0]),
        ((p.positions[temps][1]+(p.largeur/2))*zoom+decalage[1]))
        indaff = indaff +1


def ScaleUpdate(e):
    LabelTemps.config(text="temps : " + str(int(scaleObj.get()/60)) + "s")
    update_pos()


def playbtnset():
    global play
    global playbtn
    
    if not play:
        playbtn.config(text = "II")
    else:
        playbtn.config(text = ">")
    play = not play
    updatePlay()
    
def multbtnset():
    global multbtn
    global multTemps
    if multTemps <  128:
        multTemps = multTemps*2
    else :
        multTemps = 1
    multbtn.config(text ="x" + str(multTemps))
    
  
def updatePlay():
    global play
    global scaleObj
    global multTemps
    if play:    
        scaleObj.set( round ((scaleObj.get() + (multTemps*60/20)) % dataFichier.temps))
        LabelTemps.config(text="temps : " + str(int(scaleObj.get()/60)) + "s")
        fenetre.after(round(1000/20),updatePlay)
        
    
def initVisionnage():
    global l1
    global LabelTemps
    global scaleObj
    global play
    global playbtn
    global multbtn
    global multTemps
    global clcframe
    global tempsAjj
    global tempsVar
    global affichage_personne
    affichage_personne = []
    play = False
    
    for p in dataFichier.scene.liste_personne:
        affichage_personne.append(CanvasExp.create_oval(
        (p.positions[0][0]-(p.largeur/2))*zoom, 
        (p.positions[0][1]-(p.largeur/2))*zoom, 
        (p.positions[0][0]+(p.largeur/2))*zoom,
        (p.positions[0][1]+(p.largeur/2))*zoom,fill=p.couleur))


    tempsVar = StringVar()
    tempsVar.set(str(dataFichier.temps/60))
    informationsAff = []
    ModeAff = Label(l1, text="mode : Visionnage",anchor='w',bg="#F5F5F5", width=200)
    ModeAff.pack()
    Nbpers = Label(l1, text="personnes : " + str(len(dataFichier.scene.liste_personne)),anchor='w',bg="#F5F5F5", width=200)
    Nbpers.pack()
    LabelTemps = Label(l1, text="temps : 0s",anchor='w',bg="#F5F5F5", width=200)
    LabelTemps.pack()
    
    f2 = Frame(master=l1, width=100, height=200,padx=0,bg="#F5F5F5")
    f2.pack(fill="both" )
    Label(f2, text="Ajouter : ",anchor='w',bg="#F5F5F5", width=7).pack(side = LEFT,fill ="both")
    tempsAjj = StringVar()
    tempsAjj.set(str(0))
    # ss1 = Spinbox(f2,from_  = 0,to=540,wrap = False,width = 3,textvariable = tempsAjj)
    # ss1.pack(side = LEFT)
    # ss1.bind('<Return>',lambda event : AjjTemps())
    # Button(f2,text="go",command = lambda  : AjjTemps() ,width = 2).pack(side = RIGHT)
    
    
    f1 = Frame(master=l1, width=100, height=200,padx=0,bg="#F5F5F5")
    f1.pack(fill="both" )
    multbtn = Button(f1,text="x1",command = multbtnset,width = 1)
    multbtn.pack(side = LEFT)
    playbtn = Button(f1,text=">",command = playbtnset,width = 1)
    playbtn.pack(side = LEFT)
    scaleObj = Scale(l1,command = ScaleUpdate,showvalue=False, orient='horizontal', from_=0, to=dataFichier.temps, resolution=1, tickinterval=0, length=200)
    scaleObj.pack(side = LEFT,fill ="both")
    scaleObj.set(0)
    scaleObj.bind('<Button-1>',ScaleMouse)
    
    
    # clcframe = Frame(master=frameMenue, height=50, bg="#F5F5F5",pady = 20)
    # clcframe.pack(side = 'bottom')
    # clcbtn = Button(clcframe,text="Editer!",command = editer,width = 4)
    # clcbtn.pack(side = 'top')
    #Label(l1, text="temps : ",anchor='w',bg="#F5F5F5", width=9).pack(side = LEFT,fill ="both")



def setTemps():
    dataFichier.temps = float(tempsVar.get())*60



        
#--- ouvrir experience deja existente
# menubar = Menu(fenetre)
# fenetre.config(menu=menubar)
# menufichier = Menu(menubar,tearoff=0)
# menubar.add_cascade(label="Fichier", menu=menufichier)
# menufichier.add_command(label="Ouvrir ",command=ouvrir)
# menufichier.add_command(label="Nouveau ",command=ouvrir)



    
def refresh(e):
    CanvasExp.itemconfig(coord,text = str(round(e.x)) + ";" + str(round(e.y)))
   





