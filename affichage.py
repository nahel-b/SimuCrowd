#boucle pour l'affichage de la scene
import math
from fonction import*
import chemin

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import tkinter.font as tkFont


def initialisation_immeuble_affichage():

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



def lancer_ex_chemin(nb_etage1,taille_max1,taille_fenetre1,forme_etage1,liste_escalier_descendant1,liste_obstacle1):
    global nb_etage 
    global taille_max
    global taille_fenetre
    global forme_etage
    global liste_escalier_descendant
    global liste_obstacle
    global flecheAff
    nb_etage = nb_etage1
    taille_max = taille_max1
    taille_fenetre = taille_fenetre1
    forme_etage = forme_etage1
    liste_escalier_descendant = liste_escalier_descendant1
    liste_obstacle = liste_obstacle1
    flecheAff = []
    global fenetre
    fenetre = Tk()                             
    fenetre.title("test segment")
    fenetre.geometry("1000x600")
    global frameExp
    frameExp = Frame(master=fenetre,width = 1000, height = 600)
    frameExp.pack()
    global CanvasExp
    CanvasExp = Canvas(frameExp,width = 1000, height = 600 ,  bg="white")
    CanvasExp.pack()
    global coord
    coord = CanvasExp.create_text(970,590,text = "",font = ('Helvetica','12','normal'))
    global distance_aff
    distance_aff = CanvasExp.create_text(970,580,text = "",font = ('Helvetica','12','normal'))
    initialisation_immeuble_affichage()
    global prochain_point 
    prochain_point = CanvasExp.create_oval(0,0,0,0,fill = 'blue')


    CanvasExp.bind("<Motion>",refresh)
    fenetre.mainloop()  


def affiche_fleche(etage_num,num_sortie,depart):
    liste_pol = liste_obstacle[etage_num]
    pol_point = deconsrtuit(liste_obstacle[etage_num])
    i = etage_num
    decalage = ((i*taille_max[0])%taille_fenetre[0],taille_max[1]*math.floor((i*taille_max[0])/taille_fenetre[0]))
    #premier point
    p = chemin.premier_point(etage_num,num_sortie,depart)[1]
    flecheAff.append(CanvasExp.create_line(depart[0]+decalage[0],depart[1]+decalage[1],p[0]+decalage[0],p[1]+decalage[1],arrow = 'last',width = 1,fill='red'))
    last = p
    fin = True
    while( fin):
        if last == liste_escalier_descendant[etage_num][num_sortie]:
            break
        p = chemin.point_sortie_etages[etage_num][num_sortie][pol_point.index(last)][1]
        flecheAff.append(CanvasExp.create_line(last[0]+decalage[0],last[1]+decalage[1],p[0]+decalage[0],p[1]+decalage[1],arrow = 'last',width = 1,fill='red'))
        last = p
        


def refresh(e):

    CanvasExp.itemconfig(coord,text = str(round(e.x)) + ";" + str(round(e.y)))
    dist_res = 0
    pos_souris = (e.x%taille_max[0],e.y%taille_max[1])
    etage_n = int(e.x/taille_max[0] ) + int(e.y/taille_max[1])*int(taille_fenetre[0]/taille_max[0])
    if etage_n>= nb_etage:
        return
    
    #choisir la premiere sortie
    res_sortie = chemin.get_plus_rapide_prochain_sortie(etage_n,pos_souris)
    i = etage_n
    decalage = ((i*taille_max[0])%taille_fenetre[0],taille_max[1]*math.floor((i*taille_max[0])/taille_fenetre[0]))
    p = chemin.premier_point(etage_n,res_sortie,pos_souris)[1]
    rayon = 3
    CanvasExp.coords(prochain_point,p[0]-rayon + decalage[0],p[1]-rayon+ decalage[1],p[0]+rayon+decalage[0],p[1]+rayon+ decalage[1])

    for obj in flecheAff:
        CanvasExp.delete(obj)
        flecheAff.pop(flecheAff.index(obj))

    #afficher les fleches
    affiche_fleche(etage_n,res_sortie,pos_souris)
    last = res_sortie
    for i in range(etage_n-1,-1,-1): 
        a = chemin.sortie_plus_rapide[i][last][1]
        affiche_fleche(i,a,liste_escalier_descendant[i+1][last])
        last = chemin.sortie_plus_rapide[i][last][1]
    
    CanvasExp.itemconfig(distance_aff,text = str(round(chemin.premier_point(etage_n,res_sortie,pos_souris)[0] + chemin.sortie_plus_rapide[etage_n][res_sortie][0],1)),fill='grey')

