from PySide6.QtWidgets import QMainWindow, QApplication, QGraphicsView, \
    QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QDoubleSpinBox, QLabel, \
    QGridLayout, QCheckBox, QFileDialog, QMessageBox
from PySide6.QtGui import QIcon, QAction, QKeySequence
from PySide6.QtCore import Qt, QSize, QTimer,  QDir
from csv import reader
from sys import argv
from lib import *


class JeuDeLaVieApp(QMainWindow):
    """
    Hérite de:
        QMainWindow
    Rôle:
        Représente l'application du jeu de la vie
    """
    def __init__(self) -> None:
        """
        Entrée:
            self: JeuDeLaVieApp
        Sortie:
            None (ctor)
        Rôle:
            Construit un nouvel objet JeuDeLaVieApp
        """
        # Initialisation de la classe mère
        QMainWindow.__init__(self)

        # Attributs
        
        # Déclaration de dimension qui représente la dimension du plateau
        # (w x h)
        self.dimension = QSize(20, 20)
        # Déclaration d'un booléan est_fichier_ouvert
        self.est_fichier_ouvert: bool = False
        self.fichier: str = ""
        # Déclaration d'un attribut nb_cycle
        self.nb_cycle: int = 0
        # Déclaration d'un chronomètre
        self.chrono = QTimer(self)
        # Relie le signal à execute_tour
        self.chrono.timeout.connect(self.execute_tour)
        # Chrono moins précis mais moins gourmant en ressources
        self.chrono.setTimerType(Qt.TimerType.CoarseTimer)

        # Fenêtre

        # Définit une taille minimum pour la fenêtre
        self.setMinimumSize(710, 400)
        # Redimensionne la fenêtre 
        self.resize(self.screen().geometry().width() - 400, 
                    self.screen().geometry().height() - 300)
        # Replace la fenêtre
        self.move(
            (self.screen().geometry().width() - self.width()) // 2,
            (self.screen().geometry().height() - self.height()) // 2 - 50)
        # On créer central_widget
        self.central_widget = QWidget(self)
        # On définit central_widget comme le widget principal
        # (celui qui prend toute la place)
        self.setCentralWidget(self.central_widget)
        # On créer le layout principal
        self.affichage = QHBoxLayout()
        # On associe le layout au widget car setCentralLayout n'existe pas
        self.central_widget.setLayout(self.affichage)

        # Menu bar

        # Déclaration d'un attribut menuBar
        self.menu = self.menuBar()
        # Déclaration d'un attribut menu fichier
        self.menu_fichier = self.menu.addMenu("&Fichier")
        # Déclaration de importer_template
        self.importer_template = QAction(self)
        # Définition du texte de importer_template
        self.importer_template.setText("Importer un template (.csv)")
        # Définition d'un raccourci clavier
        self.importer_template.setShortcut(QKeySequence.StandardKey.Open)
        # Relie le signal à la méthode importe
        self.importer_template.triggered.connect(self.importe)
        # Ajoute l'action au menu
        self.menu_fichier.addAction(self.importer_template)

        # Déclaration de enregistrer_template
        self.enregistrer_template = QAction(self)
        # Définition du texte de enregistrer_template
        self.enregistrer_template.setText("Enregistrer le template")
        # Définition d'un raccourci clavier
        self.enregistrer_template.setShortcut(QKeySequence.StandardKey.Save)
        # Relie le signal à la méthode enregistrer
        self.enregistrer_template.triggered.connect(self.enregistrer)
        # Ajoute l'action au menu
        self.menu_fichier.addAction(self.enregistrer_template)

        # Scène - vue

        # On créer une scène du jeu de la vie
        self.scene = Scene(self)
        # On créer une vue
        self.vue = QGraphicsView(self)
        # On dit à la vue quelle scène afficher
        # Fonctionnement -> https://doc.qt.io/qt-6/graphicsview.html
        self.vue.setScene(self.scene)
        # On définit l'échelle (fonctionne par pourcentage d'agrandissement)
        self.vue.scale(0.2, 0.2)
        # On ajoute la vue au layout principal
        self.affichage.addWidget(self.vue)

        # Menu

        # Déclaration d'un layout vertical menu_layout, layout ≃ div en html
        self.menu_layout = QVBoxLayout()
        # On définit les options d'alignement du layout
        self.menu_layout.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        # Déclaration d'un label
        self.affichage_cycle = QLabel(self)
        # Modifie le texe du label
        self.affichage_cycle.setText("Cycle n°" + str(self.nb_cycle))
        # Ajoute le label dans le layout
        self.menu_layout.addWidget(self.affichage_cycle)
        
        # Déclaration d'un layout horizontal play/pause
        self.controles_layout = QHBoxLayout()
        # Déclaration d'un bouton play
        self.play = QPushButton(self)
        # Définition de l'icone de play
        icone_play = QIcon("assets\\icones\\play-button.svg")
        # Attribution de l'icone au bouton
        self.play.setIcon(icone_play)
        # Relie le signal à la méthode run
        self.play.clicked.connect(self.lance_anim)
        # Modification du style de play
        self.play.setStyleSheet("padding-top: 7px; padding-bottom: 7px")
        # Modification automatique de la taille
        self.play.adjustSize()
        # On ajoute play à controles_layout
        self.controles_layout.addWidget(self.play)
        # Déclaration d'un bouton pause
        self.pause = QPushButton(self)
        # Définition de l'icone de pause
        icone_pause = QIcon("assets\\icones\\pause-button.svg")
        # Attribution de l'icone au bouton
        self.pause.setIcon(icone_pause)
        # Relie le signal à la méthode stop
        self.pause.clicked.connect(self.stop_anim)
        # Désactive le bouton pause
        self.pause.setEnabled(False)
        # Modification du style de pause
        self.pause.setStyleSheet("padding-top: 7px; padding-bottom: 7px")
        # Modification automatique de la taille
        self.pause.adjustSize()
        # On ajoute pause à controles_layout
        self.controles_layout.addWidget(self.pause)
        # On ajoute un peu d'espace entre le haut de la fenêtre et les boutons
        self.menu_layout.addSpacing(20)
        # On ajoute controles_layout à menu_layout
        self.menu_layout.addLayout(self.controles_layout)

        # Déclaration de periode_layout
        self.periode_layout = QGridLayout()
        # Déclaration de periode_label
        self.periode_label = QLabel(self)
        # Définition du texte de periode_label
        self.periode_label.setText("Durée d'une période :")
        # Déclaration de periode_entree
        self.periode_entree = QDoubleSpinBox(self)
        # On définit la valeur minimal de periode_entree
        self.periode_entree.setMinimum(0.01)
        # Définition de la valeur de periode_entree
        self.periode_entree.setValue(0.5)
        # Définition du pas de periode_entree
        self.periode_entree.setSingleStep(0.1)
        # On définit le suffix de periode_entree
        self.periode_entree.setSuffix(" sec")
        # On définit la largeur minimal de periode_entree
        self.periode_entree.setMinimumWidth(120)
        # Ajoute periode_label dans la cellule (0;0) du layout
        self.periode_layout.addWidget(self.periode_label, 0, 0)
        # Ajoute periode_entree dans la cellule (0;1) du layout
        self.periode_layout.addWidget(self.periode_entree, 0, 1)
        # Ajoute periode_layout à menu_layout
        self.menu_layout.addLayout(self.periode_layout)
        
        # Déclaration du bouton tour par tour
        self.tour_par_tour = QPushButton(self)
        # On définit le texte à afficher
        self.tour_par_tour.setText("Tour par tour")
        # Relie le signal à la méthode tour de la scène
        self.tour_par_tour.clicked.connect(self.scene.tour)
        # On ajoute tour_par_tour au layout du menu
        self.menu_layout.addWidget(self.tour_par_tour)

        # Déclaration d'une case à cocher
        self.auto_grandissement_entree = QCheckBox(self)
        # Définition du texte de la case à cocher
        self.auto_grandissement_entree.setText("Auto grandissement")
        # On définit son état sur coché
        self.auto_grandissement_entree.setCheckState(Qt.CheckState.Checked)
        # Relie le signal à la fonction set_auto_grandissement
        self.auto_grandissement_entree.checkStateChanged.connect(
            self.set_auto_grandissement)
        # On ajoute la case à cocher au layout
        self.menu_layout.addWidget(self.auto_grandissement_entree)

        # Déclaration d'un layout horizontal
        self.zoom = QGridLayout()
        # Déclaration d'un label zoom
        self.zoom_label = QLabel("Zoom:")
        self.zoom.addWidget(self.zoom_label, 0, 0, 1, 2)
        # Déclaration d'un bouton z_in (zoom in)
        self.z_in = QPushButton(self)
        # Définition du texte du bouton
        self.z_in.setText("+")
        # Relie le signal à la méthode zoom_in
        self.z_in.clicked.connect(self.zoom_in)
        # On ajoute z_in au layout zoom
        self.zoom.addWidget(self.z_in, 1, 0)
        # Déclaration d'un bouton z_out (zoom out)
        self.z_out = QPushButton(self)
        # Définition du texte du bouton
        self.z_out.setText("-")
        # Relie le signal à la méthode zoom_out
        self.z_out.clicked.connect(self.zoom_out)
        # On ajoute z_out au layout zoom
        self.zoom.addWidget(self.z_out, 1, 1)
        # On ajoute un peu d'espace entre tour_par_tour et zoom
        self.menu_layout.addSpacing(20)
        # On ajoute zoom au layout du menu
        self.menu_layout.addLayout(self.zoom)

        # On ajoute menu_layout au layout principal
        self.affichage.addLayout(self.menu_layout)

        """
        Augmenter le nombre de cellule (pour dessiner un truc plus gros)
        Intéragir avec les cellule (mode edition et simulation)
        """

        # Affiche la fenêtre
        self.show()

    def enregistrer(self) -> None:
        """
        Entrée:
            self: JeuDeLaVieApp
        Sortie:
            None (modification en place)
        Rôle:
            Enregistre self.scene dans le format csv
        """
        # Si un fichier est "ouvert"
        if self.est_fichier_ouvert:
            
            # On ouvre le fichier (s'il n'existe plus, il est recréé)
            with open(self.fichier, 'w', encoding='utf-8') as f:
                # Récupère le plateau avec 1 pour vivant et 0 pour mort
                plateau: list[list[str]] = self.scene.get_plateau("1", "0")
                # Pour chaque ligne
                for i in range(len(plateau)):
                    # Pour chaque élément
                    for j in range(len(plateau[i])):
                        # On écrit l'élément
                        f.write(plateau[i][j])
                        # Si l'élément n'est pas le dernier
                        if j < len(plateau[i]) - 1:
                            # on écrit une virgule
                            f.write(",")
                    # Ecriture d'un retour chariot
                    f.write("\n")
                # Fermeture du fichier
                f.close()
        # S'il n'y a pas de fichier ouvert
        else:
            # Appelle la méthode enregistrer_sous
            self.enregistrer_sous()

    def enregistrer_sous(self) -> None:
        """
        Entrée:
            self: JeuDeLaVieApp
        Sortie:
            None (modification en place)
        Rôle:
            Enregistre sous self.scene dans le format csv
        """
        # Déclaration d'un nouveau QFileDialog
        enregistrer_fichier = QFileDialog(self, caption="Enregistrer sous")
        # Définition du type de fichier attendu
        enregistrer_fichier.setNameFilter("Templates (*.csv)")
        # Définition du filtre
        enregistrer_fichier.setFilter(
            QDir.Filter.Readable | QDir.Filter.Files | QDir.Filter.NoSymLinks)
        # Définition du mode du fichier sur fichier existant
        enregistrer_fichier.setFileMode(QFileDialog.FileMode.ExistingFile)
        # Définition du suffix par défaut
        enregistrer_fichier.setDefaultSuffix(".csv")
        # Définition du mode
        enregistrer_fichier.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        
        # Si l'utilisateur sélectionne un fichier
        if enregistrer_fichier.exec():
            # On met à jour l'attribut est_fichier_ouvert
            self.est_fichier_ouvert = True
            # Mise à jour du nom du fichier
            self.fichier = enregistrer_fichier.selectedFiles()[0]
            # On enregistre le template
            self.enregistrer()
    
    def importe(self) -> None:
        """
        Entrée:
            self: JeuDeLaVieApp
        Sortie:
            None (modification en place)
        Rôle:
            Importe un template d'un fichier csv.
        """
        # Déclaration d'un nouveau QFileDialog
        obtenir_fichier = QFileDialog(self, caption="Importer un template")
        # Définition du type de fichier attendu
        obtenir_fichier.setNameFilter("Templates (*.csv)")
        # Définition du filtre
        obtenir_fichier.setFilter(
            QDir.Filter.Readable | QDir.Filter.Files | QDir.Filter.NoSymLinks)
        # Définition du mode du fichier sur fichier existant
        obtenir_fichier.setFileMode(QFileDialog.FileMode.ExistingFile)
        # Définition du suffix par défaut
        obtenir_fichier.setDefaultSuffix(".csv")
        # Définition du mode
        obtenir_fichier.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        
        # Si l'utilisateur sélectionne un fichier
        if obtenir_fichier.exec():
            # Récupère le chemin du fichier
            fichier = obtenir_fichier.selectedFiles()[0]

            # On ouvre le fichier en mode lecture
            with open(file=fichier, mode='r', encoding='utf8') as f:
                # On extrait les données
                donnees = f.readlines()
                # On ferme le fichier
                f.close()
            
            # On teste la validité des données
            tableau_valide, message_erreur = est_template_valide(donnees)

            # si le tableau est valide
            if tableau_valide:
                # On arrêtre l'animation (economie de ressources)
                self.stop_anim()
                # Déclaration d'une matrice vide
                matrice = []
                # Pour chaque ligne
                for i, ligne in enumerate(reader(donnees)):
                    # On ajoute une nouvelle ligne à la matrice
                    matrice.append([])
                    # Pour chaque élément de la ligne
                    for element in ligne:
                        # On ajoute l'élément converti en int
                        matrice[i].append(int(element))
                # On définit le plateau selon la matrice, sachant que l'élément 
                # vivant est 1
                self.scene.set_plateau(matrice, 1)
                # Remet le nombre de cycle à 0
                self.nb_cycle = 0
                # Modifie le texe du label
                self.affichage_cycle.setText("Cycle n°" + str(self.nb_cycle))
                # On met à jour l'attribut est_fichier_ouvert
                self.est_fichier_ouvert = True
                # Mise à jour du nom du fichier
                self.fichier = fichier
            # Si le tableau n'est pas valide
            else:
                # Affichage du message d'erreur
                QMessageBox.warning(
                    self, "Erreur", message_erreur, 
                    QMessageBox.StandardButton.Ok, 
                    QMessageBox.StandardButton.Ok)
    
    def set_auto_grandissement(self, etat: Qt.CheckState) -> None:
        """
        Entrées:
            self: JeuDeLaVieApp
            etat: Qt.CheckState
        Sortie:
            None (modification en place)
        Rôle:
            Redéfinit la valeur de auto_grandissement selon etat
        """
        # | etat             | etat.value
        # | Unchecked        | 0
        # | Checked          | 2
        # bool(0) -> False, bool(1) -> True
        # Attribut une nouvelle valeur à auto_grandissement
        self.scene.auto_grandissement = bool(etat.value)
    
    def lance_anim(self) -> None:
        """
        Entrées:
            self: JeuDeLaVieApp
        Sortie:
            None (modification en place)
        Rôle:
            Lance l'animation
        """
        # désactive le bouton play
        self.play.setEnabled(False)
        # active le bouton pause
        self.pause.setEnabled(True)
        # On enlève focus de periode_entree, puisqu'en se désactivant, le play
        # lui donne le focus
        self.periode_entree.clearFocus()

        # Démarre le chrono pour un temps indéterminé
        self.chrono.start()
        # Executre le premier tour
        self.execute_tour()
    
    def execute_tour(self) -> None:
        """
        Entrées:
            self: JeuDeLaVieApp
        Sortie:
            None (modification en place)
        Rôle:
            Execute un tour
        """
        # Mise à jour de l'interval de temps
        self.chrono.setInterval(int(self.periode_entree.value() * 1000))
        # Execute un tour
        self.scene.tour()

    def stop_anim(self):
        """
        Entrées:
            self: JeuDeLaVieApp
        Sortie:
            None (modification en place)
        Rôle:
            Pause l'animation
        """
        # Arrête le chrono
        self.chrono.stop()
        # active le bouton play
        self.play.setEnabled(True)
        # désactive le bouton pause
        self.pause.setEnabled(False)
        # On enlève focus de periode_entree, puisqu'en se désactivant, le pause
        # lui donne le focus
        self.periode_entree.clearFocus()
    
    def zoom_in(self) -> None:
        """
        Entrées:
            self: JeuDeLaVieApp
        Sortie:
            None (modification en place)
        Rôle:
            Zoom dans la vue
        """
        # Augmente les grandeurs de 10%
        self.vue.scale(1.1, 1.1)

    def zoom_out(self) -> None:
        """
        Entrées:
            self: JeuDeLaVieApp
        Sortie:
            None (modification en place)
        Rôle:
            Dézoom dans la vue
        """
        # Diminue les grandeurs de 10%
        self.vue.scale(0.9, 0.9)


# Si le présent fichier est executé
if __name__ == '__main__':
    # On instantie QApplication en lui passe argv (héritage du c++)
    app = QApplication(argv)
    # On instantie JeuDeLaVieApp
    my_window = JeuDeLaVieApp()

    # On execute l'application
    app.exec()
