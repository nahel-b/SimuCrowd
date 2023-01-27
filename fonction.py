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

def MultListe(a,z):
        res = []
        for couple in a:
            res.append((couple[0]*z,couple[1]*z))
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
def plus_liste(p,l) :
    res = [0]*len(l)
    for i in range(len(l)):
        res[i] = (l[i][0]+p[0],l[i][1]+p[1])
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


