from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
Files = [('Json', '*.json')]
from fonction import*
from classe import*
import math
import random
import chemin
import affichage
import lecteur
import Calcul_simulation

class FenetrePrincipale(Frame):
    def __init__(self, master=None,forme_etage=[(0.5, 0.5), (19.5, 0.5), (19.5, 29.5), (0.5, 29.5)],temps = 30,nb_etage=1,taille_max = (20,30),liste_escalier_descendant=[[]],liste_obstacle=[[]]):
        super().__init__(master)
        self.master = master
        self.master.title("Editeur")
        self.master.geometry("1200x600")
        self.pack(fill=BOTH, expand=True)

        self.temps = temps
        self.forme_etage = forme_etage
        self.nb_etage = nb_etage
        self.taille_max = taille_max
        self.liste_escalier_descendant = liste_escalier_descendant
        self.liste_obstacle = liste_obstacle
        self.taille_canvas = (1000,600)
        self.zoom = 10
        self.delta = 1
        self.liste_personne = []
        self.personne_etage = [[]]
        self.etage_obj = []
        self.last_id = 0
        self.select = None
        self.l_selection = None
        self.last_rot = 0
        self.fleche_obj = []
        self.create_widgets()

    def refresh_etage(self):

        
        for obj in self.etage_obj:
            self.canvas.delete(obj)
            

        nb_etage = self.nb_etage
        forme_etage = self.forme_etage
        taille_max = (self.taille_max[0], self.taille_max[1])
        liste_escalier_descendant = self.liste_escalier_descendant
        liste_obstacle = self.liste_obstacle
        taille_fenetre = (self.taille_canvas[0]/self.zoom,self.taille_canvas[1]/self.zoom)
        zoom = self.zoom
        for i in range (nb_etage):
            decalage = ((i*taille_max[0])%(taille_fenetre[0]),taille_max[1]*math.floor(((i)*taille_max[0])/taille_fenetre[0]))
            self.etage_obj.append( self.canvas.create_polygon(MultListe(plus_liste(decalage,forme_etage),zoom),fill="white",outline='black'))
            #affiche entree/sortie
            # rayon = 0.3
            # for fleche in liste_escalier_descendant[i]:
            #     if i!=0 :
            #         #affiche entree etage i-1
            #         decalageBis = (((i-1)*taille_max[0])%taille_fenetre[0],taille_max[1]*math.floor(((i-1)*taille_max[0])/taille_fenetre[0]))
            #         self.canvas.create_oval((fleche[0]-rayon+decalage[0])*zoom,(fleche[1]-rayon+decalage[1])*zoom,(fleche[0]+rayon+decalage[0])*zoom,(fleche[1]+rayon+decalage[1])*zoom,fill ='red')
            #     else :
            #         self.canvas.create_oval((fleche[0]-rayon)*self.zoom,(fleche[1]-rayon)*zoom,(fleche[0]+rayon)*zoom,(fleche[1]+rayon)*zoom,fill = 'green')
            # #affiche obstacles
            # for obstacle in liste_obstacle[i]:
            #         self.canvas.create_polygon(MultListe(plus_liste(decalage,obstacle),zoom),fill="black",outline='black')
            #         self.canvas.create_polygon(MultListe(plus_liste(decalage,agrandir_forme(obstacle,0.75,2)),zoom),fill="",outline='red')
        self.refresh_obstacle()
        self.refresh_personne()
    def create_widgets(self):

        
        self.canvas = Canvas(self.master, width=self.taille_canvas[0], height=self.taille_canvas[1], bg="white")
        self.canvas.pack(side=LEFT)
        self.cursor_mode = "selection"
        self.canvas.bind("<Motion>", self.refresh_curseur)
        self.canvas.bind("<MouseWheel>", self.refresh_molette)
        self.canvas.bind("<Button-1>", self.refresh_clic)
        self.canvas.bind("<Button-2>", self.refresh_clic_gauche)
        self.obstacle_placement_obj = None
        self.obstacle_placement = ([],(-1,-1))
        self.liste_obstacle_obj = [[]]
        self.liste_escalier_descendant_obj = [[]]
        self.liste_ligne_securité_obj = None
        self.current_create_obstacle_preview_line = None
        self.current_create_obstacle = []
        self.current_create_obstacle_ligne_obj = []
        self.current_create_obstacle_point_obj = []
        self.espacement = 0.5
        self.create_obstacle_termine = False
        self.afficher_coord_mod = False
        self.ajout_personne_obj = []
        self.ajout_personne_info = [[(0,0)],0,0.7,0.8,0.5]
        self.liste_personne_obj = []
        self.l_personne_label_frame = None
        self.f_menue = Frame(self.master, width=200, height=self.taille_canvas[1], bg="#F5F5F5")
        self.f_menue.pack(side=RIGHT, fill=BOTH, expand=True)
        self.l_info = LabelFrame(self.f_menue, text="Informations", padx=20, pady=20, bg="#F5F5F5")
        self.l_info.pack(fill="both",side=TOP)
        
        # self.l_debug = LabelFrame(self.f_menue, text="debug", padx=20, pady=20, bg="#F5F5F5")
        # self.l_debug.pack(fill="both",side=BOTTOM)
        # self.l_debug_text = Label(self.l_debug, text="debug",bg="#F5F5F5")
        # self.l_debug_text.pack()
        # self.l_debug_text2 = Label(self.l_debug, text="debug",bg="#F5F5F5")
        # self.l_debug_text2.pack()

        self.l_nb_personnes = Label(self.l_info, text="nb de personnes",bg="#F5F5F5")
        self.l_nb_personnes.pack()

        
       #creer une checkbutton
        checkbox = Checkbutton(self.l_info, text="Zone securité",bg="#F5F5F5", command=lambda: self.zone_securite("switch"))
        checkbox.pack()

        self.l_coord = Label(self.l_info, text="Coordonnées",bg="#F5F5F5")
        self.l_coord.pack()
        #si l_coord est cliqué on mets self.afficher_coord_mod à True
        def sw():
            self.afficher_coord_mod = not self.afficher_coord_mod
            if self.afficher_coord_mod:
                self.l_coord.config(text="modulo: activé")
            else:
                self.l_coord.config(text="modulo: désactivé")
        self.l_coord.bind("<Button-1>", lambda event: sw())


        self.refresh_etage()

        def incrementer(var):
            
            if var == "etage":
                self.nb_etage = self.nb_etage+1
                self.liste_escalier_descendant.append([])
                self.liste_escalier_descendant_obj.append([])
                self.liste_obstacle.append([])
                self.liste_obstacle_obj.append([])
                self.liste_personne_obj.append([])
                self.personne_etage.append([])
                #modifier le texte du nombre d'etage
                self.l_etage.config(text="etage: "+str(self.nb_etage))
                self.refresh_etage()

            elif var == "temps":
                    self.var_temps.set(self.var_temps.get() + 1)
                    self.temps = self.var_temps.get()
    
        def decrementer(var):

            if var == "etage":
                if self.nb_etage > 0:
                    self.nb_etage = self.nb_etage - 1
                    self.liste_escalier_descendant.pop()
                    self.liste_obstacle.pop()
                    #modifier le texte du nombre d'etage
                    self.l_etage.config(text="etage: "+str(self.nb_etage))
                    for obj in self.liste_obstacle_obj[self.nb_etage] + self.liste_escalier_descendant_obj[self.nb_etage] + self.liste_personne_obj[self.nb_etage]:
                        self.canvas.delete(obj)


                    self.liste_escalier_descendant_obj.pop()
                    self.liste_obstacle_obj.pop()
                    self.liste_personne_obj.pop()
                    
                    self.personne_etage.pop()
                    for p in self.liste_personne:
                        if p.etage[0][1] == self.nb_etage:
                            self.liste_personne.remove(p)
                    self.refresh_etage()

            elif var == "temps" and self.temps > 0:
                    self.var_temps.set(self.var_temps.get() - 1)
                    self.temps = self.var_temps.get()

        def update_temps():
            if self.var_temps.get() >0:
                self.temps = self.var_temps.get()

        def create_temps_input():
            self.f_temps = Frame(self.l_info, bg="#F5F5F5")
            self.f_temps.pack(side=TOP, fill=BOTH)
            self.l_temps = Label(self.f_temps, text="temps:",bg="#F5F5F5")
            self.l_temps.pack(side=LEFT)
            self.var_temps = IntVar()
            self.var_temps.set(0)
            self.b_plus_temps = Button(self.f_temps, text="+", width=2, command=lambda: incrementer("temps"),foreground="green")
            self.b_plus_temps.pack(side=LEFT, padx=5)
            self.b_moins_temps = Button(self.f_temps, text="-", width=2, command=lambda: decrementer("temps"),foreground="red")
            self.b_moins_temps.pack(side=LEFT)
            self.input_temps = Entry(self.f_temps, validate="key", width=3, textvariable=self.var_temps)
            self.input_temps.pack(side=LEFT)
            self.l_temps = Label(self.f_temps, text="s",bg="#F5F5F5")
            self.l_temps.pack(side=LEFT)
            self.input_temps.bind("<KeyRelease>", update_temps)
        
        create_temps_input()

        def create_nb_etage_input():
    
            self.f_etage = Frame(self.l_info, bg="#F5F5F5")
            self.f_etage.pack(side=TOP, fill=BOTH)
            self.l_etage = Label(self.f_etage, text="etage: " + str(self.nb_etage),bg="#F5F5F5")
            self.l_etage.pack(side=LEFT)
            self.b_plus_temps = Button(self.f_etage, text="+", width=2, command=lambda: incrementer("etage"),foreground="green")
            self.b_plus_temps.pack(side=LEFT, padx=5)
            self.b_moins_temps = Button(self.f_etage, text="-", width=2, command=lambda: decrementer("etage"),foreground="red")
            self.b_moins_temps.pack(side=LEFT)
            
        
        create_nb_etage_input()
         # Frame parent pour l_edition

        self.l_edition = LabelFrame(self.f_menue, text="Édition", padx=20, pady=20, bg="#F5F5F5")
        self.l_edition.pack(fill="both",side=TOP)
        
        self.b_modifier_forme_etage = Button(self.l_edition, text="Modifier forme étage", command=self.ouvrir_fenetre_modification)
        self.b_modifier_forme_etage.pack()
        
        self.b_ajouter_obstacle = Button(self.l_edition, text="Ajouter obstacle", command=self.ouvrir_fenetre_ajout_obstacle)
        self.b_ajouter_obstacle.pack()

        self.b_ajouter_escalier = Button(self.l_edition, text="Ajouter escalier", command=self.ajout_escalier)
        self.b_ajouter_escalier.pack()

        self.b_ajouter_escalier = Button(self.l_edition, text="Ajouter personnes", command=self.ouvrir_fenetre_ajout_personne)
        self.b_ajouter_escalier.pack()

        self.b_ajouter_escalier = Button(self.l_edition, text="Sélection", command=self.selection_bouton)
        self.b_ajouter_escalier.pack()

        self.b_ajouter_escalier = Button(self.l_edition, text="Flèche", command=self.fleche_bouton)
        self.b_ajouter_escalier.pack()

        def enregistrer():
            batiment = batiment_class(self.nb_etage,self.taille_max,self.forme_etage,self.liste_escalier_descendant,self.liste_obstacle)
            scene = scene_class(batiment,self.liste_personne,self.temps*60)
            fichier = fichier_class("non enregistré",scene,"edition",self.temps*60)
            #aaza
            file = asksaveasfile(filetypes = Files, defaultextension = Files)

            fichier.nom = file.name.split("/")[-1].split(".json")[0]

            saveComplet(file.name,fichier)

        def lancer_simulation():

            batiment = batiment_class(self.nb_etage,self.taille_max,self.forme_etage,self.liste_escalier_descendant,self.liste_obstacle)
            scene = scene_class(batiment,self.liste_personne,self.temps*60)
            fichier = fichier_class("non enregistré-",scene,"edition",self.temps*60)
            print("oo-" + str(self.temps))
            taille_fenetre = (1000,600)
            self.master.destroy()
            chemin.initialisation_variable(fichier.scene,taille_fenetre)
            fichier = Calcul_simulation.calcul_basique(scene,1,fichier.temps,fichier.nom)

            save(fichier.nom + 'calcul',fichier)
            lecteur.lancer_lecteur(fichier,taille_fenetre,self.zoom)
        def charger():
            ()
        #creer un menue pour enregistrer et charger dans la barre de menu
        self.menubar = Menu(self.master)
        self.menu_fichier = Menu(self.menubar, tearoff=0)
        self.menu_fichier.add_command(label="Enregistrer", command=enregistrer)
        self.menu_fichier.add_command(label="Charger", command=charger)
        self.menubar.add_cascade(label="Fichier", menu=self.menu_fichier)
        self.menu_simulation = Menu(self.menubar, tearoff=0)
        self.menu_simulation.add_command(label="Lancer", command=lancer_simulation)
        self.menubar.add_cascade(label="Simulation", menu=self.menu_simulation)
        self.master.config(menu=self.menubar)


    def fleche_bouton(self):

        batiment = batiment_class(self.nb_etage,self.taille_max,self.forme_etage,self.liste_escalier_descendant,self.liste_obstacle)
        scene = scene_class(batiment,self.liste_personne,self.temps*60)
        fichier = fichier_class("fleche test-",scene,"edition",self.temps*60)
        taille_fenetre = (1000,600)
        chemin.initialisation_variable(fichier.scene,taille_fenetre)
        print("init terminée")
        self.stop_current_task()
        self.cursor_mode = "fleche"
        self.canvas.config(cursor="plus")

    def selection_bouton(self):
        self.stop_current_task()
        self.cursor_mode = "selection"
        self.canvas.config(cursor="crosshair")

    def zone_securite(self,etat):
        if etat == "switch":
            if self.liste_ligne_securité_obj is None:
                self.liste_ligne_securité_obj = []
                taille_max = self.taille_max
                taille_fenetre = (self.taille_canvas[0]/self.zoom,self.taille_canvas[1]/self.zoom)
                for i in range (self.nb_etage):
                    decalage = ((i*taille_max[0])%(taille_fenetre[0]),taille_max[1]*math.floor(((i)*taille_max[0])/taille_fenetre[0]))
                        #affiche entree/sortie
                        # rayon = 0.3
                        # for fleche in liste_escalier_descendant[i]:
                        #     if i!=0 :
                        #         #affiche entree etage i-1
                        #         decalageBis = (((i-1)*taille_max[0])%taille_fenetre[0],taille_max[1]*math.floor(((i-1)*taille_max[0])/taille_fenetre[0]))
                        #         self.canvas.create_oval((fleche[0]-rayon+decalage[0])*zoom,(fleche[1]-rayon+decalage[1])*zoom,(fleche[0]+rayon+decalage[0])*zoom,(fleche[1]+rayon+decalage[1])*zoom,fill ='red')
                        #     else :
                        #         self.canvas.create_oval((fleche[0]-rayon)*self.zoom,(fleche[1]-rayon)*zoom,(fleche[0]+rayon)*zoom,(fleche[1]+rayon)*zoom,fill = 'green')
                        #affiche obstacles
                    for obstacle in self.liste_obstacle[i]:
                        self.liste_ligne_securité_obj.append(self.canvas.create_polygon(MultListe(plus_liste(decalage,agrandir_forme(obstacle,0.75,2)),self.zoom),fill="",outline='red'))
            else :
                for obj in self.liste_ligne_securité_obj:
                    self.canvas.delete(obj)
                self.liste_ligne_securité_obj = None
        elif etat == "refresh":
            if self.liste_ligne_securité_obj is not None:
                for obj in self.liste_ligne_securité_obj:
                    self.canvas.delete(obj)
                self.liste_ligne_securité_obj = []
                taille_max = self.taille_max
                taille_fenetre = (self.taille_canvas[0]/self.zoom,self.taille_canvas[1]/self.zoom)
                for i in range (self.nb_etage):
                    decalage = ((i*taille_max[0])%(taille_fenetre[0]),taille_max[1]*math.floor(((i)*taille_max[0])/taille_fenetre[0]))
                    for obstacle in self.liste_obstacle[i]:
                        self.liste_ligne_securité_obj.append(self.canvas.create_polygon(MultListe(plus_liste(decalage,agrandir_forme(obstacle,0.75,2)),self.zoom),fill="",outline='red'))

    def ajout_escalier(self):
        self.stop_current_task()
        self.cursor_mode = "ajout_escalier"
        self.ajout_escalier_obj = [None,None]

    def refresh_clic_gauche(self,e):
        #tourner l'obstacle actuelle de 45°
        if self.obstacle_placement != None:
            self.obstacle_placement = (tourner_forme(self.obstacle_placement[0],45/2),self.obstacle_placement[1])
            self.refresh_curseur(e)

    def refresh_obstacle(self):
        
        self.zone_securite("refresh")
        for i in range (self.nb_etage):
            taille_max = self.taille_max
            taille_fenetre = (self.taille_canvas[0]/self.zoom,self.taille_canvas[1]/self.zoom)
            zoom = self.zoom
            decalage = ((i*taille_max[0])%taille_fenetre[0],taille_max[1]*math.floor((i*taille_max[0])/taille_fenetre[0]))
            #affiche entree/sortie
            
            # for fleche in self.liste_escalier_descendant[i]:
            #     if i!=0 :
            #         #affiche entree etage i-1
            #         decalageBis = (((i-1)*taille_max[0])%taille_fenetre[0],taille_max[1]*math.floor(((i-1)*taille_max[0])/taille_fenetre[0]))
            #         self.canvas.create_oval((fleche[0]-rayon+decalage[0])*zoom,(fleche[1]-rayon+decalage[1])*zoom,(fleche[0]+rayon+decalage[0])*zoom,(fleche[1]+rayon+decalage[1])*zoom,fill ='red')
            #     else :
            #         self.canvas.create_oval((fleche[0]-rayon)*zoom,(fleche[1]-rayon)*zoom,(fleche[0]+rayon)*zoom,(fleche[1]+rayon)*zoom,fill = 'green')
            # #affiche obstacles
            #print(self.liste_escalier_descendant_obj[i])
            for obj in self.liste_escalier_descendant_obj[i]:
                self.canvas.delete(obj)

            for obj in self.liste_obstacle_obj[i] + self.liste_escalier_descendant_obj[i]:
                self.canvas.delete(obj)

            while(len(self.liste_obstacle_obj[i]) != 0):
                self.liste_obstacle_obj[i].pop()
            
            while(len(self.liste_escalier_descendant_obj[i]) != 0):
                self.liste_escalier_descendant_obj[i].pop()


            for obstacle in self.liste_obstacle[i]:
                    self.liste_obstacle_obj[i].append(self.canvas.create_polygon(MultListe(plus_liste(decalage,obstacle),zoom),fill="black",outline='black'))
                    #self.canvas.create_polygon(MultListe(plus_liste(decalage,agrandir_forme(obstacle,0.75,2)),zoom),fill="",outline='red')
            
            rayon = 3
            for sortie in self.liste_escalier_descendant[i]:
                p = ((sortie[0]+decalage[0])*self.zoom,(sortie[1]+decalage[1])*self.zoom)
                self.liste_escalier_descendant_obj[i].append(self.canvas.create_oval(p[0]-rayon,p[1]-rayon,p[0]+rayon,p[1]+rayon,fill="green",outline="green"))
                if i > 0:
                    decalage_2 = (((i-1)*taille_max[0])%taille_fenetre[0],taille_max[1]*math.floor(((i-1)*taille_max[0])/taille_fenetre[0]))
                    p2 = ((sortie[0]+decalage_2[0])*self.zoom,(sortie[1]+decalage_2[1])*self.zoom)
                    r = rayon -1
                    self.liste_escalier_descendant_obj[i].append(self.canvas.create_oval(p2[0]-r,p2[1]-r,p2[0]+r,p2[1]+r,fill="gray",outline=""))
        
    def refresh_personne(self):
        for a in self.liste_personne_obj:
            for b in a:
                self.canvas.delete(b)

        self.liste_personne_obj = [[] for i in range (self.nb_etage)]
        self.personne_etage = [[] for i in range (self.nb_etage)]
        for p in self.liste_personne:
            self.personne_etage[p.liste_etage[0][1]].append(p)
        for i in range (self.nb_etage):
            taille_max = self.taille_max
            taille_fenetre = (self.taille_canvas[0]/self.zoom,self.taille_canvas[1]/self.zoom)
            zoom = self.zoom
            decalage = ((i*taille_max[0])%taille_fenetre[0],taille_max[1]*math.floor((i*taille_max[0])/taille_fenetre[0]))
            
            for personne in self.personne_etage[i]:
                x,y,r = personne.positions[0][0]*zoom + decalage[0]*zoom,personne.positions[0][1]*zoom + decalage[1]*zoom,personne.largeur*zoom/2
                self.liste_personne_obj[i].append(self.canvas.create_oval(x-r,y-r,x+r,y+r,fill=personne.couleur,outline=personne.couleur))
    def ouvrir_fenetre_ajout_personne(self):
        self.nb_personne_curseur = 1
        self.stop_current_task()
        self.fenetre_ajout_obstacle = Toplevel(self.master)
        self.fenetre_ajout_obstacle.title("Ajout d'un obstacle" )
        self.fenetre_ajout_obstacle.geometry("560x300")
        self.canvas_ajout_obstacle = Canvas(self.fenetre_ajout_obstacle, width=300, height=300, bg='white')
        self.canvas_ajout_obstacle.pack(side=LEFT)
        #creer frame pour les boutons
        self.f_ajout_obstacle = Frame(self.fenetre_ajout_obstacle, bg="#F5F5F5")
        self.f_ajout_obstacle.pack(fill=BOTH)
        self.l_edition = LabelFrame(self.f_ajout_obstacle, text="Propriétés", padx=20, pady=20, bg="#F5F5F5")
        self.l_edition.pack(fill=BOTH,side=TOP)
        self.personne_curseur_ajuste_obj = []

        def refresh_personne_curseur():
            for p in self.personne_curseur_ajuste_obj:
                self.canvas_ajout_obstacle.delete(p)
            r = 2
            if self.var_nb_personnes.get() == 0:
                return
            
            cercles,radius = genere_cercles(float(self.var_nb_personnes.get()),float(self.var_largeur_min.get()),float(self.var_largeur_max.get()),float(self.var_espacement.get()))
            radius = (radius + float(self.var_largeur_max.get()))*10
            self.personne_curseur_ajuste_obj.append(self.canvas_ajout_obstacle.create_oval(300/2-radius,300/2-radius,300/2+radius,300/2+radius,fill="#F5F5F5",outline=""))
            for c in cercles:
                x,y,r = (c[0]*10) + (300/2),(c[1]*10) + (300/2),(c[2]*10/2)
                self.personne_curseur_ajuste_obj.append(self.canvas_ajout_obstacle.create_oval(x-r,y-r,x+r,y+r,fill="",outline="black"))
            self.ajout_personne_info = [cercles,radius/10,float(self.var_largeur_min.get()),float(self.var_largeur_max.get()),float(self.var_espacement.get())]

        def genere_cercles(num_circles, min_width, max_width,espacement):
            # Créer un cercle de départ trois fois plus grand que la largeur maximale
            radius = max_width
            # Stocker les coordonnées de chaque cercle
            circles = []
            # Compter le nombre d'essais pour chaque cercle
            attempts = 0
            # Répéter jusqu'à ce que tous les cercles soient placés
            while len(circles) < num_circles:
                # Générer une longueur aléatoire pour le rayon
                lg = random.uniform(0, radius-max_width)
                angle = random.uniform(0, 2*math.pi)
                # Calculer la position du cercle sur le cercle de rayon radius
                x = lg * math.cos(angle)
                y = lg * math.sin(angle) 

                rayon = random.uniform(min_width, max_width)
                # Vérifier s'il y a une collision avec un cercle existant
                collision = False
                for circle in circles:
                    distance = math.sqrt((x - circle[0])**2 + (y - circle[1])**2)
                    if distance < (rayon/2) + (circle[2]/2) + espacement:
                        collision = True
                        break
                # Si le cercle est en collision, réessayer une nouvelle position
                if collision:
                    attempts += 1
                    # Si plus de 100 essais ont été effectués, agrandir le cercle
                    if attempts >= 300:
                        radius *= 1.05
                        attempts = 0
                # Sinon, ajouter le cercle à la liste et réinitialiser les tentatives
                else:
                    circles.append((x, y,rayon))
                    attempts = 0
            return circles, radius-max_width
            
        def incrementer(var):
            if var == "personne":
                self.var_nb_personnes.set(str(int(self.var_nb_personnes.get()) + 1))
                refresh_personne_curseur()
            elif var == "espacement":
                self.var_espacement.set(str(round(float(self.var_espacement.get()) + 0.2,1)))
                self.espacement = float(self.var_espacement.get())
                refresh_personne_curseur()
            elif var == "espacement2":
                self.var_espacement.set(str(round(float(self.var_espacement.get()) + 0.2,1)))
                self.espacement = float(self.var_espacement.get())
         
        def decrementer(var):

            if var == "personne" and float(self.var_nb_personnes.get()) > 0:
                self.var_nb_personnes.set(str(int(self.var_nb_personnes.get()) - 1))
                refresh_personne_curseur()
            elif var == "espacement" and float(self.var_espacement.get()) > 0:
                self.var_espacement.set(str(round(float(self.var_espacement.get()) - 0.2,1)))
                self.espacement = float(self.var_espacement.get())
                refresh_personne_curseur()
            elif var == "espacement2" and float(self.var_espacement.get()) > 0:
                self.var_espacement.set(str(round(float(self.var_espacement.get()) - 0.2,1)))
                self.espacement = float(self.var_espacement.get())
            

        def create_nb_personne_input():
            self.f_nb_personne = Frame(self.l_edition, bg="#F5F5F5")
            self.f_nb_personne.pack(side=TOP, fill=BOTH)
            self.l_nb = Label(self.f_nb_personne, text="nombre:",bg="#F5F5F5")
            self.l_nb.pack(side=LEFT)
            self.var_nb_personnes = IntVar()
            self.var_nb_personnes.set(len(self.ajout_personne_info[0]))
            self.b_plus_nb = Button(self.f_nb_personne, text="+", width=2, command=lambda: incrementer("personne"),foreground="green")
            self.b_plus_nb.pack(side=LEFT, padx=5)
            self.b_moins_nb = Button(self.f_nb_personne, text="-", width=2, command=lambda: decrementer("personne"),foreground="red")
            self.b_moins_nb.pack(side=LEFT)
            self.input_nb = Entry(self.f_nb_personne, validate="key", width=3, textvariable=self.var_nb_personnes)
            self.input_nb.pack(side=LEFT)
            #appeler valide lorsque on modifie le nombre de personne dans l'entrée
            self.input_nb.bind("<Return>", lambda event: valide())
            def valide():
                refresh_personne_curseur()
                #b_valide.focus()
        create_nb_personne_input()
        def create_largeur_input():
            self.f_largeur = Frame(self.l_edition, bg="#F5F5F5")
            self.f_largeur.pack(side=TOP, fill=BOTH)
            self.l_largeur = Label(self.f_largeur, text="largeur:",bg="#F5F5F5")
            self.l_largeur.pack(side=LEFT)
            self.var_largeur_min = StringVar()
            self.var_largeur_min.set(self.ajout_personne_info[2])
            self.input_largeur_min = Entry(self.f_largeur, validate="key", width=3, textvariable=self.var_largeur_min)
            self.input_largeur_min.pack(side=LEFT)
            self.l_largeur = Label(self.f_largeur, text="à",bg="#F5F5F5")
            self.l_largeur.pack(side=LEFT)
            self.var_largeur_max = StringVar()
            self.var_largeur_max.set(self.ajout_personne_info[3])
            self.input_largeur_max = Entry(self.f_largeur, validate="key", width=3, textvariable=self.var_largeur_max)
            self.input_largeur_max.pack(side=LEFT)
            #appeler valide lorsque on modifie le nombre de personne dans l'entrée
            self.input_largeur_max.bind("<Return>", lambda event: valide())
            self.input_largeur_min.bind("<Return>", lambda event: valide())

            def valide():
                if float(self.var_largeur_max.get()) < float(self.var_largeur_min.get()):
                    self.var_largeur_max.set(self.var_largeur_min.get())
                refresh_personne_curseur()
                #b_valide.focus()
        create_largeur_input()

        def valide():
            self.cursor_mode = "ajout_personne"
            self.ajout_personne_obj = []
            self.canvas.config(cursor="cross")
            self.fenetre_ajout_obstacle.destroy()

            self.l_personne_label_frame = LabelFrame(self.f_menue, text="Curseur personne", padx=20, pady=20, bg="#F5F5F5")
            self.l_personne_label_frame.pack(fill="both",side=TOP)
            
            self.f_espacement = Frame(self.l_personne_label_frame, bg="#F5F5F5")
            self.f_espacement.pack(side=TOP, fill=BOTH)
            self.l_espacement = Label(self.f_espacement, text="nombre:",bg="#F5F5F5")
            self.l_espacement.pack(side=LEFT)
            self.var_espacement = StringVar()
            self.var_espacement.set(self.espacement)
            self.b_plus_espacement = Button(self.f_espacement, text="+", width=2, command=lambda: incrementer("espacement2"),foreground="green")
            self.b_plus_espacement.pack(side=LEFT, padx=5)
            self.b_moins_espacement = Button(self.f_espacement, text="-", width=2, command=lambda: decrementer("espacement2"),foreground="red")
            self.b_moins_espacement.pack(side=LEFT)
            self.input_espacement = Entry(self.f_espacement, validate="key", width=3, textvariable=self.var_espacement)
            self.input_espacement.pack(side=LEFT)
            #appeler valide lorsque on modifie le nombre de personne dans l'entrée
            self.input_espacement.bind("<Return>", lambda event: valide())
            def valide():
                self.espacement = float(self.var_espacement.get())
                #b_valide.focus()
        
        def create_espacement_input():
            self.f_espacement = Frame(self.l_edition, bg="#F5F5F5")
            self.f_espacement.pack(side=TOP, fill=BOTH)
            self.l_espacement = Label(self.f_espacement, text="espacement:",bg="#F5F5F5")
            self.l_espacement.pack(side=LEFT)
            self.var_espacement = StringVar()
            self.var_espacement.set(self.espacement)
            self.b_plus_espacement = Button(self.f_espacement, text="+", width=2, command=lambda: incrementer("espacement"),foreground="green")
            self.b_plus_espacement.pack(side=LEFT, padx=5)
            self.b_moins_espacement = Button(self.f_espacement, text="-", width=2, command=lambda: decrementer("espacement"),foreground="red")
            self.b_moins_espacement.pack(side=LEFT)
            self.input_espacement = Entry(self.f_espacement, validate="key", width=3, textvariable=self.var_espacement)
            self.input_espacement.pack(side=LEFT)
            #appeler valide lorsque on modifie le nombre de personne dans l'entrée
            self.input_espacement.bind("<Return>", lambda event: valide())
            def valide():
                self.espacement = float(self.var_espacement.get())
                refresh_personne_curseur()
                #b_valide.focus()
        create_espacement_input()



        b_actualiser = Button(self.l_edition, text="Actualiser", command=refresh_personne_curseur)
        b_actualiser.pack()
        #creer une separation avec separator
        separator = ttk.Separator(self.l_edition, orient=HORIZONTAL)
        separator.pack(fill=X, padx=5, pady=5)
        l = Label(self.l_edition, text=" ",bg="#F5F5F5")
        l.pack()
        b_valide = Button(self.l_edition, text="Valider", command=valide)
        b_valide.pack()
        refresh_personne_curseur()

    def refresh_molette(self, event):
        if event.delta > 0:
            self.taille_placement += 0.1
        else:
            self.taille_placement -= 0.1

        if self.taille_placement < 0.1:
            self.taille_placement = 0.1
        elif self.taille_placement > 12:
            self.taille_placement = 12

        self.refresh_curseur(event)

    def refresh_curseur(self, event):
        
        #self.l_debug_text.config(text="liste obstacle: " + str(self.liste_obstacle_obj))
        #self.l_debug_text2.config(text="l " + str(self.espacement))
        #afficher coordonnées curseur

        if self.afficher_coord_mod:
                    self.l_coord.config(text="x: " + str((round(event.x/5)*5)%(self.taille_max[0]*self.zoom)) + " y: " + str((round(event.y/5)*5)%(self.taille_max[0]*self.zoom)))
        else:
            self.l_coord.config(text="x: " + (str(round(event.x/5)*5)) + " y: " + str(round(event.y/5)*5))

        if self.cursor_mode == "obstacle_placement":
            self.canvas.config(cursor="cross")
            if self.obstacle_placement_obj != None:
                self.canvas.delete(self.obstacle_placement_obj)

            if self.obstacle_placement == ([],(-1,-1)):
                return
            

            obs = plus_liste((-self.obstacle_placement[1][0],-self.obstacle_placement[1][1]) ,self.obstacle_placement[0])
            obs = MultListe(obs, self.taille_placement)
            obs = plus_liste((event.x,event.y),obs)
            self.obstacle_placement_obj = self.canvas.create_polygon(obs, fill="gray", outline="gray")
        elif self.cursor_mode == "create_obstacle":
            if self.create_obstacle_termine:
                return
            e = Event()
            e.x = round(event.x/5)*5
            e.y = round(event.y/5)*5
            self.canvas.config(cursor="cross")
            if self.current_create_obstacle_preview_line != None:
                self.canvas.delete(self.current_create_obstacle_preview_line)
            if len(self.current_create_obstacle)>0:
                self.current_create_obstacle_preview_line = self.canvas.create_line(self.current_create_obstacle[-1][0],self.current_create_obstacle[-1][1],e.x,e.y,fill="gray")
        elif self.cursor_mode == "ajout_escalier":

            taille_fenetre = (self.taille_canvas[0]/self.zoom,self.taille_canvas[1]/self.zoom)
            etage = int(event.x/(self.taille_max[0]*self.zoom) ) + int(event.y/(self.taille_max[1]*self.zoom))*int(taille_fenetre[0]/self.taille_max[0])
            if self.ajout_escalier_obj[0] != None:
                self.canvas.delete(self.ajout_escalier_obj[0])
            if self.ajout_escalier_obj[1] != None:
                self.canvas.delete(self.ajout_escalier_obj[1])

            if etage >= self.nb_etage:
                return
            rayon = 3
            pos = (round(event.x/5)*5,round(event.y/5)*5)
            p_mod = [(pos[0]%(self.taille_max[0]*self.zoom))/self.zoom,(pos[1]%(self.taille_max[1]*self.zoom))/self.zoom]
            d_min = 1
            #on teste si p_mod est proche d'une ligne du polygon forme_etage
            

            for i in range(len(self.forme_etage)):
                p = MurPoint_point(self.forme_etage[i],self.forme_etage[(i+1)%len(self.forme_etage)],p_mod)
                if dist(p,p_mod) < d_min:
                    p_mod = [p[0],p[1]]

            for pol in self.liste_obstacle[etage]:
                for i in range(len(pol)):
                    p = MurPoint_point(pol[i],pol[(i+1)%len(pol)],p_mod)
                    if dist(p,p_mod) < d_min:
                        p_mod = [p[0],p[1]]
            
            pos = (p_mod[0]*self.zoom,p_mod[1]*self.zoom)
            taille_max = self.taille_max
            i = etage
            decalage_1 = ((i*taille_max[0])%taille_fenetre[0],taille_max[1]*math.floor((i*taille_max[0])/taille_fenetre[0]))
            obj1 = self.canvas.create_oval(pos[0]-rayon+decalage_1[0]*self.zoom,pos[1]-rayon+decalage_1[1]*self.zoom,pos[0]+rayon+decalage_1[0]*self.zoom,pos[1]+rayon+decalage_1[1]*self.zoom,fill = 'red')
            self.ajout_escalier_obj = [obj1,None]

            if etage > 0:
                #objet 2 un etage en dessous
                i = etage - 1
                decalage = ((i*taille_max[0])%taille_fenetre[0],taille_max[1]*math.floor((i*taille_max[0])/taille_fenetre[0]))
                p_2 = (p_mod[0]*self.zoom,p_mod[1]*self.zoom)
                r = rayon -1
                self.ajout_escalier_obj[1] = self.canvas.create_oval(p_2[0]-r+decalage[0]*self.zoom,p_2[1]-r+decalage[1]*self.zoom,p_2[0]+r+decalage[0]*self.zoom,p_2[1]+r+decalage[1]*self.zoom,fill = 'gray',outline='')
        elif self.cursor_mode == "ajout_personne":

            taille_fenetre = (self.taille_canvas[0]/self.zoom,self.taille_canvas[1]/self.zoom)
            etage = int(event.x/(self.taille_max[0]*self.zoom) ) + int(event.y/(self.taille_max[1]*self.zoom))*int(taille_fenetre[0]/self.taille_max[0])
            for p in self.ajout_personne_obj:
                self.canvas.delete(p)
            if etage >= self.nb_etage:
                return
            
            
            
            if self.var_nb_personnes.get() == 0:
                return
            
            radius = self.ajout_personne_info[1]*10
            self.ajout_personne_obj.append(self.canvas.create_oval(event.x-radius,event.y-radius,event.x+radius,event.y+radius,fill="",outline="#F5F5F5"))
            for c in self.ajout_personne_info[0]:
                x,y,r = (c[0]*self.zoom) + event.x,(c[1]*self.zoom) + event.y,(c[2]*self.zoom/2)
                etage_p = int(x/(self.taille_max[0]*self.zoom) ) + int(y/(self.taille_max[1]*self.zoom))*int(taille_fenetre[0]/self.taille_max[0])
                if etage_p != etage:
                    continue
                x_mod, y_mod = (x % (self.taille_max[0]*self.zoom))/self.zoom, (y % (self.taille_max[1]*self.zoom))/self.zoom
                collision = False

                for pol in self.liste_obstacle[etage_p]:
                    for i in range(len(pol)):
                        if distMurPoint(pol[i],pol[(i+1)%len(pol)],(x_mod,y_mod)) < (r/self.zoom) + self.espacement:
                            collision = True
                            break
                if not collision:
                    for p in self.personne_etage[etage_p]:
                        if dist((p.positions[0][0],p.positions[0][1]),(x_mod,y_mod)) < r/self.zoom + (p.largeur/2) +( self.espacement):
                            collision = True
                            break
                if not collision:
                    for pol in self.liste_obstacle[etage_p]:
                        if contient_polygone_point(pol,(x_mod,y_mod)):
                            collision = True
                            break
                if etage_p == etage and not collision:
                    self.ajout_personne_obj.append(self.canvas.create_oval(x-r,y-r,x+r,y+r,fill="blue",outline="black"))
        elif self.cursor_mode == "fleche":
            index_largeur = 0

            taille_fenetre = (self.taille_canvas[0]/self.zoom,self.taille_canvas[1]/self.zoom)
            # etage = int(event.x/(self.taille_max[0]*self.zoom) ) + int(event.y/(self.taille_max[1]*self.zoom))*int(taille_fenetre[0]/self.taille_max[0])
            # if etage >= self.nb_etage:
            #     return
            # p = (round(event.x/5)*5,round(event.y/5)*5)
            # pos = [(p[0]%(self.taille_max[0]*self.zoom))/self.zoom,(p[1]%(self.taille_max[1]*self.zoom))/self.zoom]
            
            
            # res_sortie = chemin.get_plus_rapide_prochain_sortie(etage,pos,index_largeur)
            # p = chemin.premier_point(etage,res_sortie,pos,index_largeur)[1]
            # #ajouter le decalage
            # taille_max = self.taille_max
            
            # decalage = ((etage*taille_max[0])%taille_fenetre[0],taille_max[1]*math.floor((etage*taille_max[0])/taille_fenetre[0]))
            # for fleche in self.fleche_obj :
            #     self.canvas.delete(fleche)
            # self.fleche_obj = []
            taille_max = self.taille_max
            e = event
            pos_souris = ((e.x/self.zoom)%taille_max[0],(e.y/self.zoom)%taille_max[1])
            etage_n = int(event.x/(self.taille_max[0]*self.zoom) ) + int(event.y/(self.taille_max[1]*self.zoom))*int(taille_fenetre[0]/self.taille_max[0])
            if etage_n>= self.nb_etage:
                return
            
            #choisir la premiere sortie
            res_sortie = chemin.get_plus_rapide_prochain_sortie(etage_n,pos_souris,index_largeur)
            i = etage_n
            decalage = ((i*taille_max[0])%taille_fenetre[0],taille_max[1]*math.floor((i*taille_max[0])/taille_fenetre[0]))
            p = chemin.premier_point(etage_n,res_sortie,pos_souris,index_largeur)[1]
            rayon = 3


            for obj in self.fleche_obj:
                self.canvas.delete(obj)
                self.fleche_obj.pop(self.fleche_obj.index(obj))

            def affiche_fleche(etage_num,num_sortie,depart):
                
                liste_pol = self.liste_obstacle[etage_num]
                pol_point = deconsrtuit(chemin.liste_obstacle[index_largeur][etage_num])
                i = etage_num
                decalage = ((i*taille_max[0])%taille_fenetre[0],taille_max[1]*math.floor((i*taille_max[0])/taille_fenetre[0]))
                #premier point
                last = chemin.premier_point(etage_num,num_sortie,depart,index_largeur)[1]
                p = ((last[0]+decalage[0])*self.zoom,(last[1]+decalage[1])*self.zoom)
                depart = ((depart[0]+decalage[0])*self.zoom,(depart[1]+decalage[1])*self.zoom)
                self.fleche_obj.append(self.canvas.create_line(depart[0],depart[1],p[0],p[1],arrow = 'last',width = 1,fill='red'))
                #last = p
                fin = True
                conteur = 0
                while( fin and conteur < 100):
                    conteur += 1
                    if last == self.liste_escalier_descendant[etage_num][num_sortie]:
                        break
                    #p = chemin.point_sortie_etages[etage_num][num_sortie][pol_point.index(last)][1]
                    #p = chemin.point_sortie_etages[etage_num][num_sortie][index_largeur][pol_point.index(last)][1]
                    a = (p== last)
                    print(a)
                    #p = chemin.premier_point(etage_num,num_sortie,last,index_largeur)[1]
                    p = chemin.point_sortie_etages[etage_num][num_sortie][index_largeur][pol_point.index(last)][1]
                    p_aff = ((p[0]+decalage[0])*self.zoom,(p[1]+decalage[1])*self.zoom)
                    last_aff = ((last[0]+decalage[0])*self.zoom,(last[1]+decalage[1])*self.zoom)
                    self.fleche_obj.append(self.canvas.create_line(last_aff[0],last_aff[1],p_aff[0],p_aff[1],arrow = 'last',width = 1,fill='red'))
                    last = p    

            #afficher les fleches
            affiche_fleche(etage_n,res_sortie,pos_souris)
            l = res_sortie
            for i in range(etage_n-1,-1,-1): 
                a = chemin.sortie_plus_rapide[index_largeur][i][l][1]
                affiche_fleche(i,a,self.liste_escalier_descendant[i+1][l])
                l = chemin.sortie_plus_rapide[index_largeur][i][l][1]
                # a = chemin.premier_point()


    
    
    def stop_current_task(self):
        self.select = None 
        self.canvas.config(cursor="arrow")
        if self.l_selection != None:
            self.l_selection.destroy()
            self.l_selection = None
        if len(self.ajout_personne_obj)>0:
            for p in self.ajout_personne_obj:
                self.canvas.delete(p)
            self.ajout_personne_obj = []
        if self.l_personne_label_frame != None:
            self.l_personne_label_frame.destroy()
            self.l_personne_label_frame = None
        if self.cursor_mode == "obstacle_placement":
            if self.obstacle_placement_obj != None:
                self.canvas.delete(self.obstacle_placement_obj)
                self.obstacle_placement_obj = None
        elif self.cursor_mode == "create_obstacle":
            if self.current_create_obstacle_preview_line != None:
                self.canvas.delete(self.current_create_obstacle_preview_line)
                self.current_create_obstacle_preview_line = None
            if self.current_create_obstacle != None:
                self.canvas.delete(self.current_create_obstacle)
                self.current_create_obstacle = None
            if self.l_obstacle_create != None:
                    self.l_obstacle_create.destroy()
                    self.l_obstacle_create = None
            self.create_obstacle_termine = False
            for i in self.current_create_obstacle_point_obj:
                self.canvas.delete(i)
            for i in self.current_create_obstacle_ligne_obj:
                self.canvas.delete(i)
            self.current_create_obstacle_point_obj = []
            self.current_create_obstacle_ligne_obj = []
            
        elif self.cursor_mode == "ajout_escalier":
            if self.ajout_escalier_obj[0] != None:
                self.canvas.delete(self.ajout_escalier_obj[0])
                self.ajout_escalier_obj[0] = None
            if self.ajout_escalier_obj[1] != None:
                self.canvas.delete(self.ajout_escalier_obj[1])
                self.ajout_escalier_obj[1] = None
        self.refresh_obstacle()

    def refresh_clic(self, e):
        if self.cursor_mode == "obstacle_placement":
            
            self.canvas.config(cursor="arrow")
            taille_fenetre = (self.taille_canvas[0]/self.zoom,self.taille_canvas[1]/self.zoom)
            etage = int(e.x/(self.taille_max[0]*self.zoom) ) + int(e.y/(self.taille_max[1]*self.zoom))*int(taille_fenetre[0]/self.taille_max[0])
            i = etage
            if etage >= self.nb_etage:
                return

            
            obs = plus_liste((-self.obstacle_placement[1][0],-self.obstacle_placement[1][1]) ,self.obstacle_placement[0])
            obs = MultListe(obs, self.taille_placement/self.zoom)
            obs = plus_liste(((e.x/10)%self.taille_max[0],(e.y/10)%self.taille_max[1]),obs)
            

            self.liste_obstacle[etage].append(obs)
            self.obstacle_placement = ([],(-1,-1))
            self.canvas.delete(self.obstacle_placement_obj)
            self.obstacle_placement_obj = None
            self.cursor_mode = "selection"
            self.refresh_obstacle()
        elif self.cursor_mode == "create_obstacle":
            if self.create_obstacle_termine:
                return
            event = Event()
            event.x = round(e.x/5)*5
            event.y = round(e.y/5)*5
            #si le point est deja dans la liste, on supprime le point
            if (event.x,event.y) in self.current_create_obstacle:
                if len(self.current_create_obstacle) < 3:
                    return
                self.create_obstacle_termine = True
                self.canvas.config(cursor="arrow")
                self.current_create_obstacle_ligne_obj.append(self.canvas.create_line(self.current_create_obstacle[-1][0],self.current_create_obstacle[-1][1],self.current_create_obstacle[0][0],self.current_create_obstacle[0][1],fill="red"))

                return
            rayon = 3
            if len(self.current_create_obstacle)==0 :
                self.current_create_obstacle = [(event.x,event.y)]
                self.current_create_obstacle_point_obj = [self.canvas.create_oval(event.x-rayon,event.y-rayon,event.x+rayon,event.y+rayon,fill="red")]
            else :
                self.current_create_obstacle.append((e.x,e.y))
                self.current_create_obstacle_point_obj.append(self.canvas.create_oval(event.x-rayon,event.y-rayon,event.x+rayon,event.y+rayon,fill="red"))
                self.current_create_obstacle_ligne_obj.append(self.canvas.create_line(self.current_create_obstacle[-2][0],self.current_create_obstacle[-2][1],self.current_create_obstacle[-1][0],self.current_create_obstacle[-1][1],fill="red"))
        elif self.cursor_mode == "ajout_escalier":

            taille_fenetre = (self.taille_canvas[0]/self.zoom,self.taille_canvas[1]/self.zoom)
            etage = int(e.x/(self.taille_max[0]*self.zoom) ) + int(e.y/(self.taille_max[1]*self.zoom))*int(taille_fenetre[0]/self.taille_max[0])
            if self.ajout_escalier_obj[0] != None:
                self.canvas.delete(self.ajout_escalier_obj[0])
            if self.ajout_escalier_obj[1] != None:
                self.canvas.delete(self.ajout_escalier_obj[1])
            if etage >= self.nb_etage:
                return

            pos = (round(e.x/5)*5,round(e.y/5)*5)
            p_mod = [(pos[0]%(self.taille_max[0]*self.zoom))/self.zoom,(pos[1]%(self.taille_max[1]*self.zoom))/self.zoom]
            d_min = 1
            #on teste si p_mod est proche d'une ligne du polygon forme_etage
            

            for i in range(len(self.forme_etage)):
                p = MurPoint_point(self.forme_etage[i],self.forme_etage[(i+1)%len(self.forme_etage)],p_mod)
                if dist(p,p_mod) < d_min:
                    p_mod = [p[0],p[1]]

            for pol in self.liste_obstacle[etage]:
                for i in range(len(pol)):
                    p = MurPoint_point(pol[i],pol[(i+1)%len(pol)],p_mod)
                    if dist(p,p_mod) < d_min:
                        p_mod = [p[0],p[1]]
            
            self.liste_escalier_descendant[etage].append((p_mod[0],p_mod[1]))
            self.refresh_etage()
            #self.cursor_mode = "selection"
        elif self.cursor_mode == "ajout_personne":
            taille_fenetre = (self.taille_canvas[0]/self.zoom,self.taille_canvas[1]/self.zoom)
            etage = int(e.x/(self.taille_max[0]*self.zoom) ) + int(e.y/(self.taille_max[1]*self.zoom))*int(taille_fenetre[0]/self.taille_max[0])
            for p in self.ajout_personne_obj:
                self.canvas.delete(p)
            if etage >= self.nb_etage:
                return
            
            if self.var_nb_personnes.get() == 0:
                return
            


            for c in self.ajout_personne_info[0]:
                x,y,r = (c[0]*self.zoom) + e.x,(c[1]*self.zoom) + e.y,(c[2]*self.zoom/2)
                etage_p = int(x/(self.taille_max[0]*self.zoom) ) + int(y/(self.taille_max[1]*self.zoom))*int(taille_fenetre[0]/self.taille_max[0])
                if etage_p != etage:
                    continue
                x_mod, y_mod = (x % (self.taille_max[0]*self.zoom))/self.zoom, (y % (self.taille_max[1]*self.zoom))/self.zoom
                collision = False

                for pol in self.liste_obstacle[etage_p]:
                    for i in range(len(pol)):
                        if distMurPoint(pol[i],pol[(i+1)%len(pol)],(x_mod,y_mod)) < r/self.zoom + self.espacement:
                            collision = True
                            break
                if not collision:
                    for p in self.personne_etage[etage_p]:
                        if dist((p.positions[0][0],p.positions[0][1]),(x_mod,y_mod)) < r/self.zoom + (p.largeur/2) +( self.espacement):
                            collision = True
                            break
                if not collision:
                    for pol in self.liste_obstacle[etage_p]:
                        if contient_polygone_point(pol,(x_mod,y_mod)):
                            collision = True
                            break
                vMax = 3.5
                Masse = 70
                if etage_p == etage and not collision:
                    p = personne_classe(c[2],vMax,(0,0),[(x_mod,y_mod)],Masse,(0,0),"blue",[(0,etage_p)],self.last_id)
                    self.last_id = self.last_id + 1
                    self.personne_etage[etage_p].append(p)
                    self.liste_personne.append(p)
            self.refresh_personne()
        elif self.cursor_mode == "selection":
            #test si on a appuyé sur une personne
            event = e
            taille_fenetre = (self.taille_canvas[0]/self.zoom,self.taille_canvas[1]/self.zoom)
            etage = int(event.x/(self.taille_max[0]*self.zoom) ) + int(event.y/(self.taille_max[1]*self.zoom))*int(taille_fenetre[0]/self.taille_max[0])
            
            if etage >= self.nb_etage:
                return
            rayon = 3
            pos = (round(event.x/5)*5,round(event.y/5)*5)
            p_mod = [(pos[0]%(self.taille_max[0]*self.zoom))/self.zoom,(pos[1]%(self.taille_max[1]*self.zoom))/self.zoom]
            d_min = 0.7
            #on teste si p_mod est proche d'une ligne du polygon forme_etage
            
            select = None

            #teste si on a appuyé sur un obstacle
            for pol in self.liste_obstacle[etage]:
                if contient_polygone_point(pol,p_mod):
                    self.select = {"type":"obstacle","obj":pol}
                    break
            
            #teste si on a appuyé sur un escalier

            for i in range(len(self.liste_escalier_descendant[etage])):
                if dist(self.liste_escalier_descendant[etage][i],p_mod) < d_min:
                    select = self.liste_escalier_descendant[etage][i]
                    self.select = {"type":"sortie","obj":select}
                    break

            for i in range(len(self.personne_etage[etage])):
                if dist(self.personne_etage[etage][i].positions[0],p_mod) < d_min:
                    select = self.personne_etage[etage][i]
                    self.select = {"type":"personne","obj":select}
                    break



            if self.l_selection != None:
                self.l_selection.destroy()
                self.l_selection = None
            #aza creation label selection
            if self.select == None:
                return
            if self.select["type"] == "personne":
                self.l_selection = LabelFrame(self.f_menue, text="Sélection personne (" + str(self.select["obj"].id) +")", padx=20, pady=20, bg="#F5F5F5")
                self.l_selection.pack(fill="both",side=TOP)
                def create_position_input():
                    self.f_pos = Frame(self.l_selection, bg="#F5F5F5")
                    self.f_pos.pack(side=TOP, fill=BOTH)
                    l_pos = Label(self.f_pos, text="x:",bg="#F5F5F5")
                    l_pos.pack(side=LEFT)
                    #variable texte
                    self.var_pos = [StringVar(),StringVar()]
                    self.var_pos[0].set(round(self.select["obj"].positions[0][0],2))
                    self.var_pos[1].set(round(self.select["obj"].positions[0][1],2))
                    self.input_pos0 = Entry(self.f_pos, validate="key", width=4, textvariable=self.var_pos[0])
                    self.input_pos0.pack(side=LEFT)
                    l_pos = Label(self.f_pos, text="y:",bg="#F5F5F5")
                    l_pos.pack(side=LEFT)
                    self.input_pos1 = Entry(self.f_pos, validate="key", width=4, textvariable=self.var_pos[1])
                    self.input_pos1.pack(side=LEFT)

                    #fonction qui met a jour la position de la personne lorque l'on change les valeurs dans les inputs
                    def update_pos(event):
                        self.select["obj"].positions[0] = (float(self.var_pos[0].get()),float(self.var_pos[1].get()))
                        self.refresh_personne()
                    self.input_pos0.bind("<KeyRelease>", update_pos)
                    self.input_pos1.bind("<KeyRelease>", update_pos)
                create_position_input()
                def create_largeur_input():
                    self.f_largeur = Frame(self.l_selection, bg="#F5F5F5")
                    self.f_largeur.pack(side=TOP, fill=BOTH)
                    l_largeur = Label(self.f_largeur, text="Largeur:",bg="#F5F5F5")
                    l_largeur.pack(side=LEFT)
                    self.var_largeur = StringVar()
                    self.var_largeur.set(round(self.select["obj"].largeur,3))
                    self.input_largeur = Entry(self.f_largeur, validate="key", width=4, textvariable=self.var_largeur)
                    self.input_largeur.pack(side=LEFT)
                    def update_largeur(event):
                        self.select["obj"].largeur = float(self.var_largeur.get())
                        self.refresh_personne()
                    self.input_largeur.bind("<KeyRelease>", update_largeur)
                create_largeur_input()
                def create_vitesseMax_input():
                    self.f_vitesseMax = Frame(self.l_selection, bg="#F5F5F5")
                    self.f_vitesseMax.pack(side=TOP, fill=BOTH)
                    l_vitesseMax = Label(self.f_vitesseMax, text="Vitesse max:",bg="#F5F5F5")
                    l_vitesseMax.pack(side=LEFT)
                    #variable texte
                    self.var_vitesseMax = StringVar()
                    self.var_vitesseMax.set(round(self.select["obj"].vitesseMax,3))
                    self.input_vitesseMax = Entry(self.f_vitesseMax, validate="key", width=4, textvariable=self.var_vitesseMax)
                    self.input_vitesseMax.pack(side=LEFT)

                    #fonction qui met a jour la position de la personne lorque l'on change les valeurs dans les inputs
                    def update_vitesseMax(event):
                        self.select["obj"].vitesseMax = float(self.var_vitesseMax.get())
                        self.refresh_personne()
                    self.input_vitesseMax.bind("<KeyRelease>", update_vitesseMax)
                create_vitesseMax_input()
                def masse_input():
                    self.f_masse = Frame(self.l_selection, bg="#F5F5F5")
                    self.f_masse.pack(side=TOP, fill=BOTH)
                    l_masse = Label(self.f_masse, text="Masse:",bg="#F5F5F5")
                    l_masse.pack(side=LEFT)
                    self.var_masse = StringVar()
                    self.var_masse.set(round(self.select["obj"].masse,3))
                    self.input_masse = Entry(self.f_masse, validate="key", width=4, textvariable=self.var_masse)
                    self.input_masse.pack(side=LEFT)
                    def update_masse(event):
                        self.select["obj"].masse = float(self.var_masse.get())
                        self.refresh_personne()
                    self.input_masse.bind("<KeyRelease>", update_masse)
                masse_input()
                def couleur_input():
                    #liste deroulante de couleur
                    self.f_couleur = Frame(self.l_selection, bg="#F5F5F5")
                    self.f_couleur.pack(side=TOP, fill=BOTH)
                    l_couleur = Label(self.f_couleur, text="Couleur:",bg="#F5F5F5")
                    l_couleur.pack(side=LEFT)
                    self.var_couleur = StringVar()
                    self.var_couleur.set(self.select["obj"].couleur)
                    couleurs = ["red","blue","green","yellow","black","white","cyan","magenta"]
                    self.input_couleur = OptionMenu(self.f_couleur, self.var_couleur, *couleurs)
                    self.input_couleur.pack(side=LEFT)
                    def update_couleur(event):
                        self.select["obj"].couleur = self.var_couleur.get()
                        self.refresh_personne()
                        self.refresh_obstacle()
                    self.input_couleur.bind("<ButtonRelease-1>", update_couleur)
                couleur_input()
                #bouton pour supprimer la personne
                def supprimer_personne():
                    try:
                        self.personne_etage[etage].remove(self.select["obj"])
                        self.liste_personne.remove(self.select["obj"])
                    except:
                        print("personne non supprimée")
                    self.select = None
                    if self.l_selection != None:
                        self.l_selection.destroy()
                        self.l_selection = None
                    self.refresh_personne()
                self.b_supprimer = Button(self.l_selection, text="Supprimer", command=supprimer_personne)
                self.b_supprimer.pack(side=TOP, fill=BOTH)
            elif self.select["type"] == "obstacle":
                self.last_rot = 0
                self.l_selection = LabelFrame(self.f_menue, text="Sélection obstacle", padx=20, pady=20, bg="#F5F5F5")
                self.l_selection.pack(fill="both",side=TOP)
                def rotation_input():
                    self.f_rotation = Frame(self.l_selection, bg="#F5F5F5")
                    self.f_rotation.pack(side=TOP, fill=BOTH)
                    l_rotation = Label(self.f_rotation, text="Rotation (º):",bg="#F5F5F5")
                    l_rotation.pack(side=LEFT)
                    self.var_rotation = IntVar()
                    self.var_rotation.set(0)
                    self.input_rotation = Entry(self.f_rotation, validate="key", width=4, textvariable=self.var_rotation)
                    self.input_rotation.pack(side=LEFT)

                    def update_rotation(event):
                        print(self.var_rotation.get() - self.last_rot)
                        new_obj = tourner_forme(self.select["obj"],self.var_rotation.get() - self.last_rot)
                        self.last_rot = self.var_rotation.get()
                        #recuperer l'index de l'obstacle dans la liste
                        index = self.liste_obstacle[etage].index(self.select["obj"])
                        #remplacer l'obstacle dans la liste
                        self.liste_obstacle[etage][index] = new_obj
                        self.select["obj"] = new_obj
                        self.refresh_obstacle()

                    self.input_rotation.bind("<KeyRelease>", update_rotation)
                rotation_input()
                #bouton pour supprimer l'obstacle
                def supprimer_obstacle():
                    try:
                        self.liste_obstacle[etage].remove(self.select["obj"])
                    except:
                        print("obstacle non supprimé")
                    self.select = None
                    if self.l_selection != None:
                        self.l_selection.destroy()
                        self.l_selection = None
                    self.refresh_obstacle()
                self.b_supprimer = Button(self.l_selection, text="Supprimer", command=supprimer_obstacle)
                self.b_supprimer.pack(side=TOP, fill=BOTH)
            elif self.select["type"] == "sortie":
                self.l_selection = LabelFrame(self.f_menue, text="Sélection sortie", padx=20, pady=20, bg="#F5F5F5")
                self.l_selection.pack(fill="both",side=TOP)

                def position_input():
                    self.f_pos = Frame(self.l_selection, bg="#F5F5F5")
                    self.f_pos.pack(side=TOP, fill=BOTH)
                    l_pos = Label(self.f_pos, text="x:",bg="#F5F5F5")
                    l_pos.pack(side=LEFT)
                    #variable texte
                    self.var_pos = [StringVar(),StringVar()]
                    self.var_pos[0].set(round(self.select["obj"][0],2))
                    self.var_pos[1].set(round(self.select["obj"][1],2))
                    self.input_pos0 = Entry(self.f_pos, validate="key", width=4, textvariable=self.var_pos[0])
                    self.input_pos0.pack(side=LEFT)
                    l_pos = Label(self.f_pos, text="y:",bg="#F5F5F5")
                    l_pos.pack(side=LEFT)
                    self.input_pos1 = Entry(self.f_pos, validate="key", width=4, textvariable=self.var_pos[1])
                    self.input_pos1.pack(side=LEFT)

                    #fonction qui met a jour la position de la personne lorque l'on change les valeurs dans les inputs
                    def update_pos(event):
                        index = self.liste_escalier_descendant[etage].index(self.select["obj"])
                        self.liste_escalier_descendant[etage][index] = (float(self.var_pos[0].get()),float(self.var_pos[1].get()))
                        self.select["obj"] = (float(self.var_pos[0].get()),float(self.var_pos[1].get()))
                        self.refresh_obstacle()
                    self.input_pos0.bind("<KeyRelease>", update_pos)
                    self.input_pos1.bind("<KeyRelease>", update_pos)
                position_input()
                #bouton pour supprimer la sortie
                def supprimer_sortie():
                    try:
                        self.liste_escalier_descendant[etage].remove(self.select["obj"])
                    except:
                        print("sortie non supprimée")
                    self.select = None
                    if self.l_selection != None:
                        self.l_selection.destroy()
                        self.l_selection = None
                    self.refresh_obstacle()
                self.b_supprimer = Button(self.l_selection, text="Supprimer", command=supprimer_sortie)
                self.b_supprimer.pack(side=TOP, fill=BOTH)
                
                    

    def ouvrir_fenetre_ajout_obstacle(self):
        self.stop_current_task()
        # Création de la fenêtre de modification
        self.fenetre_ajout_obstacle = Toplevel(self.master)
        self.fenetre_ajout_obstacle.title("Ajout d'un obstacle" )
        
        def dessiner_obstacle_canvas():

            def annuler_dernier_point():
                if self.create_obstacle_termine:
                    self.create_obstacle_termine = False
                    self.canvas.delete(self.current_create_obstacle_ligne_obj[-1])
                    self.current_create_obstacle_ligne_obj.pop()
                    return
                if len(self.current_create_obstacle)>0:
                    self.canvas.delete(self.current_create_obstacle_point_obj[-1])
                    if len(self.current_create_obstacle_point_obj)>1:
                        self.canvas.delete(self.current_create_obstacle_ligne_obj[-1])
                    self.current_create_obstacle_point_obj.pop()
                    self.current_create_obstacle_ligne_obj.pop()
                    self.current_create_obstacle.pop()
                if self.current_create_obstacle_preview_line != None:
                    self.canvas.delete(self.current_create_obstacle_preview_line)
                    self.current_create_obstacle_preview_line = None

            def recommencer():
                self.create_obstacle_termine = False
                for i in self.current_create_obstacle_point_obj:
                    self.canvas.delete(i)
                for i in self.current_create_obstacle_ligne_obj:
                    self.canvas.delete(i)
                self.current_create_obstacle_point_obj = []
                self.current_create_obstacle_ligne_obj = []
                self.current_create_obstacle = []
                if self.current_create_obstacle_preview_line != None:
                    self.canvas.delete(self.current_create_obstacle_preview_line)
                    self.current_create_obstacle_preview_line = None
            def stop():
                recommencer()
                self.l_obstacle_create.destroy()
                self.l_obstacle_create = None

                self.cursor_mode = "selection"
                self.canvas.config(cursor="arrow")


            def valider():
                if len(self.current_create_obstacle)>2:
                    

                    obs = self.current_create_obstacle
                    def centre(ob):
                        x = 0
                        y = 0
                        for i in ob:
                            x += i[0]
                            y += i[1]
                        return (x/len(obs),y/len(obs))
                    c = centre(obs)
                    self.canvas.config(cursor="arrow")
                    taille_fenetre = (self.taille_canvas[0]/self.zoom,self.taille_canvas[1]/self.zoom)
                    etage = int(c[0]/(self.taille_max[0]*self.zoom) ) + int(c[1]/(self.taille_max[1]*self.zoom))*int(taille_fenetre[0]/self.taille_max[0])
                    if etage >= self.nb_etage:
                        return
                    obs = MultListe(obs, 1/self.zoom)
                    fin = []
                    for point in obs:
                        fin.append((point[0]%self.taille_max[0],point[1]%self.taille_max[1]))
                    #plus_liste(((e.x/10)%self.taille_max[0],(e.y/10)%self.taille_max[1]),obs)
            
                    recommencer()
                    self.cursor_mode = "selection"
                    self.liste_obstacle[etage].append(fin)
                    #self.liste_obstacle.append(self.current_create_obstacle)
                    self.l_obstacle_create.destroy()
                    self.l_obstacle_create = None

                    self.create_obstacle_termine = False
                    self.refresh_obstacle()


                # else:
                #     messagebox.showerror("Erreur", "Vous devez créer un obstacle avec au moins 3 points")

            self.cursor_mode = "create_obstacle"
            self.canvas.config(cursor="cross")
            #creer une nouvelle labelframe dans la fenetre principale dans f_menue qui contient 3 boutons : annuler le dernier point, recommencer, stop
            self.l_obstacle_create = LabelFrame(self.f_menue, text="Création obstacle", padx=20, pady=20, bg="#F5F5F5")
            self.l_obstacle_create.pack(fill="both",side=TOP)
            self.b_obstacle_create_annuler = Button(self.l_obstacle_create, text="Annuler le dernier point", command=annuler_dernier_point)
            self.b_obstacle_create_annuler.pack()
            self.b_obstacle_create_recommencer = Button(self.l_obstacle_create, text="Recommencer", command=recommencer)
            self.b_obstacle_create_recommencer.pack()
            self.b_obstacle_create_stop = Button(self.l_obstacle_create, text="Stop", command=stop)
            self.b_obstacle_create_stop.pack()
            self.b_obstacle_valider = Button(self.l_obstacle_create, text="Valider", command=valider)
            self.b_obstacle_valider.pack()
            self.fenetre_ajout_obstacle.destroy()

        #obstacle de base dans du 30*30
        self.liste_obstacle_base = [[(1, 1), (29, 1), (29, 29), (1, 29)],[(7, 1), (23, 1), (23, 29), (7, 29)],[(0.5, 19.5), (19.5, 19.5), (19.5, 29.5), (0.5, 29.5)]]
        self.fenetre_ajout_obstacle.geometry("175x" + str( 50 + round((len(self.liste_obstacle_base)/3)*130)))
        #bouton centré pour dessiner un obstacle
        self.b_dessiner_obstacle = Button(self.fenetre_ajout_obstacle, text="Dessiner un obstacle", command= dessiner_obstacle_canvas)
        self.b_dessiner_obstacle.pack(side=BOTTOM, pady=10)

       


        f_canvas = Frame(self.fenetre_ajout_obstacle)
        f_canvas.pack(side=LEFT, padx=10, pady=10)
        #afficher des canvas de chaque obstacle de liste_obstacle_base, les canvas sont cliquable et permettent de choisir l'obstacle à ajouter
        for i in range(0, len(self.liste_obstacle_base), 2):
            # création de la frame pour chaque ligne
            frame_ligne = Frame(f_canvas)
            frame_ligne.pack(side=TOP, padx=5, pady=5)
            
            # création des deux canvas pour chaque ligne
            for j in range(3):
                if i + j < len(self.liste_obstacle_base):
                    canvas_index = i + j
                    canvas = Canvas(frame_ligne, width=30 + 2, height=30 + 2, bg="#F5F5F5")

                    canvas.create_polygon(plus_liste((3, 3), self.liste_obstacle_base[canvas_index]), fill="black", outline="black")
                    canvas.pack(side=LEFT, padx=5)
                    canvas.bind("<Button-1>", lambda e, i=canvas_index: charger_obstacle_base(i))

        def charger_obstacle_base(i):
            def moyenne_liste(liste):
                x = 0
                y = 0
                for point in liste:
                    x += point[0]
                    y += point[1]
                return (x/len(liste),y/len(liste))
            self.cursor_mode = "obstacle_placement"
            #centre = moyenne de la liste de point
            centre = moyenne_liste(self.liste_obstacle_base[i])
            self.obstacle_placement = (self.liste_obstacle_base[i],centre)
            self.taille_placement = 2
            self.fenetre_ajout_obstacle.destroy()

    def ouvrir_fenetre_modification(self):
        self.stop_current_task()
        taille_max = (self.taille_max[0]*10,self.taille_max[1]*10)
        # Création de la fenêtre de modification
        self.fenetre_modif = Toplevel(self.master)
        self.fenetre_modif.title("Modification de la forme")

        self.fenetre_modif.geometry( str(taille_max[0] + 300) + "x" + str(taille_max[1] + 150))
        
        self.modife_liste_points = []
        self.obj_liste_ligne = []
        self.obj_liste_point = []
        self.ligne_actuelle = None
        self.edition_forme_termine = False
        #liste de forme de base :
        self.liste_forme_base = [[(5, 5), (195, 5), (195, 295), (5, 295)],[(5, 5), (195, 5), (195, 195), (5, 195)],[(5, 5), (195, 5), (100, 195)]] #sans decalage de 10 !

        # Création du canvas pour dessiner la forme
        self.canvas_modif = Canvas(self.fenetre_modif, width=taille_max[0] + 10, height= taille_max[1] + 10, bg="#F0F0F0")
        #dessiner une zone de 195x195 au centre du canvas
        self.canvas_modif.create_rectangle(10, 10, taille_max[0], taille_max[1], fill="white",outline="white")
        self.canvas_modif.pack(side=LEFT)
        

        # Création de la frame de modification
        f_modif = Frame(self.fenetre_modif)
        f_modif.pack(side=LEFT, padx=10, pady=10)

        def recommencer_forme():
            self.edition_forme_termine = False

            for obj in self.obj_liste_point + self.obj_liste_ligne:
                self.canvas_modif.delete(obj)

            if self.ligne_actuelle is not None:
                self.canvas_modif.delete(self.ligne_actuelle)

            self.ligne_actuelle = None
            self.modife_liste_points = [] #avec un decalage de 10 !
            self.obj_liste_point = []
            self.obj_liste_ligne = []

        def annuler_dernier_point():

            if self.edition_forme_termine:

                self.edition_forme_termine = False
                if len(self.modife_liste_points) > 0:
                    if len(self.obj_liste_ligne) > 0:
                        self.canvas_modif.delete(self.obj_liste_ligne[-1])
                        self.obj_liste_ligne.pop()

                    if self.ligne_actuelle is not None:
                        self.canvas_modif.delete(self.ligne_actuelle)
                        self.ligne_actuelle = None

                return

            self.edition_forme_termine = False

            if len(self.modife_liste_points) > 0:
                self.canvas_modif.delete(self.obj_liste_point[-1])
                self.obj_liste_point.pop()
                if len(self.obj_liste_ligne) > 0:
                    self.canvas_modif.delete(self.obj_liste_ligne[-1])
                    self.obj_liste_ligne.pop()

                if self.ligne_actuelle is not None:
                    self.canvas_modif.delete(self.ligne_actuelle)
                    self.ligne_actuelle = None
                self.modife_liste_points.pop()

        def valider_forme ():
            if not self.edition_forme_termine:
                return
            #fermer la fenêtre de modification
            self.fenetre_modif.destroy()
            self.forme_etage = MultListe(plus_liste((-5,-5), self.modife_liste_points),1/10)
            self.refresh_etage()
            return 
    
        def ligne_preview(e):
            self.canvas_modif.config(cursor="cross")
            event = (round(e.x/5)*5, round(e.y/5)*5)
            #texte qui affiche les coordonnées de la souris
            #si le texte existe déjà, on le supprime    
            if self.canvas_modif.find_withtag("coord"):
                self.canvas_modif.delete("coord")
            self.canvas_modif.create_text(taille_max[0]/2, 10, text=str((event[0]-5,event[1]-5)), tag="coord")

            if self.edition_forme_termine:
                self.canvas_modif.config(cursor="arrow")

                return

            #arrondir les coordonnées de la souris
            if len(self.modife_liste_points) > 0:
                if self.ligne_actuelle is not None:
                    self.canvas_modif.delete(self.ligne_actuelle)
                self.ligne_actuelle = self.canvas_modif.create_line(self.modife_liste_points[-1], (event[0], event[1]), fill="red")
            #si la souris est en dehors du canvas, on supprime la ligne
            #seulement si la souris est en dehors de la zone de dessin (5, 5, 195, 295)
            if event[0]-5 < 5 or event[0]-5 > taille_max[0] or event[1] -5 < 5 or event[1] > taille_max[1]:
                self.canvas_modif.config(cursor="arrow")
                if self.ligne_actuelle is not None:
                    self.canvas_modif.delete(self.ligne_actuelle)
                    self.ligne_actuelle = None
            
        def ajouter_point(e):
            #redefinir e si c'est un tuple

            if self.edition_forme_termine:
                return
            rayon = 3
            #arrondir les coordonnées de la souris
            event = (0,0)
            if type(e) == tuple:
                 event = (round(e[0]/5)*5 + 5, round(e[1]/5)*5 + 5)

            else:
                event = (round(e.x/5)*5, round(e.y/5)*5)
            
            #si la souris est en dehors de la zone de dessin (5, 5, 195, 295), on ne fait rien
            if event[0]-5 < 5 or event[0]-5 > taille_max[0] or event[1] -5 < 5 or event[1] > taille_max[1]:
                return
            #si le point est déjà dans la liste, on arrete
            if event in self.modife_liste_points:
                self.obj_liste_ligne.append(self.canvas_modif.create_line(event, self.modife_liste_points[-1], fill="red"))
                self.edition_forme_termine = True
                self.canvas_modif.config(cursor="arrow")

                return


            self.obj_liste_point.append(self.canvas_modif.create_oval(event[0] - rayon, event[1] - rayon, event[0] + rayon, event[1] + rayon, fill="red"))
            self.modife_liste_points.append((event[0], event[1]))
            #creer une ligne entre le dernier point et le point actuel
            if len(self.modife_liste_points) > 1:
                self.obj_liste_ligne.append(self.canvas_modif.create_line(self.modife_liste_points[-2], self.modife_liste_points[-1], fill="red"))

        self.canvas_modif.bind("<Button-1>", ajouter_point)
        self.canvas_modif.bind("<Motion>", ligne_preview)

        # Création des boutons
        self.b_recommencer = Button(f_modif, text="Recommencer", command=recommencer_forme)
        self.b_recommencer.pack(pady=5)
        self.b_annuler = Button(f_modif, text="Annuler le dernier point", command=annuler_dernier_point)
        self.b_annuler.pack(pady=5)
        self.b_valider = Button(f_modif, text="Valider", command=valider_forme)
        self.b_valider.pack(pady=5)
        self.canvas_forme_base = []

        def charger_forme_base(i):
            recommencer_forme()
            for point in self.liste_forme_base[i]:

                ajouter_point(point)
            ajouter_point(self.liste_forme_base[i][0])
            self.edition_forme_termine = True

        def charger_forme_courante():
            if self.forme_etage is not []:
                recommencer_forme()
                for point in self.forme_etage:
                    ajouter_point(multScal(10,point))
                ajouter_point(multScal(10,self.forme_etage[0]))
                self.edition_forme_termine = True
           
        charger_forme_courante()



        # petit canvas cliquable contenant les formes de base, si on clique dessus, on charge la forme dans le canvas de modification
        #pour chaque forme de base, on crée un canvas de 100x100 
        #il y a deux canvas par ligne
                
        for i in range(0, len(self.liste_forme_base), 2):
            # création de la frame pour chaque ligne
            frame_ligne = Frame(f_modif)
            frame_ligne.pack(side=TOP, padx=5, pady=5)
            
            # création des deux canvas pour chaque ligne
            for j in range(2):
                if i + j < len(self.liste_forme_base):
                    canvas_index = i + j
                    canvas = Canvas(frame_ligne, width=taille_max[0]/10 + 2, height=taille_max[1]/10 + 2, bg="white")
                    canvas.create_polygon(plus_liste((3, 3), MultListe(self.liste_forme_base[canvas_index], 1 / 10)), fill="white", outline="black")
                    canvas.pack(side=LEFT, padx=5)
                    canvas.bind("<Button-1>", lambda e, i=canvas_index: charger_forme_base(i))
            

root = Tk()
app = FenetrePrincipale(root,taille_max=(20,30))
app.pack()
root.mainloop()
