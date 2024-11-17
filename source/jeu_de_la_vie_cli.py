# Importe sleep depuis time
from time import sleep
# Importe system depuis os
from os import system
# importe exists depuis os.path
from os.path import exists
# Importe Any depuis typing
from typing import Any, Literal
# Importe copie depuis dependances.plateau
from dependances.jdlv import est_template_valide
# Importe argv, version_info depuis le module sys
from sys import version_info
# Importe reader depuis csv
from csv import reader
# Importe deepcopy depuis copy
from copy import deepcopy


class JeuDeLaVieCLI(object):
    """
    Hérite de:
        object
    Rôle:
        Représente le jeu de la vie.
    """

    def __init__(self, plateau: list[list[Literal[1] | Literal[0]]] = [])\
        -> None:
        """
        Entrées:
            self: JeuDeLaVieCLI
            tableau: list[list[Literal[1] | Literal[0]]]
                valeur par défaut: []
        Sortie:
            None (modification en place)
        Rôle:
            Construit un nouvel objet JeuDeLaVieCLI.
        """
        # Déclaration d'un tableau au cycle n-1, initialisé vide
        self.tableau_precedent: list[list[Literal[1] | Literal[0]]] = []
        # Déclaration de tableau et l'initialise à plateau
        self.tableau: list[list[Literal[1] | Literal[0]]] = plateau
        # Déclaration de symbol_mort et l'initialise à □
        self.symbole_mort = "□"
        # Déclaration de symbole_vivant et l'initialise à ■
        self.symbole_vivant = "■"
    
    def set_symbole_mort(self, symb_mort: Any) -> None:
        """
        Entrées:
            self: JeuDeLaVieCLI
            symb_mort: Any
        Sortie:
            None (modification en place)
        Rôle:
            Redéfinit le symbole des cases mortes (affichage_complexe).
        """
        # définie le nouveau symbole d'une cellule morte
        self.symbole_mort = str(symb_mort)
    
    def set_symbole_vivant(self, symb_vivant: Any) -> None:
        """
        Entrées:
            self: JeuDeLaVieCLI
            symb_vivant: Any
        Sortie:
            None (modification en place)
        Rôle:
            Redéfinit le symbole des cases vivantes (affichage_complexe).
        """
        # définie le nouveau symbole d'une cellule morte
        self.symbole_vivant = str(symb_vivant)
    
    @staticmethod
    def est_tableau_valide(plateau: Any) -> bool:
        """
        Entrée:
            plateau: list[list[Any]]
        Sortie:
            bool (validité)
        Rôle:
            Vérifie la capacité du plateau à être un tableau.
        """
        # Déclaration de valide et initialisation sur False
        valide = True

        # Si plateau est une liste
        if type(plateau) is list:
            # Déclaration d'un itérateur
            i = 0
            # Pour chaque valeur de plateau tant que valide vaut True
            while i < len(plateau) and valide:
                # Si plateau à l'indice i n'est pas une liste
                if type(plateau[i]) is not list:
                    # On passe valide à False
                    valide = False
                # Incrémentation de l'itérateur
                i += 1
        # Si plateau n'est pas une liste
        else:
            # On passe valide à False
            valide = False
                
        # Retourne la valeur de valide
        return valide
    
    def set_tableau(self, plateau: Any, vivant: Any = 1) -> bool:
        """
        Entrées:
            self: JeuDeLaVieCLI
            plateau: list[list[Any]] (attendu)
            vivant: Any
                valeur par défaut: 1
        Sortie:
            bool (validité)
        Rôle:
            Redéfinit l'attribut tableau de même dimension que le matrice. Si 
            l'élément vaut vivant, son état sera Vivant, sinon Mort.
        """
        # Si le plateau est apte à devenir tableau
        if self.est_tableau_valide(plateau):
            # On vide tableau
            self.tableau = []
            # Pour chaque indice de plateau
            for i in range(len(plateau)):
                # On ajoute une ligne à tableau
                self.tableau.append([])
                # Pour chaque indice de plateau à l'indice i
                for j in range(len(plateau[i])):
                    # Si l'élément (i;j) de plateau est vivant
                    if plateau[i][j] == vivant:
                        # On ajoute 1 à tableau (vivant)
                        self.tableau[i].append(1)
                    # Sinon
                    else:
                        # On ajoute 0 à tableau (mort)
                        self.tableau[i].append(0)
            # On retourne True car la procédure c'est bien déroulée
            return True
        
        # On retourne False car le plateau ne peut être utilisé comme tableau
        return False
    
    def __repr__(self) -> str:
        """
        Entrées:
            self: JeuDeLaVieCLI
        Sortie:
            str
        Rôle:
            Retourne une représentation en chaîne de caractères de manière 
            simple (matrice de 1 et de 0).
        """
        reponse = ""
        # Pour chaque ligne du tableau
        for ligne in self.tableau:
            # Pour chaque cellule de la ligne
            for cellule in ligne:
                # On ajoute la valeur de cellule en chaîne de caractères plus 
                # un espace
                reponse += str(cellule) + " "
            # On ajoute un retour à la ligne
            reponse += "\n"
            
        # On retourne la chaîne de caractère
        return reponse

    def affiche(self) -> None:
        """
        Entrées:
            self: JeuDeLaVieCLI
        Sortie:
            None (affichage)
        Rôle:
            Afficher de manière complexe un tableau de cellules remplacées 
            par des caractères.
        """
        # On efface le terminal
        system("cls")
        # crée la variable temporaire tab
        tab = self.tableau
        # pour chaque ligne du tableau
        for ligne in tab:
            # on crée une variable temporaire pour chaque ligne
            ligne_affiche = []
            for valeur in ligne:
                # si la valeur dans le tableau est 0 on ajoute
                # self.symbole_mort à la variable temporaire
                if valeur == 0:
                    ligne_affiche.append(self.symbole_mort)
                # si la valeur dans le tableau est 1 on ajoute
                # self.symbole_vivant à la variable temporaire
                else:
                    ligne_affiche.append(self.symbole_vivant)
            # On affiche la variable temporaire en enlevant les ""
            print(" ".join(ligne_affiche))
        # On affiche une ligne vide
        print()

    def valeur_case(self, i: int, j: int) -> Literal[0] | Literal[1]:
        """
        Entrées:
            self: JeuDeLaVieCLI
            i: int
            j: int
        Sortie:
            Literal[0] | Literal[1]
        Rôle:
            Donner l'état d'une case (1 ou 0).
        """
        # si les indices décrivent une valeur du tableau
        if 0 <= i < len(self.tableau) and 0 <= j < len(self.tableau[0]):
            # On retourne la valeur de la case (i;j)
            return self.tableau[i][j]
        # si l'indice i ou j est trop grand ou négatif
        else:
            # on retourne 0
            return 0

    def total_voisins(self, i: int, j: int) -> int:
        """
        Entrées:
            self: JeuDeLaVieCLI
            i: int
            j: int
        Sortie:
            int
        Rôle:
            Retourne le total de voisins de la cellule (i;j)
        """
        # Récupère le voisin du bas
        b = self.valeur_case(i + 1, j)
        # Récupère le voisin du bas droit
        bd = self.valeur_case(i + 1, j + 1)
        # Récupère le voisin du bas gauche
        bg = self.valeur_case(i + 1, j - 1)
        # Récupère le voisin du haut
        h = self.valeur_case(i - 1, j)
        # Récupère le voisin du haut droit
        hd = self.valeur_case(i - 1, j + 1)
        # Récupère le voisin du haut gauche
        hg = self.valeur_case(i - 1, j - 1)
        # Récupère le voisin de droite
        d = self.valeur_case(i, j + 1)
        # Récupère le voisin de gauche
        g = self.valeur_case(i, j - 1)

        # retourne la somme des voisins
        return b + bd + bg + h + hd + hg + d + g

    @staticmethod
    def meurt(nb_voisins: int) -> bool:
        """
        Entrée:
            nb_voisins: int
        Sortie:
            bool
        Rôle:
            Retourne True si la cellule meurt
        """
        # Retourne True si le nombre de voisins est différent de 2 ou 3
        return nb_voisins < 2 or nb_voisins > 3

    @staticmethod
    def nait(nb_voisins: int) -> bool:
        """
        Entrée:
            nb_voisins: int
        Sortie:
            bool
        Rôle:
            Retourne True si la cellule naît
        """
        # Retourne True si le nombre de voisins est égal à 3
        return nb_voisins == 3

    def resultat(self, i: int, j: int) -> Literal[0] | Literal[1]:
        """
        Entrées:
            self: JeuDeLaVieCLI
            i: int (ordonnée)
            j: int (abscisse)
        Sortie:
            Literal[0] | Literal[1] (Etat de la cellule)
        Rôle:
            Retourne l'état de la cellule en fonction du nombre de voisins
        """
        # On calcul le nombre de voisin
        nb_voisins = self.total_voisins(i, j)
        # si la cellule == 1 (vivante)
        if self.tableau[i][j]:
            # si la cellule meurt
            if self.meurt(nb_voisins):
                # On met à jour la valeur dans le faux tableau
                return 0
            # Sinon
            else:
                # On retourne la valeur de (i;j)
                return 1
        # si la cellule == 0 (morte)
        else:
            # si la cellule naît
            if self.nait(nb_voisins):
                # On met à jour la valeur dans le faux tableau
                return 1
            # Sinon
            else:
                # On retourne la valeur de (i;j)
                return 0

    def tour(self) -> None:
        """
        Entrée:
            self: JeuDeLaVieCLI
        Sortie:
            None (modification en place)
        Rôle:
            Execute un tour du jeu.
        """
        # On copie le tableau pour pouvoir geler le vrai pour faire les modifs
        self.tableau_precedent = deepcopy(self.tableau)
        # On déclare tableau comme une copie de l'attribut tableau (gèle)
        tableau = deepcopy(self.tableau)

        # on itère dans les lignes
        for i in range(len(self.tableau)):
            # on itère dans la ligne i
            for j in range(len(self.tableau[i])):
                tableau[i][j] = self.resultat(i, j)
        
        # On attribut le tableau gelé au vrai tableau
        self.tableau = tableau

    def arret_automatique(self) -> bool:
        """
        Entrée:
            self: JeuDeLaVieCLI
        Sortie:
            bool
        Rôle:
            Renvoie True si le plateau est identique deux tours de suite, False
            sinon.
        """
        # retourne True si le tableau n'a pas changé entre deux cycles
        return self.tableau_precedent == self.tableau

    def run(self, nombre_tours: int, delai: float) -> None:
        """
        Entrées:
            self: JeuDeLaVieCLI
            nombre_tours: int
            delai: float
        Sortie:
            None (modification en place)
        Rôle:
            Effectue nombre_tours cycles de delai seconde(s).
        """
        # Si le tableau n'est pas vide
        if self.tableau:
            # On déclare un itérateur i
            i = 0
            # se répète en fonction du nombre de tour
            while i < nombre_tours:
                # si 2 tours à la suite sont identique
                if self.arret_automatique():
                    # on stop la boucle
                    i = nombre_tours - 1
                # sinon la boucle réactualise eu prochain tour
                else:
                    # affiche la matrice de JeuDeLaVieCLI
                    self.affiche()
                    # actualise la matrice
                    self.tour()
                    # laisse un temps d'attente entre chaque tour
                    sleep(delai)
                # on incrémente n pour que la boucle ait une terminaison
                i += 1
                # Affiche le dernier tour de boucle
            self.affiche()
    
    def importe_template(self, fichier: str) -> bool:
        """
        Entrées:
            self: JeuDeLaVieCLI
            fichier: str
        Sortie:
            bool (validité)
        Rôle:
            Importe le template si celui-ci est valide.
        """
        # Si le fichier existe
        if exists(fichier):
            # On ouvre le fichier en mode lecture
            with open(file=fichier, mode='r', encoding='utf8') as f:
                # On extrait les données
                template = f.readlines()
                # On ferme le fichier
                f.close()
            # Si le template est valide
            valide, erreur = est_template_valide(template)
            if valide:
                # Attribut à tableau une matrice vide
                self.tableau = []
                # Pour chaque ligne
                for i, ligne in enumerate(reader(template)):
                    # On ajoute une nouvelle ligne à la matrice
                    self.tableau.append([])
                    # Pour chaque élément de la ligne
                    for element in ligne:
                        # On ajoute l'élément converti en int
                        self.tableau[i].append(int(element))
                # On retoure True
                return True
            else:
                print(erreur)
        # On retourne False
        return False                        


# Si le présent fichier est executé avec python 3.10 ou plus
if __name__ == "__main__" and version_info >= (3, 10):
    
    # Exemple:

    # Déclare jeu en tant qu'instance de JeuDeLaVieCLI 
    jeu = JeuDeLaVieCLI()

    # importe le template choisit dans le jeu
    jeu.importe_template(r"..\\templates\\glider gun.csv")        

    # lance le jeu de la vie pour 75 cycles de 0.2 seconde
    jeu.run(75, 0.2)
