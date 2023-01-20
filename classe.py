from fonction import*

class batiment_class :
    def __init__(self,nb_etage,taille_max,forme_etage,liste_escalier_descendant,liste_obstacle):
        self.nb_etage = nb_etage
        self.taille_max = taille_max
        self.forme_etage = forme_etage
        self.liste_escalier_descendant = liste_escalier_descendant
        self.liste_obstacle = liste_obstacle

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)

class scene_class :
    def __init__(self,batiment,liste_personne,temps):
        self.batiment = batiment
        self.liste_personne = liste_personne

    @classmethod
    def from_json(cls, data: dict):
        liste_personne = list(map(personne.from_json, data["liste_personne"]))
        return(data['batiment'],liste_personne)


class personne :
    def addDeltaPos(self,newpos,i):
        l = len(self.positions)
        if(l>i):
            self.positions[i] = add(self.positions[i-1],newpos)
        else:
            self.positions.append(add(self.positions[l-1],newpos))
    def __init__(self,largeur,vitesseMax,vitesseActuelle,positions,masse,acceleration,couleur,etage,id):
        self.largeur = largeur
        self.vitesseMax = vitesseMax
        self.vitesseActuelle = vitesseActuelle
        self.acceleration = acceleration
        self.positions = positions
        self.masse = masse
        self.couleur = couleur
        self.etage = etage
        self.id = id


    def basique(self,pos,etage):
        self.largeur = 0.75
        self.vitesseMax = 0.85
        self.vitesseActuelle = (0,0)
        self.positions = [pos]
        self.masse = 70
        self.acceleration = (0,0)
        self.couleur = "blue"
        self.etage = etage
        #self.positions.append((DIMENTIONS[0]/2,DIMENTIONS[1]/2))

    #Pour la deserialisation json
    @classmethod
    def from_json(cls, data: dict):
        #try:
        #    print(data['couleur'])
        #except:
            #return cls(data['largeur'],data['vitesseMax'],data['vitesseActuelle'],data['positions'],data['masse'],data['acceleration'],'')
        return cls(**data)


class fichier_class:
    def __init__(self,nom,scene,mode,temps):
        self.nom = nom
        self.scene = scene
        self.mode = mode
        self.temps = temps
    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


