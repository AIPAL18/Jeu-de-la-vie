from time import sleep
from os import system
from typing import Any
from lib import copie


class JeuDeLaVie(object):
    """
    Hérite de:
        object
    Rôle:
        Représente le jeu de la vie.
    """

    def __init__(self, plateau: list[list[1 | 0]]) -> None:
        """
        Entrées:
            self: JeuDeLaVie
            tableau: list[list[1 | 0]]
        Sortie:
            None (modification en place)
        Rôle:
            Initialise la classe et créer les attributs
        """
        # Déclaration d'un tableau au cycle n-1, initialisé à None
        self.tableau_precedent = None
        # Déclaration de tableau et l'initialise à plateau
        self.tableau = plateau
        # Déclaration de symbol_mort et l'initialise à □
        self.symbole_mort = "□"
        # Déclaration de symbole_vivant et l'initialise à ■
        self.symbole_vivant = "■"
    
    def set_symbole_mort(self, symb_mort: Any) -> None:
        """
        Entrées:
            self: JeuDeLaVie
            symb_mort: Any
        Sortie:
            None (modification en place)
        Rôle:
            Redéfinit le symbole des cases mortes
        """
        # définie le nouveau symbole d'une cellule morte
        self.symbole_mort = str(symb_mort)
    
    def set_symbole_mort(self, symb_vivant: Any) -> None:
        """
        Entrées:
            self: JeuDeLaVie
            symb_vivant: Any
        Sortie:
            None (modification en place)
        Rôle:
            Redéfinit le symbole des cases vivantes
        """
        # définie le nouveau symbole d'une cellule morte
        self.symbole_vivant = str(symb_vivant)
    
    def affiche_simple(self):
        """
        Entrées:
            self: JeuDeLaVie
        Sortie:
            /
        Rôle:
            Afficher de manière simple une matrice de 1 et de 0
        """
        # crée la variable temporaire tableau
        tableau = self.tableau
        # affiche le tableau ligne par ligne
        for ligne in tableau:
            print(ligne)
        print()

    def valeur_case(self, i, j):
        """
        Entrées:
            self: JeuDeLaVie
            i: int
            j: int
        Sortie:
            int
        Rôle:
            Donner l'état d'une case (1 ou 0)
        """
        # si les indices décrivent une valeur du tableau
        if 0 <= i < len(self.tableau) and 0 <= j < len(self.tableau[0]):
            return self.tableau[i][j]
        # si l'indice i ou j est trop grand ou négatif on retourne 0
        else:
            return 0

    def affiche_complexe(self):
        """
        Entrées:
            self: JeuDeLaVie
        Sortie:
            /
        Rôle:
            Afficher de manière complexe un tableau de 1 et de 0
            en les remplaçant par des substitue
        """
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
        print()

    def total_voisins(self, i: int, j: int) -> int:
        """
        Entrées:
            self: JeuDeLaVie
            i: int
            j: int
        Sortie:
            int
        Rôle:
            Retourne le total de voisins de la cellule (i;j)
        """
        # bas
        b = self.valeur_case(i + 1, j)
        # bas droite
        bd = self.valeur_case(i + 1, j + 1)
        # bas gauche
        bg = self.valeur_case(i + 1, j - 1)
        # haut
        h = self.valeur_case(i - 1, j)
        # haut droite
        hd = self.valeur_case(i - 1, j + 1)
        # haut gauche
        hg = self.valeur_case(i - 1, j - 1)
        # droite
        d = self.valeur_case(i, j + 1)
        # gauche
        g = self.valeur_case(i, j - 1)
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
        return nb_voisins == 3

    def resultat(self, i: int, j: int) -> int:
        """
        Entrées:
            self: JeuDeLaVie
            i: int (ordonnée)
            j: int (abscisse)
        Sortie:
            int (Etat de la cellule)
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
            else:
                return 1
        # si la cellule == 0 (morte)
        else:
            # si la cellule naît
            if self.nait(nb_voisins):
                # On met à jour la valeur dans le faux tableau
                return 1
            else:
                return 0

    def tour(self) -> None:
        """
        Entrée:
            self: JeuDeLaVie
        Sortie:
            None (modification en place)
        Rôle:
            Execute un tour du jeu.
        """
        # On copie le tableau pour pouvoir geler le vrai pour faire les modifs
        self.tableau_precedent = copie(self.tableau)
        tableau = copie(self.tableau)

        # on itère dans les lignes
        for i in range(len(self.tableau)):
            # on itère dans la ligne i
            for j in range(len(self.tableau[i])):
                tableau[i][j] = self.resultat(i, j)
        
        self.tableau = tableau   

    def arret_automatique(self):
        """
        Entrée:
            self: JeuDeLaVie
        Sortie:
            bool
        Rôle:
            vérifie si deux tour de suite sont identique
        """
        # retourne True si le tableau n'a pas changé entre deux cycles
        return self.tableau_precedent == self.tableau

    def run(self, nombre_tours, delai):
        """
        Entrées:
            self: JeuDeLaVie
            nombre_tours: int
            delai: float
        Sortie:
            /
        Rôle:
            Fait tourner le Jeu De La Vie
        """
        # on définie n qui sera notre variant pour la terminaison de la boucle
        n = 0
        # se répète en fonction du nombre de tour
        while n < nombre_tours:
            # si 2 tours à la suite sont identique
            if self.arret_automatique():
                # on stop la boucle
                n = nombre_tours - 1
            # sinon la boucle réactualise eu prochain tour
            else:
                # affiche la matrice de JeuDeLaVie
                self.affiche_complexe()
                # actualise la matrice
                self.tour()
                # laisse un temps d'attente entre chaque tour
                sleep(delai)
            # on incrémente n pour que la boucle ait une terminaison
            n += 1
            # Affiche le dernier tour de boucle
        self.affiche_complexe()


if __name__ == "__main__" and __package__ is None:
    __package__ = ""
    # variable test
    jeu = JeuDeLaVie([
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,0,0,0,0],
        [0,0,0,0,0,1,0,1,0,0],
        [0,0,0,0,0,1,1,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0]
        ])


    # lance le jeu de la vie pour 50 cycle de 0.3 seconde
    jeu.run(50, 0.3)
