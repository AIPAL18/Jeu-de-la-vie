# Importe les classes utilisées du module PySide6.QtWidgets
from PySide6.QtWidgets import QGraphicsSceneHoverEvent, QGraphicsItem, \
    QGraphicsRectItem, QGraphicsSceneMouseEvent
# Importe les classes utilisées du module PySide6.QtGui
from PySide6.QtGui import QPen, QBrush, QStatusTipEvent
# Importe les classes utilisées du module PySide6.QtCore
from PySide6.QtCore import Qt
# Importe Etat depuis dependances.constantes
from dependances.constantes import Etat
# Importe deepcopy depuis copy
from copy import deepcopy
# Importe Any depuis typing
from typing import Any


class Cellule(QGraphicsRectItem):
    """
    Hérite de:
        QGraphicsRectItem
    Rôle:
        Représente une cellule
    """
    def __init__(self, parent: QGraphicsItem | None = None, 
                 etat: Etat = Etat.Vivant) -> None:
        """
        Entrée:
            self: Cellule
            parent QGraphicsItem | None
                valeur par défaut: None
            etat: Etat
        Sortie:
            None (ctor)
        Rôle:
            Construit un nouvel objet Cellule
        """
        # Initialise la classe mère
        QGraphicsRectItem.__init__(self, parent)
        # L'objet accepte de recevoir les événements de survole de la souris
        self.setAcceptHoverEvents(True)
        # on définit l'état 
        self.etat = etat
        # On peint la cellule en fonction de l'état
        self.peint()
        # Définit le rectangle d'affichage (x, y, w, h)
        self.setRect(0, 0, 50, 50)
        # Définit la couleur et taille du contour sur transparent et 0
        # car le contour agrandit le rectangle
        self.setPen(QPen(Qt.GlobalColor.transparent, 0))
    
    def peint(self) -> None:
        """
        Entrée:
            self: Cellule
        Sortie:
            None (modification en place)
        Rôle:
            Définit la couleur de la cellule
        """
        # Si la cellule est vivante
        if self.etat is Etat.Vivant:
            # On remplit en noir
            self.setBrush(QBrush(Qt.GlobalColor.black))
        # si la cellule est morte
        else:
            # On remplit en blanc
            self.setBrush(QBrush(Qt.GlobalColor.white))

    def mousePressEvent(self, even: QGraphicsSceneMouseEvent) -> None:
        """
        Réimplémentation de mousePressEvent hérité de QGraphicsRectItem
        Entrées:
            self: Cellule
            even: QGraphicsSceneMouseEvent (événement)
        Sortie:
            None (modification en place)
        Rôle:
            Détecte les événements de pression de souris sur la cellule.
        """
        # Si le click est un click gauche
        if even.button() is Qt.MouseButton.LeftButton:
            # Inverse l'état de la cellule
            self.etat = Etat.Vivant
        elif even.button() is Qt.MouseButton.RightButton:
            # Inverse l'état de la cellule
            self.etat = Etat.Mort
        # On peint la cellule en fonction de l'état
        self.peint()

        # On rend l'événement à la classe mère
        return super().mousePressEvent(even)
    
    def hoverEnterEvent(self, even: QGraphicsSceneHoverEvent) -> None:
        """
        Réimplémentation de hoverEnterEvent hérité de QGraphicsScene
        Entrées:
            self: Cellule
            even: QEvent (et les classes qui en hérite)
        Sortie:
            bool
        Rôle:
            Capture les événements de QGraphicsRectItem, les traites, puis les 
            rends.
        """
        # Si la cellule est vivante
        if self.etat is Etat.Vivant:
            # Envoie un évènement QStatusTipEvent à la scène mère
            self.scene().event(QStatusTipEvent(
                "Cliquez droit pour changer l'état. Pour modifier l'état de " +
                "plusieurs cellules, maintenez le clique droit en déplaçant " +
                "la souris."))
        # Si la cellule est morte
        else:
            # Envoie un évènement QStatusTipEvent à la scène mère
            self.scene().event(QStatusTipEvent(
                "Cliquez gauche pour changer l'état. Pour modifier l'état " +
                "de plusieurs cellules, maintenez le clique gauche en " + 
                "déplaçant la souris."))
        
        # Rend l'évènement
        return super().hoverEnterEvent(even)

    def set_etat(self, etat: Etat) -> None:
        """
        Entrées:
            self: Cellule
            etat: Etat
        Sortie:
            None (modification en place)
        Rôle:
            Redéfinit l'état de la cellule.
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
            Etat
        Rôle:
            Retourne l'état de la cellule.
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
            Méthode magique __repr__, représentation de la cellule en str.
        """
        # Si la cellule est vivante
        if self.etat is Etat.Vivant:
            # Retourne ■
            return "■"
        # Si la cellule est morte
        else:
            # Retourne □
            return "□"
    
    def __deepcopy__(self, memo: dict) -> object:
        """
        Entrées:
            self: Cellule
            memo: dict
        Sortie:
            object (copie de self)
        Rôle:
            Méthode magique du module copy pour effectuer des copies de 
            l'object.
        Addendum:
            Ne connaissant pas le module copy, j'ai utilisé la réponse 
            suivante : https://stackoverflow.com/a/15774013/15793884
        """
        # classe de self (Cellule)
        cls = self.__class__
        # Créer une nouvelle instance de Cellule
        result = cls.__new__(cls)
        # ajoute au dictionnaire memo le couple identifant du présent object et 
        # nouvel object
        memo[id(self)] = result
        # Pour chaque nom d'attribut et sa valeur de self (le présent object)
        for k, v in self.__dict__.items():
            # On affecte à l'attribut k de result une copie de la valeur de 
            # l'attribut k
            setattr(result, k, deepcopy(v, memo))
        
        # Revoie l'object copié
        return result

    def __eq__(self, valeur: Any) -> bool:
        """
        Entrées:
            self: Cellule
            valeur: Any
        Sortie:
            bool
        Rôle:
            Méthode magique appelée par l'opérateur d'égalité ==. 
        Explications:
            Une explication complète du fonctionnement de __eq__ est disponible
            via le lien suivant: https://stackoverflow.com/a/3588809/15793884
        """
        # Retoure True si etat est égal à valeur
        return self.etat == valeur
