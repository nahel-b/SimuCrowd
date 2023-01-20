from fonction import*
from classe import*
import time 
import chemin

def calcul_basique(scene,debut,nb_seconde,nom):
    personne_etage = [[]]*scene.batiment.nb_etage
    for p in scene.liste_personne:
        personne_etage[p.etage].append(p.id)


    start = time.time()
    for i in range (round(debut),round(nb_seconde*60)+1): # rafraississement : 1/60 de seconde pour 3 x 1 min (60*60*3)
        dt = 1/60
        T = 2 #s
        A = 2*10**3 #N
        B = 0.08 #m
        k = 1.2*10**5 #kg/s^2
        k_ = 2.4 * 10**5 #kg.m^-1.s^-1
        index=0
    
        if i % 25 == 0:
            print(i)
            #deltaTime = (time.time()-start)/(i-debut)
            #region
            #avancement1.config(text= str(round((i-deb)*100/(dataFichier.temps-deb))) + "%")
            #avancement2.config(text ="environ : " + str(round(deltaTime*(dataFichier.temps - i))) + "secondes")
            #indaff = 0
            # for p in md.liste_personne:
            #     CanvasExp.coords(affichage_personne[indaff],
            #     (p.positions[i-1][0]-(p.largeur/2))*zoom, 
            #     (p.positions[i-1][1]-(p.largeur/2))*zoom, 
            #     (p.positions[i-1][0]+(p.largeur/2))*zoom,
            #     (p.positions[i-1][1]+(p.largeur/2))*zoom)
            #     indaff = indaff+1
            # fenetre.update()
            #endregion
        for p in scene.liste_personne:
            p.vitesseActuelle = add(p.vitesseActuelle,multScal(dt,p.acceleration))
            #print("---" + str(p.positions[i-1])+ "---" + str(p.positions))
            dir = chemin.get_direction_plus_rapide(p.positions[i-1],p.etage)
            
              
            directionVoulue = multScal(1/T,sub(multScal(p.vitesseMax,dir),p.vitesseActuelle))
            ForceMur = (0,0)
            ForcePersonnes = (0,0)
            ForcePilier = (0,0)
            
            forme_e = scene.batiment.forme_etage
            for j in range(len(forme_e)):
                #print(mur.PosA)
                ForceMur = add(ForceMur,multScal((1/p.masse)*A*math.exp(((p.largeur/2)-distMurPoint(forme_e[j],forme_e[(j+1)%len(forme_e)],p.positions[i-1]))/B), ortho(forme_e[j],forme_e[(j+1)%len(forme_e)],p.positions[i-1]) ))             
                # ForceMur +=  (1/p)*(Ai*exp(ri-diw)/Bi)*niw
            

            for ps in scene.liste_personne:
                if ps != p and ps.etage == p.etage:
                    n = multScal(dist(ps.positions[i-1],p.positions[i-1]),sub(p.positions[i-1],ps.positions[i-1]))#(ri − rj )/dij
                    ForcePersonnes = add(ForcePersonnes,multScal( A*math.exp(((p.largeur/2)-dist(ps.positions[i-1],p.positions[i-1]))/B),n))
            p.acceleration =  add( directionVoulue, add( ForceMur, add(ForcePersonnes,ForcePilier) ))
            p.addDeltaPos(multScal(dt,p.vitesseActuelle),i)
            
        
            index=index+1

        res = fichier_class(nom,scene,"simu",nb_seconde)
        save(nom,res)