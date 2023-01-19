from fonction import*

def initialisation_variable(liste_escalier_descendant1,liste_obstacle1,forme_etage1,nb_etage1,taille_max1,taille_fenetre1):
    global liste_escalier_descendant
    global liste_obstacle
    global forme_etage
    global nb_etage
    global taille_max
    global taille_fenetre
    liste_escalier_descendant = liste_escalier_descendant1
    liste_obstacle = liste_obstacle1
    forme_etage = forme_etage1
    nb_etage = nb_etage1
    taille_max = taille_max1
    taille_fenetre = taille_fenetre1
    init_point_etage()
    init_sortie_plus_rapide()

#renvoie la liste dist_point_sortie, qui contient pour chaque point de l'étage,
#la distance la plus courte entre ce point et la sortie spécifiée 
def get_point_dist(etage_num,num_sortie):
    sortie = liste_escalier_descendant[etage_num][num_sortie]
    dist_point_sortie = []
    liste_pol = liste_obstacle[etage_num]
    pol_point = deconsrtuit(liste_obstacle[etage_num])
    for i in range (len(pol_point)):
        dist_point_sortie.append((-1,(0,0))) #(distance,point)
    
    for point in pol_point :
        if not seg_polintersect(point[0],point[1],sortie[0],sortie[1],liste_pol):
            dist_point_sortie[pol_point.index(point)] = (dist(sortie,point),sortie)
        
    for l in dist_point_sortie :
        if l[0]!= -1:
            p = pol_point[dist_point_sortie.index(l)]
    finie = False
    i =0
    while (not finie):
        i=i+1
        if (i>1000) :
            print("stopppp")
            for point in pol_point :
                if dist_point_sortie[pol_point.index(point)][0] == -1:
                    print(point)
            break
            
        finie = True
        for point in pol_point :
            if dist_point_sortie[pol_point.index(point)][0] == -1:
                #print("lui->" + str(point))
                finie = False
            for p2 in pol_point:
                
                #verifier un a un les condition de la boucle de haut dessus pour (37,113) et (37,161)
                
                #if((point[0],point[1],p2[0],p2[1]) == (37,113,37,161) ):
                #    print("--r>" + str(seg_int(point[0],point[1],p2[0],p2[1],liste_pol)))
                #not seg_int(point[0],point[1],p2[0],p2[1],liste_pol) and
                if (not intersect_mur(point[0],point[1],p2[0],p2[1],forme_etage)) and (not seg_int(point[0],point[1],p2[0],p2[1],liste_pol)) and dist_point_sortie[pol_point.index(p2)][0] != -1 and (point[0]!=p2[0] or point[1]!=p2[1] )and (not seg_polintersect(point[0],point[1],p2[0],p2[1],liste_pol) and (dist_point_sortie[pol_point.index(point)][0] > dist(point,p2)+dist_point_sortie[pol_point.index(p2)][0] or dist_point_sortie[pol_point.index(point)][0] == -1)):
                
                    dist_point_sortie[pol_point.index(point)] = (dist(point,p2)+dist_point_sortie[pol_point.index(p2)][0],p2)
                    finie = False
    i = etage_num
    return dist_point_sortie

#pour chaque sortie, pour chaque etage la liste de la distance entre chacun des points de l'etage et de la sortie

def init_point_etage():
    global point_sortie_etages
    point_sortie_etages = []
    for etage_num in range (nb_etage):
        a=[]
        for sortie in range(len(liste_escalier_descendant[etage_num])):
            a.append(get_point_dist(etage_num,sortie))
        point_sortie_etages.append(a)

#calcul pour un point (pos_entre) le prochain point et la distance du chemine le plus court
#entre ce point et la sortie specifiée
def premier_point(etage_num,num_sortie,pos_entre):
    sortie = liste_escalier_descendant[etage_num][num_sortie]
    res = (100000,(0,0))
    liste_pol = liste_obstacle[etage_num]
    pol_point = deconsrtuit(liste_obstacle[etage_num])
    dist_point_sortie = point_sortie_etages[etage_num][num_sortie]
    for point in pol_point :
        #print(dist_point_sortie)
        if dist_point_sortie[pol_point.index(point)][0] != -1:
            if (not seg_polintersect(point[0],point[1],pos_entre[0],pos_entre[1],liste_pol)):
                if res[0] > dist(point,pos_entre)+dist_point_sortie[pol_point.index(point)][0]:
                    res = (dist(point,pos_entre)+dist_point_sortie[pol_point.index(point)][0],point)
    if (not seg_polintersect(sortie[0],sortie[1],pos_entre[0],pos_entre[1],liste_pol)) and res[0] > dist(sortie,pos_entre):
        res = (dist(sortie,pos_entre),sortie)
    return res

#renvoie une liste des escalier descendant associé a leurs distance la plus courte
#jusqu'a la sortie tout en bas et la prochaine sortie ou aller
#sortie_plus_rapide_res[i][j] : dist + prochaine escalier a prendre pour
#la sortie (esc descendant) j de l'etage i
def init_sortie_plus_rapide():
    global sortie_plus_rapide
    sortie_plus_rapide = [[(0,0),(0,0),(0,0),(0,0)]]
    for etage_num in range (1,nb_etage):
        a=[]
        for entree in range(len(liste_escalier_descendant[etage_num])):
            a.append((premier_point(etage_num-1,0,liste_escalier_descendant[etage_num][entree])[0]  + sortie_plus_rapide[etage_num-1][0][0] ,entree))#+sorti+rap 0 ??
            for sortie in range(len(liste_escalier_descendant[etage_num-1])):
                if premier_point(etage_num-1,sortie,liste_escalier_descendant[etage_num][entree])[0] + sortie_plus_rapide[etage_num-1][sortie][0] < a[entree][0]:
                    a[entree] = (premier_point(etage_num-1,sortie,liste_escalier_descendant[etage_num][entree])[0] + sortie_plus_rapide[etage_num-1][sortie][0],sortie )
        sortie_plus_rapide.append(a)


#prochaine sortie a prendre pour le chemin plus rapide
def get_plus_rapide_prochain_sortie(etage,position):
    res_sortie = 0
    for i in range(len(liste_escalier_descendant[etage])) :
        if (premier_point(etage,i,position)[0] + sortie_plus_rapide[etage][i][0] < premier_point(etage,res_sortie,position)[0] + sortie_plus_rapide[etage][res_sortie][0]):
            res_sortie = i
    return res_sortie

#renvoie la prochaine position ou aller en prenant en compte le decalage
def get_direction(pos_reel):
    etage_n = int(pos_reel[0]/taille_max[0] ) + int(pos_reel[1]/taille_max[1])*int(taille_fenetre[0]/taille_max[0])
    i = etage_n
    pos_abs = (pos_reel[0]%taille_max[0],pos_reel[1]%taille_max[1])
    decalage = ((i*taille_max[0])%taille_fenetre[0],taille_max[1]*math.floor((i*taille_max[0])/taille_fenetre[0]))
    res_sortie = get_plus_rapide_prochain_sortie(etage_n,pos_abs)
    p = premier_point(etage_n,res_sortie,pos_abs)[1]
    d = dist(pos_reel,p)
    return ((p[0]-pos_reel[0])/d,(p[1]-pos_reel[1])/d)