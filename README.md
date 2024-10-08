# 🏃‍♂️ Simulateur de Mouvement de Foule 🏢

## 📄 Description

Ce projet est un logiciel entièrement écrit en Python permettant de simuler le mouvement de foules dans divers environnements. Le logiciel inclut un éditeur graphique pour personnaliser les bâtiments, ajouter des personnes avec des caractéristiques uniques, et observer leur comportement en fonction de différentes situations, comme des incendies ou des changements d'accès.

## ⚙️ Fonctionnalités

### 1. **🏗️ Éditeur Graphique de Bâtiments**
- Créez et éditez vos propres bâtiments.
- Ajoutez des éléments comme des murs, des portes, des escaliers, etc.
- Personnalisez les propriétés de l'environnement.

### 2. **👥 Ajout de Personnes**
- Ajoutez des individus à la foule avec des attributs spécifiques :
  - **📏 Taille** : définissez la taille des personnes.
  - **⚖️ Poids** : définissez le poids des individus.
  - **🏃‍♀️ Vitesse** : ajustez leur vitesse de déplacement.
  - **🧠 Caractère** : ajustez le caractère de chaque personne.
  - **😨 Comportement dans la foule** : définissez la réaction de chaque individu face aux situations de stress (incendie, surcharge, etc.).
  
### 3. **🛠️ Gestion des Objets et Situations**
- Modifiez les propriétés des portes, escaliers, et autres objets du bâtiment.
- Simulez des événements tels que des **🔥 incendies** ou des situations d’urgence.
  
### 4. **📊 Simulation de Mouvement de Foule**
- L'algorithme du logiciel calcule le mouvement de la foule en fonction des éléments configurés (personnalités, structure, obstacles).
- Paramétrez la durée de la simulation et suivez en temps réel le déplacement de chaque individu.

### 5. **🎥 Lecture des Simulations**
- Une fois la simulation terminée, visionnez l'expérience comme une vidéo, permettant d’analyser les comportements de la foule et l'efficacité des plans d'évacuation.

## 🛠️ Technologies Utilisées

- **🐍 Python** : Langage principal pour la logique et les algorithmes de simulation.
- **🖼️ Tkinter** : Utilisé pour l'interface graphique et l'éditeur visuel.
- **📐 NumPy** : Pour les calculs mathématiques complexes.
