class scene :

    def __init__(self,liste_mur,liste_personne):
        self.liste_mur = liste_mur
        self.liste_personne = liste_personne
    def from_json(cls, data: dict):
        liste_personne = list(map(personne.from_json, data["liste_personne"]))
        liste_mur = list(map(mur.from_json, data["liste_mur"]))

class personne :
    def addDeltaPos(self,newpos,i):
        l = len(self.positions)
        if(l>i):
            self.positions[i] = add(self.positions[i-1],newpos)
        else:
            self.positions.append(add(self.positions[l-1],newpos))
    def __init__(self,largeur,vitesseMax,vitesseActuelle,positions,masse,acceleration,couleur):
        self.largeur = largeur
        self.vitesseMax = vitesseMax
        self.vitesseActuelle = vitesseActuelle
        self.acceleration = acceleration
        self.positions = positions
        self.masse = masse
        self.couleur = couleur


    def basique(self,pos):
        self.largeur = 0.75
        self.vitesseMax = 0.85
        self.vitesseActuelle = (0,0)
        self.positions = [pos]
        self.masse = 70
        self.acceleration = (0,0)
        #self.positions.append((DIMENTIONS[0]/2,DIMENTIONS[1]/2))

    #Pour la deserialisation json
    @classmethod
    def from_json(cls, data: dict):
        #try:
        #    print(data['couleur'])
        #except:
            #return cls(data['largeur'],data['vitesseMax'],data['vitesseActuelle'],data['positions'],data['masse'],data['acceleration'],'')
        return cls(**data)

class mur:

    def __init__(self,PosA,PosB):
        self.PosA = PosA
        self.PosB = PosB

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)
class pilier:
    def __init__(self,position,largeur):
            self.position = position
            self.largeur = largeur

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)
class monde :

    def init(self,nb,f):

        for i in range (nb) :
            a = personne(0.75,0.85,(0,0),[(500,300)],70,(0,0))
            self.liste_personne.append(a)


    def __init__(self,liste_personne,liste_mur,liste_zone,liste_pilier):
        self.liste_personne = liste_personne
        self.liste_mur = liste_mur
        self.liste_zone = liste_zone
        self.liste_pilier = liste_pilier

    #Pour la deserialisation json
    @classmethod
    def from_json(cls, data: dict):
        liste_personne = list(map(personne.from_json, data["liste_personne"]))
        liste_mur = list(map(mur.from_json, data["liste_mur"]))
        liste_zone = list(map(zone.from_json, data["liste_zone"]))
        try :
            liste_pilier = list(map(pilier.from_json, data["liste_pilier"]))
            return cls(liste_personne,liste_mur,liste_zone,liste_pilier)
        except:
            return cls(liste_personne,liste_mur,liste_zone,[])


class zone :

    def __init__(self,arrivee,points,couleur,nom):
        self.arrivee = arrivee
        self.points = points
        self.couleur = couleur
        self.nom = nom

    def contains(self, pos):
        inter = 0

        for i in range (0,len(self.points)):

            if (self.points[i][0]<=pos[0]<=self.points[(i+1)%len(self.points)][0] or self.points[i][0]>=pos[0]>=self.points[(i+1)%len(self.points)][0]) and self.points[i][0] != self.points[(i+1)%len(self.points)] :
                a = (self.points[(i+1)%len(self.points)][1]-self.points[i][1])/(self.points[(i+1)%len(self.points)][0]-self.points[i][0])
                b = self.points[i][1]-a*self.points[i][0] # car PosA appartient a la droite donc veridie l'equation
                y_d = a*pos[0] + b
                if y_d>=pos[1]:
                    inter = inter+1
                #print("inter")
        return (inter%2==1)

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)

class fichier:
    def __init__(self,nom,monde,mode,temps):
        self.nom = nom
        self.monde = monde
        self.mode = mode
        self.temps = temps
    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


