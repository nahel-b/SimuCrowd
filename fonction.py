import math
import numpy as np
import json

def add(a,b):
    return (a[0]+b[0],a[1]+b[1])

def sub(a,b):
    return (a[0]-b[0],a[1]-b[1])

def multScal(s,a):
    return(s*a[0],s*a[1])

def mult(a,b):
    return(a[0]*b[0],a[1]*b[1])

def MultListe(liste,zoom):
        res = []
        for couple in liste:
            res.append((couple[0]*zoom,couple[1]*zoom))
        return res

class encodeur(json.JSONEncoder):
        def default(self, o):
            return o.__dict__
        
def dist(a,b):
    return math.sqrt((b[0]-a[0])**2+(b[1]-a[1])**2) 

def seg_polintersect(x1,y1,x2,y2,liste_pol): #true si intersection
    for pol in liste_pol:
        for i in range (0,len(pol)):
            if (segIntersect(x1,y1,x2,y2,pol[i][0],pol[i][1],pol[(i+1)%len(pol)][0],pol[(i+1)%len(pol)][1])):
                return True
    return False

def segIntersect(x1, y1,x2, y2,x3, y3,x4, y4): #true si intersection
    
    if x1==x3 and y1==y3 and x2==x4 and y2==y4:#meme segment
        return False
    if (max(x1,x2) < min(x3,x4)):
        return False
    elif x1-x2==0 and x3-x4==0 : #deux segment parralleles
        return False  
    elif x1-x2 == 0 and x3-x4!=0:
        a2 = (y3-y4)/(x3-x4)
        b2 = y3-a2*x3 
        return (max(y1,y2)>a2*x1+b2 and min(y1,y2)<a2*x1+b2 and min(x3,x4)<x1 and max(x3,x4)>x1)

    elif x1-x2 != 0 and x3-x4==0: 
        #if faut rajouter la hauteyr avec y et pas x
        a1 = (y1-y2)/(x1-x2)
        b1 = y1-a1*x1 
        return (max(y3,y4)>a1*x3+b1 and min(y3,y4)<a1*x3+b1 and min(x1,x2)<x3 and max(x1,x2)>x3 )

    elif x1-x2 !=0 and x3-x4 !=0:
        # calcul eq des droite passant par les deux segment
        a1 = (y1-y2)/(x1-x2)
        a2 = (y3-y4)/(x3-x4)
        b1 = y1-a1*x1 
        b2 = y3-a2*x3 
        if (a1 == a2):
            return False # segment parralleles
        xa = (b2 - b1) / (a1 - a2) # abscisse du point d'intersection
        return (xa-0.00001>max(min(x1,x2),min(x3,x4)) and xa+0.00001<min( max(x1,x2), max(x3,x4)))
        #xa appartient a l'intersection des abscisses des deux segment

def normal(A,B):
    AB=(B[0]-A[0],B[1]-A[1])
    u=(AB[0]/math.sqrt(AB[0]**2+AB[1]**2),AB[1]/math.sqrt(AB[0]**2+AB[1]**2))
    return u

def plus_liste(point,liste) :
    res = [0]*len(liste)
    for i in range(len(liste)):
        res[i] = (liste[i][0]+point[0],liste[i][1]+point[1])
    return res
#[[a,b],[c,d]] -> [a,b,c,d]
def deconsrtuit(l):
    res = []
    for i in range(len(l)):
        for obj in l[i] :
            res.append(obj)
    return res

def seg_int(x1,y1,xres,yres,liste_pol): #true si segment interieur a un polygone
    for pol in liste_pol:
        if (x1,y1) in pol and (xres,yres) in pol:
            if (abs(pol.index((x1,y1)) - pol.index((xres,yres)))!=1 and not(pol.index((x1,y1)) == 0 and pol.index((xres,yres))==(len(pol)-1)) and not (pol.index((x1,y1)) == (len(pol)-1) and pol.index((xres,yres))==0)):
                if (x1,y1,xres,yres) == (37,113,37,161):
                    return True
    return False

def intersect_mur(x1,y1,x2,y2,liste_mur):
    for i in range (len(liste_mur)):
        if segIntersect(x1,y1,x2,y2,liste_mur[i][0],liste_mur[i][1],liste_mur[(i+1)%len(liste_mur)][0],liste_mur[(i+1)%len(liste_mur)][1]):
            return True
    return False

