from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsSceneMouseEvent
from PySide6.QtGui import QPen, QBrush
from PySide6.QtCore import Qt, QObject
from lib.constantes import Etat
from copy import deepcopy


class Cellule(QGraphicsRectItem):
    """
    Hérite de:
        QGraphicsRectItem
    Rôle:
        Représente une cellule
    """
    def __init__(self, parent: QObject = None, etat: Etat = Etat.Vivant)\
        -> None:
        """
        Entrée:
            self: Cellule
            parent QObjet (ligne d'héritage pour désallouer la mémoire)
        Sortie:
            None (ctor)
        Rôle:
            Construit un nouvel objet Cellule
        """
        # Initialise la classe mère
        QGraphicsRectItem.__init__(self, parent)
        # on définit l'état 
        self.etat = etat
        # On peint la cellule en fonction de l'état
        self.peint()
        # Définit le rectangle d'affichage (x, y, w, h)
        self.setRect(0, 0, 50, 50)
    
    def peint(self) -> None:
        """
        Entrée:
            self: Cellule
        Sortie:
            None (modification en place)
        Rôle:
            Définit la couleur de la couleur
        """
        # Si la cellule est vivante
        if self.etat is Etat.Vivant:
            # Définit la couleur du contour
            self.setPen(QPen(Qt.GlobalColor.black))
            # On remplit en noir
            self.setBrush(QBrush(Qt.GlobalColor.black))
        # si la cellule est morte
        else:
            # Définit la couleur du contour
            self.setPen(QPen(Qt.GlobalColor.white))
            # On remplit en blanc
            self.setBrush(QBrush(Qt.GlobalColor.white))

    def mousePressEvent(self, even: QGraphicsSceneMouseEvent) -> None:
        """
        Rééimplémentation de mousePressEvent hérité de QGraphicsRectItem
        Entrées:
            self: Cellule
            even: QGraphicsSceneMouseEvent (évenement)
        Sortie:
            None (modification en place)
        Rôle:
            Détecte les évenements de pression de souris sur la cellule.
        """
        # Inverse l'état de la cellule
        self.etat = Etat(not self.etat.value)
        # On peint la cellule en fonction de l'état
        self.peint()

        return super().mousePressEvent(even)

    def set_etat(self, etat: Etat) -> None:
        """
        Entrées:
            self: Cellule
            vivant: Etat
        Sortie:
            None (modification en place)
        Rôle:
            Redéfinit l'état de la cellule True -> vivant, False -> mort
        """
        # On met à jour l'attribut est_vivant
        self.etat = etat
        # On peint la cellule en fonction de l'état
        self.peint()

    def get_etat(self) -> Etat:
        """
        Entrée:
            self: Cellule
        Sortie:
            bool
        Rôle:
            Retourne l'état de la cellule True -> vivant et False -> mort
        """
        # On retourne la valeur de l'attribut est_vivant
        return self.etat
    
    def __repr__(self) -> str:
        """
        Entrée:
            self: Cellule
        Sortie:
            str
        Rôle:
            Méthode magique __repr__, représentation.
        """
        # Si la cellule est vivante
        if self.etat is Etat.Vivant:
            # Retourne ■
            return "■"
        # Sinon
        else:
            # Retourne □
            return "□"
    
    def __deepcopy__(self, memo):
        """
        P.S.:
            https://stackoverflow.com/questions/1500718/how-to-override-the-copy-deepcopy-operations-for-a-python-object
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def __eq__(self, valeur: object) -> bool:
        return self.etat == valeur.etat
