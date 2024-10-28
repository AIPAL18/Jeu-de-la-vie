from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import QObject
from lib.plateau import construit
from typing import Any
from lib.overload import Overload, signature
from lib.constantes import Etat, Direction
from .cellule import Cellule


class JDLV(QGraphicsScene):
    """
    Hérite de:
        object
        QGraphicsScene
    Rôle:
        Représente la scène du jeu de la vie (jdlv)
    """
    def __init__(self, parent: QObject = None) -> None:
        """
        Entrées:
            self: JDLV
            parent: QObject (par défaut None)
        Sortie:
            None (ctor)
        Rôle:
            Construit un nouvel objet JDLV
        """
        # On initialise la classe mère
        QGraphicsScene.__init__(self, parent)

        # Déclaration d'un attribut auto grandissement
        self.auto_grandissement = True

        # Déclaration d'une matrice vide
        self.matrice: list[list[Cellule]] = []
        # On construit le plateau de jeu d'après les attributs de la fenêtre
        self.set_plateau(
            parent.dimension.height(), parent.dimension.width(), Etat.Mort)
    
    def vide_scene(self) -> None:
        """
        Entrée:
            self: JDLV
        Sortie:
            None (modification en place)
        Rôle:
            Retire les éléments de la scène
        """
        # Pour chaque ligne de la matrice
        for i in range(len(self.matrice)):
            # Pour chaque colonne de la matrice
            for j in range(len(self.matrice[i])):
                # On retire l'élément de la scène
                self.removeItem(self.matrice[i][j])

    @Overload  # On appelle overload pour créer une méthode surchargée
    @signature("int", "int", "Etat")  # On précise sa signature
    def set_plateau(self, height: int, width: int, etat: Etat) -> None:
        """
        Entrée:
            self: JDLV
            height: int
            width: int
            etat: Etat
        Sortie:
            None (modification en place)
        Rôle:
            Créer un plateau de dimension height x width dans l'état etat.
        """
        # On remet le plateau en ordre
        self.vide_scene()
        # On itère dans le nombre de ligne
        for i in range(height):
            # On ajoute une ligne
            self.matrice.append([])
            # On itère dans le nombre d'élément pas ligne
            for j in range(width):
                # On créer une cellule
                temp = Cellule()
                # On ajuste sa position (w x h)
                temp.setPos(j * 50, i * 50)
                # On définit l'état de temp
                temp.set_etat(etat)
                # On ajoute la cellule à la matrice
                self.matrice[i].append(temp)
                # On ajoute la cellule à la scène
                self.addItem(temp)

    @set_plateau.overload  # On surcharge la méthode set_plateau
    @signature("list", "object")  # On précise sa signature
    def set_plateau(self, matrice: list[list[Any]], vivant: Any) -> None:
        """
        Surcharge de set_plateau
        Entrées:
            self: JDLV
            matrice: list[list[Any]]
            vivant: Any
        Sortie:
            None (modification en place)
        Rôle:
            Créer un plateau de même dimension que la matrice. si l'élément 
            vaut vivant, son état sera Vivant, sinon Mort.
        """
        # Redéfinit la hateur du plateau
        self.parent().dimension.setHeight(len(matrice))
        # Redéfinit la largeur du plateau
        self.parent().dimension.setWidth(len(matrice[0]))
        # Enlève toutes les cellules de la scène
        self.vide_scene()
        # Déclaration d'une matrice vide
        self.matrice = []
        # On itère dans le nombre de ligne
        for i in range(len(matrice)):
            # On ajoute une ligne
            self.matrice.append([])
            # On itère dans le nombre d'élément pas ligne
            for j in range(len(matrice[i])):
                # On créer une cellule
                temp = Cellule()
                # On ajuste sa position (w x h)
                temp.setPos(j * 50, i * 50)
                # Si la cellule (i;j) est vivante
                if matrice[i][j] == vivant:
                    # On définit l'état de temp sur vivant
                    temp.set_etat(Etat.Vivant)
                # Si la cellule (i;j) est mort
                else:
                    # On définit l'état de temp sur mort
                    temp.set_etat(Etat.Mort)
                # On ajoute la cellule à la matrice
                self.matrice[i].append(temp)
                # On ajoute la cellule à la scène
                self.addItem(temp)


    def est_voisin(self, i, j) -> bool:
        """
        Entrées:
            self: JeuDeLaVie
            i: int
            j: int
        Sortie:
            Etat
        Rôle:
            Retourne True si la cellule est vivante et donc est un voisin 
            potentiel, False sinon.
        """
        # si les indices décrivent une valeur du tableau
        if 0 <= i < len(self.matrice) and 0 <= j < len(self.matrice[0]):
            # si True si vivant, False sinon
            return self.matrice[i][j].get_etat() is Etat.Vivant
        # si l'indice i ou j est trop grand ou négatif, ou si la cellule est morte on retourne 0
        else:
            # Retourne False car l'élément inexistant est considéré mort
            return False


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
        # Récupère le voisin du bas (int(False) -> 0 et int(True) -> 1)
        b = int(self.est_voisin(i + 1, j))
        # Récupère le voisin du bas droit
        bd = int(self.est_voisin(i + 1, j + 1))
        # Récupère le voisin du bas gauche
        bg = int(self.est_voisin(i + 1, j - 1))
        # Récupère le voisin du haut
        h = int(self.est_voisin(i - 1, j))
        # Récupère le voisin du haut droit
        hd = int(self.est_voisin(i - 1, j + 1))
        # Récupère le voisin du haut gauche
        hg = int(self.est_voisin(i - 1, j - 1))
        # Récupère le voisin de droite
        d = int(self.est_voisin(i, j + 1))
        # Récupère le voisin de gauche
        g = int(self.est_voisin(i, j - 1))

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
        # Retourne True si nb_voisins est différent de 2 ou 3
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
        # Retourne True si nb_voisins est égal à 3
        return nb_voisins == 3


    def resultat(self, ord: int, absc: int) -> Etat:
        """
        Entrées:
            self: JeuDeLaVie
            ord: int (ordonnée)
            absc: int (abscisse)
        Sortie:
            Etat
        Rôle:
            Retourne l'état de la cellule en fonction du nombre de voisins
        """
        # On calcul le nombre de voisin
        nb_voisins = self.total_voisins(ord, absc)
        # si la cellule est vivante
        if self.matrice[ord][absc].get_etat() is Etat.Vivant:
            # si la cellule meurt
            if self.meurt(nb_voisins):
                # Retourne le nouvel état de la cellule
                return Etat.Mort
            # si la cellule ne change pas d'état
            else:
                # Retourne l'état de la cellule
                return Etat.Vivant
        # si la cellule est morte
        else:
            # si la cellule naît
            if self.nait(nb_voisins):
                # Retourne le nouvel état de la cellule
                return Etat.Vivant
            # si la cellule ne change pas d'état
            else:
                # Retourne l'état de la cellule
                return Etat.Mort
    
    def doit_agrandir_matrice(self) -> list[Direction]:
        """
        Entrée:
            self: JeuDeLaVie
        Sortie:
            tuple[bool, Direction]
        Rôle:
            retourne la liste des directions vers lesquelles il faut agrandir 
            la matrice
        """
        # Déclaration d'une liste qui représente les directions vers lesquelles 
        # il faut agrandir la matrice
        liste_directions = []
        
        # on teste la frontière nord:
        i = 0
        # Déclaration de variable d'arrêt et initialisation à False
        stop = False
        # Pour chaque cellule de la première ligne
        while not (i >= self.parent().dimension.width() or stop):
            # Si la cellule est vivante
            if self.matrice[0][i].get_etat() is Etat.Vivant:
                # On arrête la boucle
                stop = True
                # on ajoute Nord au direction
                liste_directions.append(Direction.Nord)
            # On icrémente l'itérateur
            i += 1
        
        # on teste la frontière sud:
        i = 0
        # Initialisation de stop à False
        stop = False
        # On cherche l'indice de la dernière ligne
        derniere_ligne = self.parent().dimension.height() - 1
        # Pour chaque cellule de la dernière ligne
        while not (i >= self.parent().dimension.width() or stop):
            # Si la cellule est vivante
            if self.matrice[derniere_ligne][i].get_etat() is Etat.Vivant:
                # On arrête la boucle
                stop = True
                # on ajoute Sud au direction
                liste_directions.append(Direction.Sud)
            # On icrémente l'itérateur
            i += 1
        
        # on teste la frontière ouest:
        i = 0
        # Initialisation de stop à False
        stop = False
        # Pour chaque ligne
        while not (i >= self.parent().dimension.height() or stop):
            # Si la dernière cellule est vivante
            if self.matrice[i][0].get_etat() is Etat.Vivant:
                # On arrête la boucle
                stop = True
                # on ajoute Ouest au direction
                liste_directions.append(Direction.Ouest)
            # On icrémente l'itérateur
            i += 1
        
        # on teste la frontière ouest:
        i = 0
        # Initialisation de stop à False
        stop = False
        # On cherche l'indice de la dernière colonne
        derniere_colonne = self.parent().dimension.width() - 1
        # Pour chaque ligne
        while not (i >= self.parent().dimension.height() or stop):
            # Si la dernière cellule est vivante
            if self.matrice[i][derniere_colonne].get_etat() is Etat.Vivant:
                # On arrête la boucle
                stop = True
                # on ajoute Est au direction
                liste_directions.append(Direction.Est)
            # On icrémente l'itérateur
            i += 1
        
        # Retourne la liste
        return liste_directions

    def extension(self, direction: str) -> None:
        """
        Entrées:
            self: JeuDeLaVie
            direction: Direction
        Sortie:
            None (modification en place)
        Rôle
            Étend la matrice vers une direction donnée
        """
        # Si la direction est Nord
        if direction is Direction.Nord:
            # Déclaration de abscisse
            abscisse = self.matrice[0][0].pos().x()
            # Déclaration de ordonnée
            ordonnée = self.matrice[0][0].pos().y() - 50
            # On ajoute une ligne à l'indice 0 (déplace les éléments)
            self.matrice.insert(0, [])
            # Pour chaque colonne
            for i in range(self.parent().dimension.width()):
                # On créer une cellule
                temp = Cellule()
                # On ajuste sa position (w x h)
                temp.setPos(abscisse + i * 50, ordonnée)
                # On définit l'état de temp
                temp.set_etat(Etat.Mort)
                # On ajoute la cellule à la matrice
                self.matrice[0].append(temp)
                # On ajoute la cellule à la scène
                self.addItem(temp)

            # On ajuste la dimension de la matrice
            self.parent().dimension.setHeight(
                self.parent().dimension.height() + 1
            )
        # Si la direction est Sud
        elif direction is Direction.Sud:
            # Déclaration de abscisse
            abscisse = self.matrice[0][0].pos().x()
            # Déclaration de ordonnée
            ordonnée = self.matrice[-1][0].pos().y() + 50
            # On ajoute une ligne à la fin de la matrice
            self.matrice.append([])
            # Pour chaque colonne
            for i in range(self.parent().dimension.width()):
                # On créer une cellule
                temp = Cellule()
                # On ajuste sa position (w x h)
                temp.setPos(abscisse + i * 50, ordonnée)
                # On définit l'état de temp
                temp.set_etat(Etat.Mort)
                # On ajoute la cellule à la matrice
                self.matrice[-1].append(temp)
                # On ajoute la cellule à la scène
                self.addItem(temp)

            # On ajuste la dimension de la matrice
            self.parent().dimension.setHeight(
                self.parent().dimension.height() + 1
            )
        # Si la direction est Est
        elif direction is Direction.Est:
            # Déclaration de ordonnée
            ordonnée = self.matrice[0][0].pos().y()
            # Déclaration de abscisse
            abscisse = self.matrice[0][-1].pos().x() + 50
            # Pour chaque ligne
            for i in range(self.parent().dimension.height()):
                # On créer une cellule
                temp = Cellule()
                # On ajuste sa position (w x h)
                temp.setPos(abscisse, ordonnée + i * 50)
                # On définit l'état de temp
                temp.set_etat(Etat.Mort)
                # On ajoute la cellule à la matrice
                self.matrice[i].append(temp)
                # On ajoute la cellule à la scène
                self.addItem(temp)

            # On ajuste la dimension de la matrice
            self.parent().dimension.setWidth(
                self.parent().dimension.width() + 1
            )
        # Si la direction est Ouest
        elif direction is Direction.Ouest:
            # Déclaration de ordonnée
            ordonnée = self.matrice[0][0].pos().y()
            # Déclaration de abscisse
            abscisse = self.matrice[0][0].pos().x() - 50
            # Pour chaque ligne
            for i in range(self.parent().dimension.height()):
                # On créer une cellule
                temp = Cellule()
                # On ajuste sa position (w x h)
                temp.setPos(abscisse, ordonnée + i * 50)
                # On définit l'état de temp
                temp.set_etat(Etat.Mort)
                # On ajoute la cellule à la matrice
                self.matrice[i].insert(0, temp)
                # On ajoute la cellule à la scène
                self.addItem(temp)

            # On ajuste la dimension de la matrice
            self.parent().dimension.setWidth(
                self.parent().dimension.width() + 1
            )
    
    def tour(self) -> None:
        """
        Entrée:
            self: JeuDeLaVie
        Sortie:
            None (modification en place)
        Rôle:
            Execute un tour du jeu.
        """
        # On créer un tableau qui ne contient que les états.
        tableau_etat = construit(
            self.parent().dimension.height(),
            self.parent().dimension.width(),
            Etat.Mort
        )
        
        # On calcul l'état de chaque cellule
        # on itère dans les lignes
        for i in range(len(self.matrice)):
            # on itère dans la ligne i
            for j in range(len(self.matrice[i])):
                # On stocke l'état dans le tableau d'état
                tableau_etat[i][j] = self.resultat(i, j)
        
        # On met à jour le tableau
        # on itère dans les lignes
        for i in range(len(self.matrice)):
            # on itère dans la ligne i
            for j in range(len(self.matrice[i])):
                # On met à jour l'état
                self.matrice[i][j].set_etat(tableau_etat[i][j])
        
        # On incrémente le nombre de cycle effectué
        self.parent().nb_cycle += 1
        # Mise à jour du texte du label affichage_cycle
        self.parent().affichage_cycle.setText("Cycle n°" + 
                                              str(self.parent().nb_cycle))
        
        # Si l'auto grandissement est activé:
        if self.auto_grandissement:
            # On cherche les directions vers lesquelles agrandir la matrice
            direction = self.doit_agrandir_matrice()
            # S'il faut agrandir
            if direction:  # vide -> False (conversion implicite par le if)
                # On itère dans les directions vers lesquelles agrandir
                for d in direction:
                    # Extension de la matrice vers la direction d
                    self.extension(d)