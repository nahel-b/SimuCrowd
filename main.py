import chemin
import affichage
import lecteur
import Calcul_simulation
from classe import*

#detaille sur la geometrie de l'immeuble
nb_etage = 3
zoom = 10
taille_max = (20,30)
taille_fenetre = (1000,600)
forme_etage=[(1,1),(19,1),(19,29),(1,29)]
liste_escalier_descendant = [[(9.5,1)],[(1,14.5),(19,14.5)],[(19,27),(9.5,1)]]
liste_obstacle = [[[(4.5,3.3),(14,3.3),(9.5,12)]],[[(11,20),(11,6),(16,6),(15.7,20)],[(3.7,16.1),(1,11.3),(3.7,11)]],[[(4.5,3.3),(14,3.3),(9.5,12)],[(4.5,16),(14,16),(19,24)]]]
#95;196
batiment = batiment_class(nb_etage,taille_max,forme_etage,liste_escalier_descendant,liste_obstacle)

p1 = personne_classe(0,0,0,[(0,0)],0,0,"",0,0)
p1.basique((12.3,22.3),[(0,0)],0)
p2 = personne_classe(0,0,0,[(0,0)],0,0,"",0,0)
p2.basique((17,26.5),[(0,0)],1)
p3 = personne_classe(0,0,0,[(0,0)],0,0,"",0,0)
p3.basique((18.1,10.0),[(0,1)],2)
p4 = personne_classe(0,0,0,[(0,0)],0,0,"",0,0)
p4.basique((18.1,11.0),[(0,1)],3)
p5 = personne_classe(0,0,0,[(0,0)],0,0,"",0,0)
p5.basique((18.1,12.0),[(0,1)],4)
p6 = personne_classe(0,0,0,[(0,0)],0,0,"",0,0)
p6.basique((13.3,22.3),[(0,0)],5)
p7 = personne_classe(0,0,0,[(0,0)],0,0,"",0,0)
p7.basique((14.3,22.3),[(0,0)],6)
p8 = personne_classe(0,0,0,[(0,0)],0,0,"",0,0)
p8.basique((14.3,23.3),[(0,0)],7)
p9 = personne_classe(0,0,0,[(0,0)],0,0,"",0,0)
p9.basique((14.3,21.3),[(0,0)],8)

scene = scene_class(batiment,[p1,p2,p3,p4,p5,p6,p7,p8,p9],60)


chemin.initialisation_variable(scene,taille_fenetre)
fichier = Calcul_simulation.calcul_basique(scene,1,60*60,"test")
save(fichier.nom,fichier)
lecteur.lancer_lecteur(fichier,taille_fenetre,zoom)
#affichage.lancer_ex_chemin(batiment,taille_fenetre)

#save(fichier.nom,fichier)

