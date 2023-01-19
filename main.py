import chemin
import affichage

#detaille sur la geometrie de l'immeuble
nb_etage = 3
taille_max = (200,300)
taille_fenetre = (1000,600)
forme_etage=[(5,5),(190,5),(190,290),(5,290)]
liste_escalier_descendant = [[(95,5)],[(5,145),(190,145)],[(190,270),(95,5)]]
liste_obstacle = [[[(45,33),(137,33),(95,122)]],[[(112,205),(112,58),(157,58),(157,205)],[(37,161),(4,113),(37,113)]],[[(45,33),(137,33),(95,122)],[(45,160),(137,160),(190,240)]]]
#95;196


chemin.initialisation_variable(liste_escalier_descendant,liste_obstacle,forme_etage,nb_etage)

affichage.lancer_ex_chemin(nb_etage,taille_max,taille_fenetre,forme_etage,liste_escalier_descendant,liste_obstacle)


