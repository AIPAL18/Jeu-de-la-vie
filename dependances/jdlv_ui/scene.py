# Importe les classes utilisées du module PySide6.QtWidgets
from PySide6.QtWidgets import QGraphicsScene, QWidget, \
    QGraphicsSceneMouseEvent
# Importe les classes utilisées du module PySide6.QtGui
from PySide6.QtGui import QStatusTipEvent
# Importe les classes utilisées du module PySide6.QtCore
from PySide6.QtCore import Qt, QSize, QTimer, QEvent
# Importe construit depuis dependances.plateau
from dependances.plateau import construit
# Importe Any depuis typing
from typing import Any
# Importe Overload, signature depuis dependances.overload
from dependances.overload import Overload, signature
# Importe Etat, Direction depuis dependances.constantes
from dependances.constantes import Etat, Direction
# Importe Cellule depuis cellule
from .cellule import Cellule
# Importe deepcopy depuis copy
from copy import deepcopy


class Scene(QGraphicsScene):
    """
    Hérite de:
        QGraphicsScene
    Rôle:
        Représente la scène du jeu de la vie (Scene)
    """
    def __init__(self, parent: QWidget | None = None, 
                 taille: QSize = QSize(0, 0)) -> None:
        """
        Entrées:
            self: Scene
            parent QWidget (ligne d'héritage pour désallouer la mémoire)
                valeur par défaut: None
            taille: QSize
                valeur par défaut: QSize(0, 0)
        Sortie:
            None (ctor)
        Rôle:
            Construit un nouvel objet JDLV
        """
        # On initialise la classe mère
        QGraphicsScene.__init__(self, parent)
        
        # Déclaration de dimension qui représente la dimension du plateau
        # (w x h)
        self.dimension: QSize = taille
        # Déclaration d'un attribut auto grandissement
        self.auto_grandissement: bool = None
        # Déclaration d'un attribut auto stop
        self.auto_stop: bool = None
        # Déclaration d'interval
        self.periode: int = None
        # Déclaration d'un attribut est_souris_dans_scene
        self.est_souris_dans_scene = False

        # Déclaration d'un chronomètre
        self.chrono = QTimer(self)
        # Relie le signal à execute_tour
        self.chrono.timeout.connect(self.execute_tour)
        # Chrono moins précis mais moins gourmant en ressources
        self.chrono.setTimerType(Qt.TimerType.CoarseTimer)

        # Déclaration d'un tableau à l'état n-1
        self.tableau_precedent: list[list[Cellule]] = []
        # Déclaration d'un tableau vide
        self.tableau: list[list[Cellule]] = []
        # On construit le plateau de jeu d'après les attributs de la fenêtre
        self.set_plateau(
            self.dimension.height(), self.dimension.width(), Etat.Mort)
    
    def vide_scene(self) -> None:
        """
        Entrée:
            self: Scene
        Sortie:
            None (modification en place)
        Rôle:
            Retire les éléments de la scène
        """
        # Pour chaque ligne du tableau
        for i in range(len(self.tableau)):
            # Pour chaque colonne du tableau
            for j in range(len(self.tableau[i])):
                # On retire l'élément de la scène
                self.removeItem(self.tableau[i][j])

    @Overload  # On appelle overload pour créer une méthode surchargée
    @signature("int", "int", "Etat")  # On précise sa signature
    def set_plateau(self, height: int, width: int, etat: Etat) -> None:
        """
        Entrée:
            self: Scene
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
            self.tableau.append([])
            # On itère dans le nombre d'élément pas ligne
            for j in range(width):
                # On créer une cellule
                temp = Cellule()
                # On ajuste sa position (w x h)
                temp.setPos(j * 50, i * 50)
                # On définit l'état de temp
                temp.set_etat(etat)
                # On ajoute la cellule au tableau
                self.tableau[i].append(temp)
                # On ajoute la cellule à la scène
                self.addItem(temp)
        
        # Copie le tableau dans tableau_precedent
        self.tableau_precedent = deepcopy(self.tableau)

    @set_plateau.overload  # On surcharge la méthode set_plateau
    @signature("list", "object")  # On précise sa signature
    def set_plateau(self, tableau: list[list[Any]], vivant: Any) -> None:
        """
        Surcharge de set_plateau
        Entrées:
            self: Scene
            tableau: list[list[Any]]
            vivant: Any
        Sortie:
            None (modification en place)
        Rôle:
            Créer un plateau de même dimension que le tableau. Si l'élément 
            vaut vivant, son état sera Vivant, sinon Mort.
        """
        # Redéfinit la hateur du plateau
        self.dimension.setHeight(len(tableau))
        # Redéfinit la largeur du plateau
        self.dimension.setWidth(len(tableau[0]))
        # Enlève toutes les cellules de la scène
        self.vide_scene()
        # Déclaration d'un tableau vide
        self.tableau = []
        # On itère dans le nombre de ligne
        for i in range(len(tableau)):
            # On ajoute une ligne
            self.tableau.append([])
            # On itère dans le nombre d'élément pas ligne
            for j in range(len(tableau[i])):
                # On créer une cellule
                temp = Cellule()
                # On ajuste sa position (w x h)
                temp.setPos(j * 50, i * 50)
                # Si la cellule (i;j) est vivante
                if tableau[i][j] == vivant:
                    # On définit l'état de temp sur vivant
                    temp.set_etat(Etat.Vivant)
                # Si la cellule (i;j) est mort
                else:
                    # On définit l'état de temp sur mort
                    temp.set_etat(Etat.Mort)
                # On ajoute la cellule au tableau
                self.tableau[i].append(temp)
                # On ajoute la cellule à la scène
                self.addItem(temp)
        
        # Copie le tableau dans tableau_precedent
        self.tableau_precedent = deepcopy(self.tableau)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Réimplémentation de mouseMoveEvent hérité de QGraphicsScene
        Entrées:
            self: Scene
            even: QGraphicsSceneMouseEvent
        Sortie:
            None (modification en place)
        Rôle:
            Capture l'événement QGraphicsSceneMouseEvent, le traite et le rend.
        """
        # Abscisse de la souris
        x = event.scenePos().x()
        # Ordonnée de la souris
        y = event.scenePos().y()
        # Ordonnée du haut de la scène
        haut = self.sceneRect().top()
        # Ordonnée du bas de la scène
        bas = self.sceneRect().bottom()
        # Abscisse de côté gauche de la scène
        gauche = self.sceneRect().left()
        # Abscisse de côté droit de la scène
        droit = self.sceneRect().right()
        # Si la souris est dans le rectangle de la scène
        if gauche <= x < droit and haut <= y < bas:
            # Si la souris n'est pas encore entrée dans la scène
            if not self.est_souris_dans_scene:
                # Pour chaque vue
                for vue in self.views():
                    # On dit à la vue que la souris est partie
                    vue.event(QEvent(QEvent.Type.Leave))
            # On passe l'attribut est_souris_dans_scene à True
            self.est_souris_dans_scene = True
            # On calcul l'indice i de la cellule dans le tableau
            i = int((y - haut) // 50)
            # On calcul l'indice j de la cellule dans le tableau
            j = int((x - gauche) // 50)
            # Si le bouton gauche de la souris est pressé
            if event.buttons() is Qt.MouseButton.LeftButton:
                # On définit l'état de la cellule touchée par la souris sur 
                # Vivant
                self.tableau[i][j].set_etat(Etat.Vivant)
            # Si le bouton droit de la souris est pressé
            elif event.buttons() is Qt.MouseButton.RightButton:
                # On définit l'état de la cellule touchée par la souris sur 
                # Mort
                self.tableau[i][j].set_etat(Etat.Mort)
        # Si la souris n'est plus dans la scène et que l'attribut 
        # est_souris_dans_scene est encore sur True
        elif self.est_souris_dans_scene:
            # On passe l'attribut est_souris_dans_scene sur False, puisqu'elle est 
            # sortie
            self.est_souris_dans_scene = False
            # Pour chaque vue de la scène
            for vue in self.views():
                # On dit à la vue que la souris est sortie de la scène, donc 
                # entrée dans la vue
                vue.event(QEvent(QEvent.Type.Enter))
        
        # Rend l'événement à la classe mère
        return super().mouseMoveEvent(event)
    
    def event(self, even: QEvent) -> bool:
        """
        Réimplémentation de event hérité de QMainWindow
        Entrées:
            self: Scene
            even: QEvent (et les classes qui en hérite)
        Sortie:
            bool
        Rôle:
            Capture les événements de QMainWindow, les traites, puis les rends.
        """
        # Si le type de l'évènement est StatusTipEvent
        if even.type() is QEvent.Type.StatusTip:
            # On précise le type de l'évènement pour être sûr de pouvoir 
            # accéder aux méthodes (optionnel)
            even: QStatusTipEvent = even
            # Relais l'évènement à la classe mère
            self.parent().event(even)
            """
            Fonctionnement:
            Chaque objet possédant l'attribut statusTip émet un signal 
            QStatusTipEvent lorsque la souris le survole. Ce signal comporte un
            tip, un conseil, concernant le dit objet. Il est par défaut 
            réceptionné par statusBar de QMainWindow, mais il peut être 
            intercepté et affiché autre part.
            """
        
        # On rend l'évènement à la classe mère
        return super().event(even)

    def get_plateau(self, vivant: Any, mort: Any) -> list[list[Any]]:
        """
        Entrées:
            self: Scene
            vivant: Any
            mort: Any
        Sortie:
            list[list[Any]]  (consitué uniquement de vivant et mort)
        Rôle:
            Retourne le plateau de jeu avec des valeurs personnalisées de 
            vivant et mort.
        """
        # Déclaration d'un tableau vide plateau
        plateau: list[list] = []
        # Pour chaque ligne de tableau
        for i in range(len(self.tableau)):
            # Ajout d'une nouvelle ligne dans plateau
            plateau.append([])
            # Pour chaque élément de la ligne
            for j in range(len(self.tableau[i])):
                # Si l'élément (i;j) est d'état vivant
                if self.tableau[i][j].get_etat() is Etat.Vivant:
                    # On ajoute la valeur vivant au plateau
                    plateau[i].append(vivant)
                # Si l'élément (i;j) est d'état mort
                else:
                    # On ajoute la valeur mort au plateau
                    plateau[i].append(mort)
        
        # On retourne le plateau
        return plateau

    def valeur_case(self, i, j) -> bool:
        """
        Entrées:
            self: Scene
            i: int
            j: int
        Sortie:
            bool
        Rôle:
            Retourne True si la cellule est vivante et donc est un voisin 
            potentiel, False sinon.
        """
        # si les indices décrivent une valeur du tableau
        if 0 <= i < len(self.tableau) and 0 <= j < len(self.tableau[0]):
            # si True si vivant, False sinon
            return self.tableau[i][j].get_etat() is Etat.Vivant
        # si l'indice i ou j est trop grand ou négatif, ou si la cellule est 
        # morte on retourne 0
        else:
            # Retourne False car l'élément inexistant est considéré mort
            return False

    def total_voisins(self, i: int, j: int) -> int:
        """
        Entrées:
            self: Scene
            i: int
            j: int
        Sortie:
            int
        Rôle:
            Retourne le total de voisins de la cellule (i;j)
        """
        # Récupère le voisin du bas (int(False) -> 0 et int(True) -> 1)
        b = int(self.valeur_case(i + 1, j))
        # Récupère le voisin du bas droit
        bd = int(self.valeur_case(i + 1, j + 1))
        # Récupère le voisin du bas gauche
        bg = int(self.valeur_case(i + 1, j - 1))
        # Récupère le voisin du haut
        h = int(self.valeur_case(i - 1, j))
        # Récupère le voisin du haut droit
        hd = int(self.valeur_case(i - 1, j + 1))
        # Récupère le voisin du haut gauche
        hg = int(self.valeur_case(i - 1, j - 1))
        # Récupère le voisin de droite
        d = int(self.valeur_case(i, j + 1))
        # Récupère le voisin de gauche
        g = int(self.valeur_case(i, j - 1))

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
            self: Scene
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
        if self.tableau[ord][absc].get_etat() is Etat.Vivant:
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
    
    def doit_agrandir_tableau(self) -> list[Direction]:
        """
        Entrée:
            self: Scene
        Sortie:
            tuple[bool, Direction]
        Rôle:
            retourne la liste des directions vers lesquelles il faut agrandir 
            le tableau
        """
        # Déclaration d'une liste qui représente les directions vers lesquelles 
        # il faut agrandir le tableau
        liste_directions = []
        
        # on teste la frontière nord:
        i = 0
        # Déclaration de variable d'arrêt et initialisation à False
        stop = False
        # Pour chaque cellule de la première ligne
        while not (i >= self.dimension.width() or stop):
            # Si la cellule est vivante
            if self.tableau[0][i].get_etat() is Etat.Vivant:
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
        derniere_ligne = self.dimension.height() - 1
        # Pour chaque cellule de la dernière ligne
        while not (i >= self.dimension.width() or stop):
            # Si la cellule est vivante
            if self.tableau[derniere_ligne][i].get_etat() is Etat.Vivant:
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
        while not (i >= self.dimension.height() or stop):
            # Si la dernière cellule est vivante
            if self.tableau[i][0].get_etat() is Etat.Vivant:
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
        derniere_colonne = self.dimension.width() - 1
        # Pour chaque ligne
        while not (i >= self.dimension.height() or stop):
            # Si la dernière cellule est vivante
            if self.tableau[i][derniere_colonne].get_etat() is Etat.Vivant:
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
            self: Scene
            direction: Direction
        Sortie:
            None (modification en place)
        Rôle
            Étend le tableau vers une direction donnée
        """
        # Si la direction est Nord
        if direction is Direction.Nord:
            # Déclaration de abscisse
            abscisse = self.tableau[0][0].pos().x()
            # Déclaration de ordonnée
            ordonnée = self.tableau[0][0].pos().y() - 50
            # On ajoute une ligne à l'indice 0 (déplace les éléments)
            self.tableau.insert(0, [])
            # Pour chaque colonne
            for i in range(self.dimension.width()):
                # On créer une cellule
                temp = Cellule()
                # On ajuste sa position (w x h)
                temp.setPos(abscisse + i * 50, ordonnée)
                # On définit l'état de temp
                temp.set_etat(Etat.Mort)
                # On ajoute la cellule au tableau
                self.tableau[0].append(temp)
                # On ajoute la cellule à la scène
                self.addItem(temp)

            # On ajuste la dimension du tableau
            self.dimension.setHeight(self.dimension.height() + 1)
        # Si la direction est Sud
        elif direction is Direction.Sud:
            # Déclaration de abscisse
            abscisse = self.tableau[0][0].pos().x()
            # Déclaration de ordonnée
            ordonnée = self.tableau[-1][0].pos().y() + 50
            # On ajoute une ligne à la fin du tableau
            self.tableau.append([])
            # Pour chaque colonne
            for i in range(self.dimension.width()):
                # On créer une cellule
                temp = Cellule()
                # On ajuste sa position (w x h)
                temp.setPos(abscisse + i * 50, ordonnée)
                # On définit l'état de temp
                temp.set_etat(Etat.Mort)
                # On ajoute la cellule au tableau
                self.tableau[-1].append(temp)
                # On ajoute la cellule à la scène
                self.addItem(temp)

            # On ajuste la dimension du tableau
            self.dimension.setHeight(self.dimension.height() + 1)
        # Si la direction est Est
        elif direction is Direction.Est:
            # Déclaration de ordonnée
            ordonnée = self.tableau[0][0].pos().y()
            # Déclaration de abscisse
            abscisse = self.tableau[0][-1].pos().x() + 50
            # Pour chaque ligne
            for i in range(self.dimension.height()):
                # On créer une cellule
                temp = Cellule()
                # On ajuste sa position (w x h)
                temp.setPos(abscisse, ordonnée + i * 50)
                # On définit l'état de temp
                temp.set_etat(Etat.Mort)
                # On ajoute la cellule au tableau
                self.tableau[i].append(temp)
                # On ajoute la cellule à la scène
                self.addItem(temp)

            # On ajuste la dimension du tableau
            self.dimension.setWidth(self.dimension.width() + 1)
        # Si la direction est Ouest
        elif direction is Direction.Ouest:
            # Déclaration de ordonnée
            ordonnée = self.tableau[0][0].pos().y()
            # Déclaration de abscisse
            abscisse = self.tableau[0][0].pos().x() - 50
            # Pour chaque ligne
            for i in range(self.dimension.height()):
                # On créer une cellule
                temp = Cellule()
                # On ajuste sa position (w x h)
                temp.setPos(abscisse, ordonnée + i * 50)
                # On définit l'état de temp
                temp.set_etat(Etat.Mort)
                # On ajoute la cellule au tableau
                self.tableau[i].insert(0, temp)
                # On ajoute la cellule à la scène
                self.addItem(temp)

            # On ajuste la dimension du tableau
            self.dimension.setWidth(self.dimension.width() + 1)

    def arret_automatique(self) -> bool:
        """
        Entrée:
            self: Scene
        Sortie:
            bool
        Rôle:
            vérifie si deux tour de suite sont identique
        """
        # retourne True si le tableau n'a pas changé entre deux cycles
        return self.tableau_precedent == self.tableau
    
    def tour(self) -> None:
        """
        Entrée:
            self: Scene
        Sortie:
            None (modification en place)
        Rôle:
            Execute un tour du jeu.
        """
        # Si l'auto stop est activé
        if self.auto_stop:
            # Copie le tableau dans tableau_precedent
            self.tableau_precedent = deepcopy(self.tableau)

        # On créer un tableau qui ne contient que les états.
        tableau_etat = construit(
            self.dimension.height(), self.dimension.width(), Etat.Mort)
        
        # On calcul l'état de chaque cellule
        # on itère dans les lignes
        for i in range(len(self.tableau)):
            # on itère dans la ligne i
            for j in range(len(self.tableau[i])):
                # On stocke l'état dans le tableau d'état
                tableau_etat[i][j] = self.resultat(i, j)
        
        # On met à jour le tableau
        # on itère dans les lignes
        for i in range(len(self.tableau)):
            # on itère dans la ligne i
            for j in range(len(self.tableau[i])):
                # On met à jour l'état
                self.tableau[i][j].set_etat(tableau_etat[i][j])
        
        # On incrémente le nombre de cycle effectué
        self.parent().nb_cycle += 1
        # Mise à jour du texte du label affichage_cycle
        self.parent().affichage_cycle.setText("Cycle n°" + 
                                              str(self.parent().nb_cycle))
        
        # Si l'auto grandissement est activé:
        if self.auto_grandissement:
            # On cherche les directions vers lesquelles agrandir le tableau
            direction = self.doit_agrandir_tableau()
            # S'il faut agrandir
            if direction:  # vide -> False (conversion implicite par le if)
                # On itère dans les directions vers lesquelles agrandir
                for d in direction:
                    # Extension du tableau vers la direction d
                    self.extension(d)
        
        # Si l'auto stop est activé et que l'animation doit s'arrêter
        if self.auto_stop and self.arret_automatique():
            # On stop l'animation
            self.parent().stop_anim()
    
    def execute_tour(self) -> None:
        """
        Entrées:
            self: Scene
        Sortie:
            None (modification en place)
        Rôle:
            Execute un tour
        """
        # Mise à jour de l'interval de temps
        self.chrono.setInterval(self.periode)
        # Execute un tour
        self.tour()
