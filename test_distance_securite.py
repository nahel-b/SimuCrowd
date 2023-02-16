import math

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
import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

def agrandir_forme(forme, distance,k): #k : le nb de point a ajouter pour les coin concaves
    nouvelle_forme = []
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

        # angle = math.atan2(ny + ny_next, nx + nx_next)
        # nx_coin = math.cos(angle)
        # ny_coin = math.sin(angle)
        # nouveau_point3 = (point_actuel[0] + nx_coin * distance, point_actuel[1] + ny_coin * distance)
        # nouvelle_forme.append(nouveau_point3)
        
    return nouvelle_forme








# Coordonnées de la forme initiale
forme = [(200, 100), (200, 20), (30, 50),(100,300),(150,150),(300,100)]
# Coordonnées de la forme agrandie
forme_agrandie = agrandir_forme(forme,10,2)
# Créer la fenêtre et le canvas


# Dessiner la forme initiale
canvas.create_polygon(forme_agrandie, fill="red")
canvas.create_polygon(forme, fill="blue")

for p in forme_agrandie:
    rayon = 2
    canvas.create_oval(p[0] -rayon, p[1]-rayon, p[0]+rayon,  p[1]+rayon, fill="black")

print(len(forme_agrandie))

# Créer le bouton pour agrandir la forme
#bouton = tk.Button(root, text="Agrandir", command=agrandir_forme)
#bouton.pack()

# Lancer la boucle principale
root.mainloop()
