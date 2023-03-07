from tkinter import *
from fonction import*

class FenetrePrincipale(Frame):
    def __init__(self, master=None,forme_etage=[]):
        super().__init__(master)
        self.master = master
        self.master.title("Ma fenêtre")
        self.master.geometry("1200x600")
        self.pack(fill=BOTH, expand=True)

        self.forme_etage = forme_etage
        self.nb_etage

        self.create_widgets()

    def create_widgets(self):

        self.canvas = Canvas(self.master, width=1000, height=600, bg="white")
        self.canvas.pack(side=LEFT)
        f_menue = Frame(self.master, width=200, height=1000, bg="#F5F5F5")
        f_menue.pack(side=RIGHT)
        self.l_info = LabelFrame(f_menue, text="Informations", padx=20, pady=20, bg="#F5F5F5")
        self.l_info.pack(fill="both")
        
        self.l_nb_personnes = Label(self.l_info, text="nb de personnes")
        self.l_nb_personnes.pack()
        
        self.f_temps = Frame(self.l_info, bg="#F5F5F5")
        self.f_temps.pack(side=TOP, fill=X)
        
        self.l_temps = Label(self.f_temps, text="temps:")
        self.l_temps.pack(side=LEFT)
        
        self.b_plus = Button(self.f_temps, text="+", width=1, command=self.incrementer_temps)
        self.b_plus.pack(side=LEFT, padx=5)
        
        self.b_moins = Button(self.f_temps, text="-", width=1, command=self.decrementer_temps)
        self.b_moins.pack(side=LEFT)
        
        self.var_temps = IntVar()
        self.var_temps.set(0)
        self.input_temps = Entry(self.f_temps, validate="key", width=3, textvariable=self.var_temps)
        self.input_temps.pack(side=LEFT)
        
         # Frame parent pour l_edition

        self.l_edition = LabelFrame(f_menue, text="Édition", padx=20, pady=20, bg="#F5F5F5")
        self.l_edition.pack(fill="both")
        
        self.b_modifier_forme_etage = Button(self.l_edition, text="Modifier forme étage", command=self.ouvrir_fenetre_modification)
        self.b_modifier_forme_etage.pack()
        
        self.var_selection = BooleanVar()
        self.var_personne = BooleanVar()
        
    def incrementer_temps(self):
        temps_actuel = self.var_temps.get()
        self.var_temps.set(temps_actuel + 1)
    
    def decrementer_temps(self):
        temps_actuel = self.var_temps.get()
        if temps_actuel > 0:
            self.var_temps.set(temps_actuel - 1)

    def ouvrir_fenetre_modification(self):
        # Création de la fenêtre de modification
        self.fenetre_modif = Toplevel(self.master)
        self.fenetre_modif.title("Modification de la forme")
        self.fenetre_modif.geometry("450x450")
        
        self.modife_liste_points = []
        self.obj_liste_ligne = []
        self.obj_liste_point = []
        self.ligne_actuelle = None
        self.edition_forme_termine = False
        #liste de forme de base :
        self.liste_forme_base = [[(0, 0), (200, 0), (200, 300), (0, 300)],[(0, 0), (200, 0), (200, 200), (0, 200)],[(0, 0), (200, 0), (100, 200)]] #sans decalage de 10 !

        # Création du canvas pour dessiner la forme
        self.canvas_modif = Canvas(self.fenetre_modif, width=220, height=320, bg="#F0F0F0")
        #dessiner une zone de 200x300 au centre du canvas
        self.canvas_modif.create_rectangle(10, 10, 210, 310, fill="white",outline="white")
        self.canvas_modif.pack(side=LEFT, padx=10, pady=10)
        

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

            return self.modife_liste_points
    
        def ligne_preview(e):
            
            event = (round(e.x/10)*10, round(e.y/10)*10)
            #texte qui affiche les coordonnées de la souris
            #si le texte existe déjà, on le supprime    
            if self.canvas_modif.find_withtag("coord"):
                self.canvas_modif.delete("coord")
            self.canvas_modif.create_text(100, 10, text=str((event[0]-10,event[1]-10)), tag="coord")

            if self.edition_forme_termine:
                return

            #arrondir les coordonnées de la souris
            if len(self.modife_liste_points) > 0:
                if self.ligne_actuelle is not None:
                    self.canvas_modif.delete(self.ligne_actuelle)
                self.ligne_actuelle = self.canvas_modif.create_line(self.modife_liste_points[-1], (event[0], event[1]), fill="red")
            #si la souris est en dehors du canvas, on supprime la ligne
            #seulement si la souris est en dehors de la zone de dessin (50, 10, 250, 310)
            if event[0] < 10 or event[0] > 210 or event[1] < 10 or event[1] > 310:
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
                 event = (round(e[0]/10)*10 + 10, round(e[1]/10)*10 + 10)

            else:
                event = (round(e.x/10)*10, round(e.y/10)*10)
            
            #si la souris est en dehors de la zone de dessin (10, 10, 210, 310), on ne fait rien
            if event[0] < 10 or event[0] > 210 or event[1] < 10 or event[1] > 310:
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
                    canvas = Canvas(frame_ligne, width=22, height=32, bg="white")
                    canvas.create_polygon(plus_liste((3, 3), MultListe(self.liste_forme_base[canvas_index], 1 / 10)), fill="white", outline="black")
                    canvas.pack(side=LEFT, padx=5)
                    canvas.bind("<Button-1>", lambda e, i=canvas_index: charger_forme_base(i))
            

root = Tk()
app = FenetrePrincipale(root)
app.pack()
root.mainloop()
