from tkinter import *
from fonction import*
import math

class FenetrePrincipale(Frame):
    def __init__(self, master=None,forme_etage=[(0.5, 0.5), (19.5, 0.5), (19.5, 29.5), (0.5, 29.5)],temps = 30,nb_etage=1,taille_max = (20,30),liste_escalier_descendant=[[]],liste_obstacle=[[]]):
        super().__init__(master)
        self.master = master
        self.master.title("Ma fenêtre")
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

        self.etage_obj = []
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
        self.create_obstacle_termine = False
        self.f_menue = Frame(self.master, width=200, height=self.taille_canvas[1], bg="#F5F5F5")
        self.f_menue.pack(side=RIGHT, fill=BOTH, expand=True)
        self.l_info = LabelFrame(self.f_menue, text="Informations", padx=20, pady=20, bg="#F5F5F5")
        self.l_info.pack(fill="both",side=TOP)
        
        self.l_debug = LabelFrame(self.f_menue, text="debug", padx=20, pady=20, bg="#F5F5F5")
        self.l_debug.pack(fill="both",side=BOTTOM)
        self.l_debug_text = Label(self.l_debug, text="debug",bg="#F5F5F5")
        self.l_debug_text.pack()
        self.l_debug_text2 = Label(self.l_debug, text="debug",bg="#F5F5F5")
        self.l_debug_text2.pack()

        self.l_nb_personnes = Label(self.l_info, text="nb de personnes",bg="#F5F5F5")
        self.l_nb_personnes.pack()

        
       #creer une checkbutton
        checkbox = Checkbutton(self.l_info, text="Zone securité",bg="#F5F5F5", command=lambda: self.zone_securite("switch"))
        checkbox.pack()

        self.l_coord = Label(self.l_info, text="Coordonnées",bg="#F5F5F5")
        self.l_coord.pack()

        self.refresh_etage()

        def incrementer(var):
            
            if var == "etage":
                self.nb_etage = self.nb_etage+1
                self.liste_escalier_descendant.append([])
                self.liste_obstacle.append([])
                self.liste_obstacle_obj.append([])
                self.liste_escalier_descendant_obj.append([])
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
                    #print(str(self.nb_etage) + "-oo-" + str(len(self.liste_obstacle_obj))) 
                    print(self.liste_obstacle_obj)
                    for obj in self.liste_obstacle_obj[self.nb_etage]:
                        print("sup " + str(obj))
                        self.canvas.delete(obj)
                    self.liste_escalier_descendant_obj.pop()
                    self.liste_obstacle_obj.pop()
                    self.refresh_etage()

            elif var == "temps" and self.temps > 0:
                    self.var_temps.set(self.var_temps.get() - 1)
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



    def refresh_clic_gauche(self,e):
        #tourner l'obstacle actuelle de 45°
        if self.obstacle_placement != None:
            self.obstacle_placement = (tourner_forme(self.obstacle_placement[0],45/2),self.obstacle_placement[1])
            self.refresh_curseur(e)


    def refresh_obstacle(self):
        
        
        for i in range (self.nb_etage):
            taille_max = self.taille_max
            taille_fenetre = (self.taille_canvas[0]/self.zoom,self.taille_canvas[1]/self.zoom)
            zoom = self.zoom
            decalage = ((i*taille_max[0])%taille_fenetre[0],taille_max[1]*math.floor((i*taille_max[0])/taille_fenetre[0]))
            #affiche entree/sortie
            rayon = 0.3
            # for fleche in self.liste_escalier_descendant[i]:
            #     if i!=0 :
            #         #affiche entree etage i-1
            #         decalageBis = (((i-1)*taille_max[0])%taille_fenetre[0],taille_max[1]*math.floor(((i-1)*taille_max[0])/taille_fenetre[0]))
            #         self.canvas.create_oval((fleche[0]-rayon+decalage[0])*zoom,(fleche[1]-rayon+decalage[1])*zoom,(fleche[0]+rayon+decalage[0])*zoom,(fleche[1]+rayon+decalage[1])*zoom,fill ='red')
            #     else :
            #         self.canvas.create_oval((fleche[0]-rayon)*zoom,(fleche[1]-rayon)*zoom,(fleche[0]+rayon)*zoom,(fleche[1]+rayon)*zoom,fill = 'green')
            # #affiche obstacles
            print(self.liste_escalier_descendant_obj[i])
            for obj in self.liste_escalier_descendant_obj[i]:
                self.canvas.delete(obj)
                self.liste_escalier_descendant_obj[i].pop()
            for obj in self.liste_obstacle_obj[i]:
                self.canvas.delete(obj)
                self.liste_obstacle_obj[i].pop()


            for obstacle in self.liste_obstacle[i]:
                    self.liste_obstacle_obj[i].append(self.canvas.create_polygon(MultListe(plus_liste(decalage,obstacle),zoom),fill="black",outline='black'))
                    #self.canvas.create_polygon(MultListe(plus_liste(decalage,agrandir_forme(obstacle,0.75,2)),zoom),fill="",outline='red')
        self.zone_securite("refresh")

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
        self.l_debug_text.config(text="liste obstacle: " + str(self.liste_obstacle_obj))
        self.l_debug_text2.config(text="listeo: " + str(len(self.liste_obstacle)))
        #afficher coordonnées curseur
        self.l_coord.config(text="x: " + str(round(event.x/5)*5) + " y: " + str(round(event.y/5)*5))
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


    def ouvrir_fenetre_ajout_obstacle(self):
        # Création de la fenêtre de modification
        self.fenetre_ajout_obstacle = Toplevel(self.master)
        self.fenetre_ajout_obstacle.title("Ajout d'un obstacle" )
        
        def ouvrir_fenetre_dessin_obstacle():

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
                    print("centre :" + str(c))
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

                    self.refresh_obstacle()
                    self.create_obstacle_termine = False


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
        self.b_dessiner_obstacle = Button(self.fenetre_ajout_obstacle, text="Dessiner un obstacle", command= ouvrir_fenetre_dessin_obstacle)
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