def normal(PosA,PosB):
    AB=(PosB[0]-PosA[0],PosB[1]-PosA[1])
    return (AB[0]/math.sqrt(AB[0]**2+AB[1]**2),AB[1]/math.sqrt(AB[0]**2+AB[1]**2))# AB/norme(AB)
    
def distMurPoint(posA,posB,p):
    v = np.array([posB[0]-posA[0], posB[1]-posA[1]])
    pos = np.array([p[0] -posA[0],p[1]-posA[1]])
    v_norme = np.sqrt(sum(v**2))
    h = (np.dot(pos, v)/v_norme**2)*v
    if round (dist((0,0),h) + dist(h,v),4) == round(dist((0,0),v),4):
        return dist(p,(h[0]+posA[0],h[1]+posA[1]))
    elif dist(p,posA)>dist(p,posB):
        return dist(posB,p)
    else:
        return dist(posA,p)
    
def MurPoint_point(posA,posB,p):
    v = np.array([posB[0]-posA[0], posB[1]-posA[1]])
    pos = np.array([p[0] -posA[0],p[1]-posA[1]])
    v_norme = np.sqrt(sum(v**2))
    h = (np.dot(pos, v)/v_norme**2)*v
    if round (dist((0,0),h) + dist(h,v),4) == round(dist((0,0),v),4):
        return (h[0]+posA[0],h[1]+posA[1])
    elif dist(p,posA)>dist(p,posB):
        return posB
    else:
        return posA

def ortho(PosA,PosB,p):
    if PosA[0]>PosB[0]:
        temp = PosA
        PosA=PosB
        PosB=temp
    AB=(PosB[0]-PosA[0],PosB[1]-PosA[1])
    u=(AB[0]/math.sqrt(AB[0]**2+AB[1]**2),AB[1]/math.sqrt(AB[0]**2+AB[1]**2))# AB/norme(AB)
    angle = math.asin(u[1])
    if PosB[0]!=PosA[0]:
        a = (PosB[1]-PosA[1])/(PosB[0]-PosA[0]) # coefficient directeur : y = ax + b
        b = PosA[1]-a*PosA[0] # car PosA appartient a la droite donc veridie l'equation
        y_d = a*p[0] + b # ordonnée du point d'abscisse yp sur la droite ab
        rayon = 2
        add = 0
        if y_d < p[1]: # p au dessus de la droite
            add = +(math.pi/2)
        else:
            add = -(math.pi/2) # p en dessous de la droite
        return (math.cos( angle + add ), math.sin(angle + add ))
    else:
        if p[0]>PosB[0]:
            return (1,0)
        else:
            return (-1,0)

def save(nom,data):
    encode = (encodeur().encode(data))
    with open(nom + ".json", 'w') as f:
        json.dump(json.loads(encode),f, indent=4, sort_keys=True)

def saveComplet(nom,data):
    encode = (encodeur().encode(data))
    with open(nom, 'w') as f:
        json.dump(json.loads(encode),f, indent=4, sort_keys=True)


def calcul_angle(a,b):#angle entre le vecteur a et le vecteur b 
    dot_prod = a[0]*b[0] + a[1]*b[1]
    norm_prod = math.sqrt(a[0]**2 + a[1]**2) * math.sqrt(b[0]**2 + b[1]**2)
    return math.acos(dot_prod/norm_prod)

def vec_entre(v1, v2, k):
    angle = calcul_angle(v1,v2)
    angle_entre_vecteurs = angle / (k+1)
    
    res = []
    for i in range(1, k+1):#calcul des k vecteurs unitaires
        x = v1[0]*math.cos(i*angle_entre_vecteurs) + v1[1]*math.sin(i*angle_entre_vecteurs)
        y = -v1[0]*math.sin(i*angle_entre_vecteurs) + v1[1]*math.cos(i*angle_entre_vecteurs)
        res.append((x,y))
    return res

def est_convexe(forme, i):#true si langle au point d'index i de la forme est inferieur à 180 degré, pi/2
    p1 = forme[i-1]
    p2 = forme[i]
    p3 = forme[(i+1) % len(forme)]
    v1 = (p2[0] - p1[0], p2[1] - p1[1])
    v2 = (p3[0] - p2[0], p3[1] - p2[1])
    produit = v1[0]*v2[1] - v1[1]*v2[0]
    return produit > 0

