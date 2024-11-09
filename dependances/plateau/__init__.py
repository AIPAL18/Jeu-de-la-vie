###############################################################################
#                                                                             #
#                             Elie RUGGIERO                                   #
#                                                                             #
#      CC BY-NC-SA (https://creativecommons.org/licenses/by-nc-sa/4.0/)       #
#                                                                             #
###############################################################################

r"""
Fonction de manipulation de tableau
===================================

copie
-----
Copie une matrice (moins efficace que deepcopy du module copy de python)

construit
---------
Construit une matrice de taille désirée avec une valeur par défaut

extention
---------
Etend une matrice dans une direction donnée, d'un nombre d'élément donné avec 
une valeur par défaut
est_template_valide
-------------------
Vérifie la validité d'un template pour faire office de tableau
"""

from .plateau import copie, construit, extention, est_template_valide
