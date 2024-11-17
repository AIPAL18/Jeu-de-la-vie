from typing import Any
from re import search


def construit(h: int, l: int, valeur_defaut: Any) -> list[list[Any]]:
    """
    Entrée:
        h: int (hauteur)
        l: int (largeur)
    Sortie:
        list[list[int]]
    Rôle:
        Construit un tableau de taille taille avec comme valeur valeur_defaut
    """
    # Déclaration d'un tableau vide
    plateau = []

    # Pour chaque ligne de la matrice (de hauteur h)
    for i in range(h):
        # On ajoute une nouvelle ligne au tableau
        plateau.append([])
        # Pour chaque élément de la ligne (de longeur l)
        for _ in range(l):
            # On ajoute la valeur par défaut à la ligne du tableau
            plateau[i].append(valeur_defaut)

    # On retourne le tableau
    return plateau


def est_template_valide(tableau: Any) -> tuple[bool, str]:
    """
    Entrée:
        tableau: list[str]  (attendu)
    Sortie:
        tuple[
            bool,   (validité)
            str     (message d'erreur)
        ]
    Rôle:
        Retourne True si le tableau respecte le format d'un template. En cas
        d'erreur, le deuxième élément sera le message qui explique l'erreur.
    """
    message = ""
    # Si le tableau est de type list
    if type(tableau) is list:
        # Déclare taille et l'initialise à -1
        taille = -1
        # Déclaration d'une variable d'arrêt
        lignes_valide = True
        # Déclaration d'un itérateur
        i = 0
        # Pour chaque ligne du tableau tant que les lignes sont valides
        while i < len(tableau) and lignes_valide:
            # Si la ligne du tableau est une chaîne de caractères
            if type(tableau[i]) is str:
                # On cherche l'expression régulière suivante dans la ligne
                # ^ : on part du premier caractère
                # $ : on s'arrête au dernier caractère
                # 0-1 : l'élément est soit 0 soit 1
                # , : il est suivit d'une virgule
                # * : il est présent 0 ou plus fois
                # \\n : la ligne finit par \n
                correspondance = search("^[0-1,]*\\n$", tableau[i])
                
                # S'il y a une correspondance
                if correspondance:
                    # Si la taille n'a pas encore été définit
                    if taille == -1:
                        # On définit la taille d'une ligne
                        taille = len(tableau[i])
                    # Si la ligne ne fait pas la même taille que la première
                    if len(tableau[i]) != taille:
                        # On définit un message d'erreur
                        message = "Les lignes doivent être de même taille"
                        # On arrête la boucle
                        lignes_valide = False
                # S'il n'y a pas de correspondance
                else:
                    # On définit un message d'erreur
                    message = "Les éléments doivent être 0 ou 1. Ils " +\
                        "doivent être séparés par des virgules."
                    # On arrête la boucle
                    lignes_valide = False
            else:
                # On définit un message d'erreur
                message = "Chaque ligne doit être une chaîne de caractère " +\
                    "encodant la valeurs des cellules."
                # On arrête la boucle
                lignes_valide = False
            
            # Incrémentation de l'itérateur
            i += 1
        
        # On retourne True si toutes les lignes sont valides, False sinon
        return lignes_valide, message
    
    # On retourne False sinon
    return False, message
