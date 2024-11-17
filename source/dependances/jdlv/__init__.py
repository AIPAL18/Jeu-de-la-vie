###############################################################################
#                                                                             #
#                             Elie RUGGIERO                                   #
#                                                                             #
#      CC BY-NC-SA (https://creativecommons.org/licenses/by-nc-sa/4.0/)       #
#                                                                             #
###############################################################################

r"""
JDLV UI
=======
Dépendences de jeu_de_la_vie_gui

Scene
-----
Scène du jeu de la vie

Cellule
-------
Représente une cellule du jeu de la vie

construit
---------
Construit une matrice de taille désirée avec une valeur par défaut

est_template_valide
-------------------
Vérifie la validité d'un template pour devenir le nouveau tableau
"""

from .cellule import Cellule
from .scene import Scene
from .tableau import construit, est_template_valide
