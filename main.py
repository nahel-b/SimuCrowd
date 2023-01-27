import chemin
import affichage
import lecteur
import Calcul_simulation
from classe import*

#detaille sur la geometrie de l'immeuble
nb_etage = 3
taille_max = (200,300)
taille_fenetre = (1000,600)
forme_etage=[(5,5),(190,5),(190,290),(5,290)]
liste_escalier_descendant = [[(95,5)],[(5,145),(190,145)],[(190,270),(95,5)]]
liste_obstacle = [[[(45,33),(137,33),(95,122)]],[[(112,205),(112,58),(157,58),(157,205)],[(37,161),(4,113),(37,113)]],[[(45,33),(137,33),(95,122)],[(45,160),(137,160),(190,240)]]]
#95;196
batiment = batiment_class(nb_etage,taille_max,forme_etage,liste_escalier_descendant,liste_obstacle)

p1 = personne_classe(0,0,0,[(0,0)],0,0,"",0,0)
p1.basique((12.3,22.3),[(0,0)],0)
p2 = personne_classe(0,0,0,[(0,0)],0,0,"",0,0)
p2.basique((17,26.5),[(0,0)],1)
p3 = personne_classe(0,0,0,[(0,0)],0,0,"",0,0)
p3.basique((16.1,10.0),[(0,1)],2)
scene = scene_class(batiment,[p1,p2,p3],60)

chemin.initialisation_variable(batiment,taille_fenetre)
fichier = Calcul_simulation.calcul_basique(scene,1,60*60,"test")
save(fichier.nom,fichier)
lecteur.lancer_lecteur(fichier,taille_fenetre)
#affichage.lancer_ex_chemin(batiment,taille_fenetre)

#save(fichier.nom,fichier)

