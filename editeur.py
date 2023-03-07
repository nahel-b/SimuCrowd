from tkinter import *
from fonction import*

class FenetrePrincipale(Frame):
    def __init__(self, master=None,forme_etage=[],nb_etage=0,taille_max = (20,30),liste_escalier_descendant=[],liste_obstacle=[]):
        super().__init__(master)
        self.master = master
        self.master.title("Ma fenêtre")
        self.master.geometry("1200x600")
        self.pack(fill=BOTH, expand=True)

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
            print(decalage)
            self.etage_obj.append( self.canvas.create_polygon(MultListe(plus_liste(decalage,forme_etage),zoom),fill="white",outline='black'))
            #affiche entree/sortie
            rayon = 0.3
            for fleche in liste_escalier_descendant[i]:
                if i!=0 :
                    #affiche entree etage i-1
                    decalageBis = (((i-1)*taille_max[0])%taille_fenetre[0],taille_max[1]*math.floor(((i-1)*taille_max[0])/taille_fenetre[0]))
                    self.canvas.create_oval((fleche[0]-rayon+decalage[0])*zoom,(fleche[1]-rayon+decalage[1])*zoom,(fleche[0]+rayon+decalage[0])*zoom,(fleche[1]+rayon+decalage[1])*zoom,fill ='red')
                else :
                    self.canvas.create_oval((fleche[0]-rayon)*self.zoom,(fleche[1]-rayon)*zoom,(fleche[0]+rayon)*zoom,(fleche[1]+rayon)*zoom,fill = 'green')
            #affiche obstacles
            for obstacle in liste_obstacle[i]:
                    self.canvas.create_polygon(MultListe(plus_liste(decalage,obstacle),zoom),fill="black",outline='black')
                    self.canvas.create_polygon(MultListe(plus_liste(decalage,agrandir_forme(obstacle,0.75,2)),zoom),fill="",outline='red')

    def create_widgets(self):

        
        self.canvas = Canvas(self.master, width=self.taille_canvas[0], height=self.taille_canvas[1], bg="white")
        self.canvas.pack(side=LEFT)
        f_menue = Frame(self.master, width=200, height=self.taille_canvas[1], bg="#F5F5F5")
        f_menue.pack(side=RIGHT)
        self.l_info = LabelFrame(f_menue, text="Informations", padx=20, pady=20, bg="#F5F5F5")
        self.l_info.pack(fill="both")
        
        self.l_nb_personnes = Label(self.l_info, text="nb de personnes")
        self.l_nb_personnes.pack()


        
        
        self.refresh_etage()

        def incrementer(var):
            x = var.get()
            var.set(x + 1)
            if var == self.var_etage:
                self.nb_etage = x+1
                self.liste_escalier_descendant.append([])
                self.liste_obstacle.append([])
                self.refresh_etage()

            elif var == self.var_temps:
                    self.temps = self.var_temps.get()
    
        def decrementer(var):
            x = var.get()
            if x > 0:
                var.set(x - 1)
                if var == self.var_etage:
                    self.nb_etage = x-1
                    self.liste_escalier_descendant.pop()
                    self.liste_obstacle.pop()
                    self.refresh_etage()

                elif var == self.var_temps:
                    self.temps = self.var_temps.get()

        def create_temps_input():
            self.f_temps = Frame(self.l_info, bg="#F5F5F5")
            self.f_temps.pack(side=TOP, fill=X)
            self.l_temps = Label(self.f_temps, text="temps:")
            self.l_temps.pack(side=LEFT)
            self.var_temps = IntVar()
            self.var_temps.set(0)
            self.b_plus_temps = Button(self.f_temps, text="+", width=1, command=lambda: incrementer(self.var_temps))
            self.b_plus_temps.pack(side=LEFT, padx=5)
            self.b_moins_temps = Button(self.f_temps, text="-", width=1, command=lambda: decrementer(self.var_temps))
            self.b_moins_temps.pack(side=LEFT)
            self.input_temps = Entry(self.f_temps, validate="key", width=3, textvariable=self.var_temps)
            self.input_temps.pack(side=LEFT)
        
        create_temps_input()

        def create_nb_etage_input():
            self.var_etage = IntVar()
            self.var_etage.set(self.nb_etage)
            self.f_etage = Frame(self.l_info, bg="#F5F5F5")
            self.f_etage.pack(side=TOP, fill=X)
            self.l_etage = Label(self.f_etage, text="etage:")
            self.l_etage.pack(side=LEFT)
            self.b_plus_temps = Button(self.f_etage, text="+", width=1, command=lambda: incrementer(self.var_etage))
            self.b_plus_temps.pack(side=LEFT, padx=5)
            self.b_moins_temps = Button(self.f_etage, text="-", width=1, command=lambda: decrementer(self.var_etage))
            self.b_moins_temps.pack(side=LEFT)
            self.input_etage = Entry(self.f_etage, validate="key", width=3, textvariable=self.var_etage)
            self.input_etage.pack(side=LEFT)
        
        create_nb_etage_input()
         # Frame parent pour l_edition

        self.l_edition = LabelFrame(f_menue, text="Édition", padx=20, pady=20, bg="#F5F5F5")
        self.l_edition.pack(fill="both")
        
        self.b_modifier_forme_etage = Button(self.l_edition, text="Modifier forme étage", command=self.ouvrir_fenetre_modification)
        self.b_modifier_forme_etage.pack()
        
        self.var_selection = BooleanVar()
        self.var_personne = BooleanVar()
        
    

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
            #fermer la fenêtre de modification
            self.fenetre_modif.destroy()
            self.forme_etage = MultListe(plus_liste((-5,-5), self.modife_liste_points),1/10)
            self.refresh_etage()
            return 
    
        def ligne_preview(e):
            
            event = (round(e.x/5)*5, round(e.y/5)*5)
            #texte qui affiche les coordonnées de la souris
            #si le texte existe déjà, on le supprime    
            if self.canvas_modif.find_withtag("coord"):
                self.canvas_modif.delete("coord")
            self.canvas_modif.create_text(taille_max[0]/2, 10, text=str((event[0]-5,event[1]-5)), tag="coord")

            if self.edition_forme_termine:
                return

            #arrondir les coordonnées de la souris
            if len(self.modife_liste_points) > 0:
                if self.ligne_actuelle is not None:
                    self.canvas_modif.delete(self.ligne_actuelle)
                self.ligne_actuelle = self.canvas_modif.create_line(self.modife_liste_points[-1], (event[0], event[1]), fill="red")
            #si la souris est en dehors du canvas, on supprime la ligne
            #seulement si la souris est en dehors de la zone de dessin (5, 5, 195, 295)
            if event[0]-5 < 5 or event[0]-5 > taille_max[0] or event[1] -5 < 5 or event[1] > taille_max[1]:
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
                print((event, self.modife_liste_points[0]))
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
            print("chargement de la forme", i)
            recommencer_forme()
            for point in self.liste_forme_base[i]:

                ajouter_point(point)
            ajouter_point(self.liste_forme_base[i][0])
            self.edition_forme_termine = True



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
