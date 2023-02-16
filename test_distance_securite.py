import math

def agrandir_forme(forme, distance,k):
    nouvelle_forme = []
    for i in range(len(forme)):
        point_actuel = forme[i]
        point_precedent = forme[i-1]
        dx = point_actuel[0] - point_precedent[0]
        dy = point_actuel[1] - point_precedent[1]
        distance_segment = math.sqrt(dx**2 + dy**2)
        if distance_segment == 0:
            nouvelle_forme.append(point_actuel)
            continue
        nx = -dy / distance_segment
        ny = dx / distance_segment
        nouveau_point1 = (point_precedent[0] + nx * distance, point_precedent[1] + ny * distance)
        nouveau_point2 = (point_actuel[0] + nx * distance, point_actuel[1] + ny * distance)
        nouvelle_forme.append(nouveau_point1)
        nouvelle_forme.append(nouveau_point2)
        
        # Ajout des coins
        point_suivant = forme[(i+1) % len(forme)]
        dx_next = point_suivant[0] - point_actuel[0]
        dy_next = point_suivant[1] - point_actuel[1]
        distance_segment_suivant = math.sqrt(dx_next**2 + dy_next**2)
        if distance_segment_suivant == 0:
            continue
        nx_next = -dy_next / distance_segment_suivant
        ny_next = dx_next / distance_segment_suivant
        angle = math.atan2(ny + ny_next, nx + nx_next)
        nx_coin = math.cos(angle)
        ny_coin = math.sin(angle)
        nouveau_point3 = (point_actuel[0] + nx_coin * distance, point_actuel[1] + ny_coin * distance)
        nouvelle_forme.append(nouveau_point3)
        
    return nouvelle_forme






import tkinter as tk


# Coordonnées de la forme initiale
forme = [(100, 100), (200, 20), (30, 50)]
# Coordonnées de la forme agrandie
forme_agrandie = agrandir_forme(forme,10,1)
# Créer la fenêtre et le canvas
root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Dessiner la forme initiale
canvas.create_polygon(forme_agrandie, fill="red")
canvas.create_polygon(forme, fill="blue")


# Créer le bouton pour agrandir la forme
#bouton = tk.Button(root, text="Agrandir", command=agrandir_forme)
#bouton.pack()

# Lancer la boucle principale
root.mainloop()
