from typing import Any
from re import search


def copie(matrice: list[list[Any]]) -> list[list[Any]]:
    """
    Entrée:
        matrice: list[list[Any]]
    Sortie:
        matrice: list[list[Any]]
    Rôle:
        Retourne la copie mémoire de matrice
    P.S.:
        Pour les listes imbriquées on peut utiliser:
        >>> import copy
        >>> b = copy.deepcopy(a)
    """
    # Déclaration d'un tableau vide
    tableau = []

    # Pour chaque ligne de la matrice
    for i in range(len(matrice)):
        # On ajoute une nouvelle ligne au tableau
        tableau.append([])
        # Pour chaque élément de la ligne
        for j in range(len(matrice[i])):
            # On ajoute l'élément à la ligne du tableau
            tableau[i].append(matrice[i][j])
    
    # On retourne le tableau
    return tableau


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


def extention(matrice: list[list[Any]], direction: str, nb_element: int, 
              valeur_defaut: Any) -> list[list[Any]]:
    """
    Entrées:
        matrice: list[list[Any]]
        direction: str
        nb_element: int
        valeur_defaut: Any
    Sortie:
        matrice: list[list[Any]]
    Rôle
        Étend la matrice vers une direction donnée d'un nombre d'élément donné
    """
    # On uniformise la variable direction
    direction = direction.upper()
    # Si la direction demandée est valide
    if direction in ["N", "E", "S", "O"]:
        # On déclare une variable hauteur
        hauteur = len(matrice)
        # Si la hauteur de la matrice <= 0, il n'y a pas de largeur
        largeur = 0
        # Si la hauteur de la matrice > 0, il y a une largeur
        if hauteur > 0:
            largeur = len(matrice[0])
        
        # Si on veut étendre la matrice vers le nord (↑)
        if direction == "N":
            # On copie la matrice dans une variable temporaire
            temp = copie(matrice)
            # On construit une matrice de la hauteur de l'extention et de la 
            # lageur de la matrice
            matrice = construit([nb_element, largeur], valeur_defaut)
            # On étend la matrice avec la variable la matrice temporaire
            matrice.extend(temp)
        # Si on veut étendre la matrice vers l'est (→)
        elif direction == "E":
            # Pour chaque ligne de la matrice
            for ligne in matrice:
                # On étend la ligne du nombre d'élément demandé
                ligne.extend([valeur_defaut for i in range(nb_element)])
        # Si on veut étendre la matrice vers le sud (↓)
        elif direction == "S":
            # On construit une matrice de la hauteur de l'extention et de la 
            # lageur de la matrice
            temp = construit([nb_element, largeur], valeur_defaut)
            # On étend la matrice avec la variable la matrice temporaire
            matrice.extend(temp)
        # Si on veut étendre la matrice vers l'ouest (←)
        elif direction == "O":
            # On déclare une matrice temporaire
            matrice_temp = []
            # Pour chaque ligne de la matrice
            for ligne in matrice:
                temp = [valeur_defaut for i in range(nb_element)]
                # On étend la ligne du nombre d'élément demandé
                temp.extend(ligne)
                # On ajoute la ligne à la matrice temporaire
                matrice_temp.append(temp)
            # On affecte la valeur de matrice_temp à la variable matrice
            matrice = matrice_temp
        # On retroune la nouvelle matrice
        return matrice
    # Si la direction demandée n'est pas valide
    else:
        # Affichage d'un message d'erreur
        print("On ne peut pas étendre dans la direction", direction)
        # On retroune la matrice
        return matrice


def est_template_valide(tableau: Any) -> tuple[bool, str]:
    """
    Entrée:
        tableau: list[list[0 | 1]]  (pésumé)
    Sortie:
        tuple[bool, str]
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
                message = "Les éléments doivent être 0 ou 1. Ils doivent " + \
                    "être séparés par des virgules."
                # On arrête la boucle
                lignes_valide = False
            
            # Incrémentation de l'itérateur
            i += 1
        
        # On retourne True si toutes les lignes sont valides, False sinon
        return lignes_valide, message
    
    # On retourne False sinon
    return False, message
