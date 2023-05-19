from fonction import*
from classe import*
import time 
import chemin


def get_etage(id):
    #print (sc.liste_personne) en json stringify
   
    return sc.liste_personne[id].liste_etage[-1][1]
    liste_etage = scene.liste_personne[id].liste_etage
    res = liste_etage[0][1]
    for i in range(len(liste_etage)):
        if(len(liste_etage) == i+1):
            return liste_etage[i][0]
        if(liste_etage[i+1][0] > temps):
            return liste_etage[i][0]


def calcul_basique(scene,debut,temps,nom):
    global sc 
    sc = scene
    personne_etage = []
    for i in range(scene.batiment.nb_etage):
        personne_etage.append([])
    for p in scene.liste_personne:
        personne_etage[p.liste_etage[0][1]].append(p.id)

    start = time.time()
    for i in range (round(debut),round(temps)+1): # rafraississement : 1/60 de seconde pour 3 x 1 min (60*60*3)
        dt = 1/60
        T = 0.5 #s
        A = 2*(10**3) #N
        B = 0.08 #m
        k = 1.2*10**5 #kg/s^2
        k_ = 2.4 * 10**5 #kg.m^-1.s^-1
        index=0
    
        if i % 100 == 0:
            print(str(round((i/round(temps))*100)) + "% (calcul)", end='\r')
        for p in scene.liste_personne:

            if get_etage(p.id) == -1:
                p.addDeltaPos((0,0),i)
            else :
                p.vitesseActuelle = add(p.vitesseActuelle,multScal(dt,p.acceleration))
                dir = chemin.get_direction_plus_rapide(p.positions[i-1],get_etage(p.id),p.largeur)
                directionVoulue = multScal(1/T,sub(multScal(p.vitesseMax,dir),p.vitesseActuelle))
                ForceMur = (0,0)
                ForcePersonnes = (0,0)
                ForcePilier = (0,0)
                etage_personne = get_etage(p.id)

                #collisions avec les murs
                forme_e = scene.batiment.forme_etage
                for j in range(len(forme_e)):
                    #print(mur.PosA)
                    fj = forme_e[j]
                    fj2 = forme_e[(j+1)%len(forme_e)]
                    ForceMur = add(ForceMur,multScal((1/p.masse)*A*math.exp(((p.largeur/2)-distMurPoint(fj,fj2,p.positions[i-1]))/B), ortho(fj,fj2,p.positions[i-1]) ))             
                    # ForceMur +=  (1/p)*(Ai*exp(ri-diw)/Bi)*niw
                 
            
                for j in range(len(scene.batiment.liste_obstacle[etage_personne])):
                    obstacle = scene.batiment.liste_obstacle[etage_personne][j]
                    for k in range(len(obstacle)):
                        #print(mur.PosA)
                        fj = obstacle[k]#point a
                        fj2 = obstacle[(k+1)%len(obstacle)] #point b
                        ForceMur = add(ForceMur,multScal((1/p.masse)*A*math.exp(((p.largeur/2)-distMurPoint(fj,fj2,p.positions[i-1]))/B), ortho(fj,fj2,p.positions[i-1]) ))             
                        # ForceMur +=  (1/p)*(Ai*exp(ri-diw)/Bi)*niw
                
               
                

                for ps in scene.liste_personne:
                    if ps != p and get_etage(ps.id) == get_etage(p.id):
                        n = multScal(dist(ps.positions[i-1],p.positions[i-1]),sub(p.positions[i-1],ps.positions[i-1]))#(ri − rj )/dij
                        ForcePersonnes = add(ForcePersonnes,multScal( A*math.exp(((p.largeur/2)-dist(ps.positions[i-1],p.positions[i-1]))/B),n))
                p.acceleration =  add( directionVoulue, add( ForceMur, add(ForcePersonnes,ForcePilier) ))

                p.addDeltaPos(multScal(dt,p.vitesseActuelle),i)

                #descendre si proche d'une sortie 
                for descente in scene.batiment.liste_escalier_descendant[etage_personne] :
                    #print(dist(p.positions[i],descente) < p.largeur*2)
                    if(dist(p.positions[i],descente) < p.largeur):
                        if etage_personne == 0:
                            personne_etage[etage_personne].remove(p.id)
                            personne_etage[etage_personne-1].append(p.id)
                            p.liste_etage.append((i,etage_personne-1))

                        else :
                            trigger = False
                            for id2 in personne_etage[etage_personne-1]:
                                if (dist(p.positions[i],scene.liste_personne[id2].positions[i-1]) < 1.5*max(p.largeur,scene.liste_personne[id2].largeur) and p.id != id2):
                                    trigger = True
                                    #print((dist(p.positions[i],scene.liste_personne[id2].positions[i-1]),id2))
                            if not trigger:
                                personne_etage[etage_personne].remove(p.id)
                                personne_etage[etage_personne-1].append(p.id)
                                p.liste_etage.append((i,etage_personne-1))


                

                




        
            index=index+1

        res = fichier_class(nom,scene,"simu",temps)
    return res