def agrandir_forme(f, distance,k): #k : le nb de point a ajouter pour les coin concaves
    nouvelle_forme = []
    forme = f[::-1] #cette fonction marche pour les forme donnée dans le sens horaire
    for i in range(len(forme)):# on traite le segment i,i-1 pour le translater en direction du vecteur normal 
        point_actuel = forme[i]
        point_precedent = forme[i-1]
        dx = point_actuel[0] - point_precedent[0]
        dy = point_actuel[1] - point_precedent[1]
        distance_segment = math.sqrt(dx**2 + dy**2)
        if distance_segment == 0:
            nouvelle_forme.append(point_actuel)
            continue
        nx = -dy / distance_segment #vecteur normal a ce segment (x)
        ny = dx / distance_segment # (y)
        nouveau_point1 = (point_precedent[0] + nx * distance, point_precedent[1] + ny * distance) #les deux points translatés
        nouveau_point2 = (point_actuel[0] + nx * distance, point_actuel[1] + ny * distance)
        
        if not est_convexe(forme, i-1):
            nouvelle_forme.append(nouveau_point1)#ne rien ajouter si l'angle non traité est aigue : la prochaine itération s'en occupera

        if est_convexe(forme, i):
             # Ajout d'un coin seulement si l'angle est aigu, pique vers l'interieur
            point_suivant = forme[(i+1) % len(forme)]
            dx_next = point_suivant[0] - point_actuel[0]
            dy_next = point_suivant[1] - point_actuel[1]
            distance_segment_suivant = math.sqrt(dx_next**2 + dy_next**2)
            if distance_segment_suivant == 0:
                continue
            nx_next = -dy_next / distance_segment_suivant #vecteurs nomal du deuxieme segment (pour traiter l'angle apres)
            ny_next = dx_next / distance_segment_suivant
            angle = math.atan2(ny + ny_next, nx + nx_next) # angle entre (nx,ny) et (nx_next,ny_next)
            nx_coin = math.cos(angle) #transforme l'angle en vecteur unitaire
            ny_coin = math.sin(angle)
            distance_convexe = math.sqrt(distance**2 + distance**2)#distance pour respecter la distance de sécurité au niveau des segments a coté de l'angle aigue
            coin_convexe = (point_actuel[0] + nx_coin * distance_convexe, point_actuel[1] + ny_coin * distance_convexe)
            nouvelle_forme.append(coin_convexe)

        else:

            nouvelle_forme.append(nouveau_point2)#on ajoute le point associé a l'extrémité du segment

            # Ajout des coins pour approximer un arrondis
            point_suivant = forme[(i+1) % len(forme)]
            dx_next = point_suivant[0] - point_actuel[0]# deuxieme segment (pour traiter l'angle apres)
            dy_next = point_suivant[1] - point_actuel[1]
            distance_segment_suivant = math.sqrt(dx_next**2 + dy_next**2)
            if distance_segment_suivant == 0:
                continue
            nx_next = -dy_next / distance_segment_suivant#vecteurs nomal du deuxieme segment 
            ny_next = dx_next / distance_segment_suivant
            vec_coin = vec_entre((nx,ny), (nx_next,ny_next), k) #récupere k vecteurs normaux entre les deux de base
            for vec in vec_coin:
                p = (vec[0]*distance+point_actuel[0],vec[1]*distance+point_actuel[1])
                nouvelle_forme.append(p)

    return nouvelle_forme[::-1]

def contient_polygone_point(pol,point):
        inter = 0

        for i in range (0,len(pol)):

            if (pol[i][0]<=point[0]<=pol[(i+1)%len(pol)][0] or pol[i][0]>=point[0]>=pol[(i+1)%len(pol)][0]) and pol[i][0] != pol[(i+1)%len(pol)] :
                a = (pol[(i+1)%len(pol)][1]-pol[i][1])/(pol[(i+1)%len(pol)][0]-pol[i][0])
                b = pol[i][1]-a*pol[i][0] # car PosA appartient a la droite donc veridie l'equation
                y_d = a*point[0] + b
                if y_d>=point[1]:
                    inter = inter+1
                #print("inter")
        return (inter%2==1)

def tourner_forme(points, degrees):
    #moyenne
    avg_x = sum([p[0] for p in points]) / len(points)
    avg_y = sum([p[1] for p in points]) / len(points)
    radians = math.radians(degrees)

    rotated_points = []
    for point in points:
        x = point[0] - avg_x
        y = point[1] - avg_y
        rotated_x = x * math.cos(radians) - y * math.sin(radians)
        rotated_y = x * math.sin(radians) + y * math.cos(radians)      
        rotated_points.append((rotated_x + avg_x, rotated_y + avg_y))
  
    return rotated_points
