# TP sur les Boids préparé par YON Alexis

# Installation
Pour installer les dépendances il est conseillé d'utiliser un venv :
```bash
python3 -m venv .venv
```
*Nb: remplacer python3 par le nom de votre executable python en fonction de la version*

Pour activer ce venv il suffit de taper une des commandes :
- Linux & MacOS : `source ./.venv/bin/activate`
- Windows : `.\.venv\Scripts\activate`


Une fois dans le venv via bash, cmd ou autre :
```bash
pip install -r requirements.txt
```
*N'hésitez pas à demander de l'aide si vous n'êtes pas habitués aux virtual env*

Veuillez à bien lancer le projet depuis le venv pour que les dépendances soient résolues. Une fois le TP terminé vous pourrez supprimer ce dossier et les dépendances ne pollueront pas votre PC.

# Introduction
Ce TP a pour but de vous familiariser avec le principe de l'algorithme boids. Pour celà, vous allez implémenter les divers comportements qui caractérisent les boids :
- Alignement
- Cohésion
- Séparation

Pour vous faciliter la tâche, le code permettant de faire le rendu en temps réel ainsi que l'architecture générale vous sont fournis. Vous trouverez dans le code plusieurs commentaires TODO indiquant du code à compléter. Un premier est au niveau de la boucle de rendu principale (main.py) et servira notamment à manipuler les poids des comportements. Le reste se trouve dans le corps de la classe Boid (boid.py) et correspond aux comportements à implémenter.

Pour lancer le projet il suffit de lancer main.py.

# Implémentation
Avant de se lancer dans le développement des différents comportements, il serait bon de savoir comment fonctionne le projet.

Ce programme permet de simuler un nombre défini de "boids" à une certaine fréquence d'affichage, si le programme tourne avec une fréquence de 60 FPS alors notre boucle de rendu devrait environ être appelée 60 fois par seconde. C'est dans cette boucle de rendu que l'on va appeler toute la logique de chaque boids avant de l'afficher à l'écran.

Les boids exploitent une classe Vector2, notamment pour exprimer la direction (à travers `Boid.getVelocity` et `Boid.setVelocity`) à l'aide d'un vecteur normalisé.

Pour implémenter les différents comportements il est donc préférable de retourner un vecteur par comportement, de l'ajouter à la velocité du boid en fonction d'un multiplicateur défini et d'enfin normaliser (`Boid.setVelocity` effectue une normalisation donc vous n'avez pas à le faire).

Dernièrement, les boids sont divisés dans une grille qui permet d'accélérer la recherche de voisins, pour chercher les voisins on utilisera donc `Boid.get_neighbours_in_grid` avec la grille déjà initialisée au début de la boucle de rendu. 

## Alignement
Le premier comportement que nous allons ajouter à nos boids est l'alignement. Le nom de ce comportement est assez descriptif, le but est bien d'aligner nos boids. Pour obtenir un vecteur relativement aligné, il suffit de **faire la moyenne des vélocités des autres boids** (et possiblement normaliser ce vecteur).

## Cohésion
La cohésion consiste à diriger un boid vers le centre de la nuée, c'est-à-dire **la moyenne des positions de chaque boids de la nuée**. Ce comportement peut aussi potentiellement bénéficier d'une normalisation.

## Séparation
La séparation permet d'éviter aux boids une collision avec un voisin. Pour celà on veut récupérer tous les voisins et en retirer un **vecteur non normalisé pour chaque voisin en dessous de la distance minimale**. La **somme de ces vecteurs nous donne une force de séparation** qui n'est donc pas normalisée, ce qui lui donne un poids variable.

# Résultats
Rien qu'avec ces trois comportements simples vous devriez avoir un rendu correct. IL est possible de changer le poids de chaque comportement dans la config si vous le souhaitez. N'hésitez pas à expérimenter !

# Bonus
## Prédateur
Si l'on souhaite aller plus loin il peut-être intéressant d'essayer de simuler la réaction de nos boids à un potentiel prédateur. Pour celà il est possible de refactoriser le programme pour abstraire une partie de Boids et en faire inhériter une nouvelle classe Predator. Il faut aussi implémenter un nouveau comportement de fuite chez les boids avec un poids associé.