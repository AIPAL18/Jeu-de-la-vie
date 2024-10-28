from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtGui import QPen, QBrush
from PySide6.QtCore import Qt, QObject
from lib.constantes import Etat


class Cellule(QGraphicsRectItem):
    """
    Hérite de:
        object
        QGraphicsRectItem
    Rôle:
        Représente une cellule
    """
    def __init__(self, parent: QObject = None) -> None:
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

        # Déclare l'attribut etat est l'initialise à Mort
        self.etat: Etat = Etat.Mort
        # Définit la couleur du contour
        self.setPen(QPen(Qt.GlobalColor.white))
        # Définit la couleur de remplissage
        self.setBrush(QBrush(Qt.GlobalColor.white))
        # Définit le rectangle d'affichage (x, y, w, h)
        self.setRect(0, 0, 50, 50)
    
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
        # Si la cellule est vivante
        if self.etat is Etat.Vivant:
            # On remplit en noir
            self.setBrush(QBrush(Qt.GlobalColor.black))
        # si la cellule est morte
        else:
            # On remplit en blanc
            self.setBrush(QBrush(Qt.GlobalColor.white))
    
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