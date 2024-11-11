# importe util depuis importlib
from importlib import util

# Si le module PySide6 n'est pas installé
if not util.find_spec("PySide6"):
    # Questionne l'utilisateur sur sa volonté d'installer PySide6
    reponse = input("Le module PySide6 n'est pas installé, souhaitez-vous " + 
                    "l'installer automatiquement ? (o/n)")[0]
    # Si la réponse est o (pour oui)
    if reponse.lower() == "o":
        # import run et PIPE du module subprocess
        from subprocess import run, PIPE
        # Affichage d'un message pour que l'utilisateur patiente
        print("Intallation de PySide6, cela peut prendre quelques minutes. " + 
            "Merci de ne pas intérompre le processus.")
        # Installation de PySide6
        proc = run("pip install PySide6", stdout=PIPE)
        # Affiche le flux de sortie du terminal 
        print(proc.stdout.decode())
        # Si le code de sortie n'est pas 0
        if proc.returncode:
            # Affichage d'un message d'erreur
            print("Une erreur est intervenue, merci de la corriger avant de " +
                  "relancer le programme")
            # Termine le processus avec proc.returncode en code de sortie
            exit(proc.returncode)
    # Si le message d'erreur est n (pour n) ou autre
    else:
        # Affiche un message à l'utilisateur
        print("Le programme ne peut démarrer tant que PySide6 n'est pas " + 
              "installé")
        # Termine le processus avec 1 en code de sortie
        exit(1)

# Importe les classes utilisées depuis PySide6.QtWidgets
from PySide6.QtWidgets import QMainWindow, QApplication, QGraphicsView, \
    QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QDoubleSpinBox, QLabel, \
    QGridLayout, QCheckBox, QFileDialog, QMessageBox, QFrame, QSizePolicy
# Importe les classes utilisées depuis PySide6.QtGui
from PySide6.QtGui import QIcon, QAction, QKeySequence, QStatusTipEvent
# Importe les classes utilisées depuis PySide6.QtCore
from PySide6.QtCore import Qt, QSize,  QDir, QEvent
# Importe reader depuis le module csv
from csv import reader
# Importe argv, version_info depuis le module sys
from sys import argv, version_info
# Importe est_template_valide du module plateau de dependances.plateau
from dependances.plateau import est_template_valide
# Importe Scene du module plateau de dependances.jdlv_ui
from dependances.jdlv_ui import Scene
# Importe basename depuis le module os.path
from os.path import basename


class JeuDeLaVieGUI(QMainWindow):
    """
    Hérite de:
        QMainWindow
    Rôle:
        Représente l'application du jeu de la vie
    """
    def __init__(self) -> None:
        """
        Entrée:
            self: JeuDeLaVieGUI
        Sortie:
            None (ctor)
        Rôle:
            Construit un nouvel objet JeuDeLaVieGUI
        """
        # Initialisation de la classe mère
        QMainWindow.__init__(self)

        # Attributs
        
        # Déclaration de chemin_absolu pour accéder aux ressources (svg, ...)
        self.chemin_absolu = __file__[:-len(basename(__file__))]
        # Déclaration d'un booléan est_fichier_ouvert
        self.est_fichier_ouvert: bool = False
        self.fichier: str = ""
        # Déclaration d'un attribut nb_cycle
        self.nb_cycle: int = 0

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

        # Déclaration de enregistrer_template_sous
        self.enregistrer_template_sous = QAction(self)
        # Définition du texte de enregistrer_template
        self.enregistrer_template_sous.setText("Enregistrer le template")
        # Définition d'un raccourci clavier
        self.enregistrer_template_sous.setShortcut(
            QKeySequence.StandardKey.SaveAs)
        # Relie le signal à la méthode enregistrer
        self.enregistrer_template_sous.triggered.connect(self.enregistrer_sous)
        # Ajoute l'action au menu
        self.menu_fichier.addAction(self.enregistrer_template_sous)

        # Scène - vue

        # On créer une scène du jeu de la vie
        self.scene = Scene(self, QSize(10, 10))
        # On créer une vue
        self.vue = QGraphicsView(self)
        # Définition d'un conseil pour l'utilisateur
        self.vue.setStatusTip(
            "Scène du jeu de la vie. Vous pouvez zommer, vous y déplacer et " + 
            "modifier l'état des cellules en cliquant dessus")
        self.vue.enterEvent
        # On dit à la vue quelle scène afficher
        # Fonctionnement -> https://doc.qt.io/qt-6/graphicsview.html
        self.vue.setScene(self.scene)
        # On définit l'échelle (fonctionne par pourcentage d'agrandissement)
        self.vue.scale(0.5, 0.5)
        # On ajoute la vue au layout principal
        self.affichage.addWidget(self.vue)

        # Bar d'outils

        # Déclaration d'un layout vertical outils_layout, layout ≃ div en html
        self.outils_layout = QVBoxLayout()
        # On définit les options d'alignement du layout
        self.outils_layout.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        # On ajoute outils_layout au layout principal
        self.affichage.addLayout(self.outils_layout)

        # Déclaration d'un label
        self.affichage_cycle = QLabel(self)
        # Définition d'un conseil pour l'utilisateur
        self.affichage_cycle.setStatusTip("Compte le nombre de cycle effectué")
        # Modifie le texe du label
        self.affichage_cycle.setText("Cycle n°" + str(self.nb_cycle))
        # Définit l'alignement du texte
        self.affichage_cycle.setAlignment(Qt.AlignmentFlag.AlignRight)
        # Ajoute le label dans le layout
        self.outils_layout.addWidget(self.affichage_cycle)
        # On ajoute un peu d'espace entre le haut de la fenêtre et les boutons
        self.outils_layout.addSpacing(20)
        
        # Déclaration d'un label
        self.controles_titre = QLabel(self)
        # Définition d'un conseil pour l'utilisateur
        self.controles_titre.setStatusTip("Contrôle du jeu de l'animation.")
        # Définitons du texte du label
        self.controles_titre.setText("Contrôles :")
        # Définition du style du texte et de sa taille
        self.controles_titre.setStyleSheet("font-style: bold; font-size: 11pt;")
        # Ajoute le titre à outils_layout
        self.outils_layout.addWidget(self.controles_titre)
        # Déclaration d'un layout horizontal play/pause
        self.controles_layout = QHBoxLayout()
        # Déclaration d'un bouton play
        self.play = QPushButton(self)
        # Définition d'un conseil pour l'utilisateur
        self.play.setStatusTip("Joue l'animation.")
        # Définition de l'icone de play
        icone_play = QIcon(self.chemin_absolu + 
                           "assets\\icones\\play-button.svg")
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
        # Définition d'un conseil pour l'utilisateur
        self.pause.setStatusTip("Pause l'animation")
        # Définition de l'icone de pause
        icone_pause = QIcon(self.chemin_absolu + 
                            "assets\\icones\\pause-button.svg")
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
        # On ajoute controles_layout à outils_layout
        self.outils_layout.addLayout(self.controles_layout)
        
        # Déclaration du bouton tour par tour
        self.tour_par_tour = QPushButton(self)
        # Définition d'un conseil pour l'utilisateur
        self.tour_par_tour.setStatusTip("Exécute un tour de l'animation")
        # On définit le texte à afficher
        self.tour_par_tour.setText("Tour par tour")
        # Relie le signal à la méthode tour de la scène
        self.tour_par_tour.clicked.connect(self.scene.tour)
        # On ajoute tour_par_tour au layout du menu
        self.outils_layout.addWidget(self.tour_par_tour)
        # Ajoute de l'espace après

        # Déclaration de periode_layout
        self.periode_layout = QGridLayout()
        # Déclaration de periode_label
        self.periode_label = QLabel(self)
        # Définition d'un conseil pour l'utilisateur
        self.periode_label.setStatusTip(
            "La période est la durée d'un cycle de l'animation.")
        # Définition du texte de periode_label
        self.periode_label.setText("Durée d'une période :")
        # Déclaration de periode_entree
        self.periode_entree = QDoubleSpinBox(self)
        # Définition d'un conseil pour l'utilisateur
        self.periode_entree.setStatusTip(
            "Une période trop courte peut causer des ralentissements.")
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
        # Relie le signal à la méthode set_periode
        self.periode_entree.valueChanged.connect(self.set_periode)
        # Ajoute periode_label dans la cellule (0;0) du layout
        self.periode_layout.addWidget(self.periode_label, 0, 0)
        # Ajoute periode_entree dans la cellule (0;1) du layout
        self.periode_layout.addWidget(self.periode_entree, 0, 1)
        # Ajoute periode_layout à outils_layout
        self.outils_layout.addLayout(self.periode_layout)
        # Ajoute de l'espace après
        self.outils_layout.addSpacing(7)
        # Déclaration d'une ligne de séparation
        self.ligne_post_controles = QFrame(self)
        # Définition de la forme
        self.ligne_post_controles.setFrameShape(QFrame.Shape.HLine)
        # Définiton des ombres
        self.ligne_post_controles.setFrameShadow(QFrame.Shadow.Sunken)
        # Ajoute la ligne à outils_layout
        self.outils_layout.addWidget(self.ligne_post_controles)
        # Ajoute de l'espace après
        self.outils_layout.addSpacing(7)

        # Déclaration d'une case à cocher
        self.auto_grandissement_entree = QCheckBox(self)
        # Définition d'un conseil pour l'utilisateur
        self.auto_grandissement_entree.setStatusTip("Quand est cochée, " + 
            "agrandit le plateau pour s'adapter à l'animation")
        # Définition du texte de la case à cocher
        self.auto_grandissement_entree.setText("Auto grandissement")
        # On définit son état sur coché
        self.auto_grandissement_entree.setCheckState(Qt.CheckState.Checked)
        # Relie le signal à la fonction set_auto_grandissement
        self.auto_grandissement_entree.checkStateChanged.connect(
            self.set_auto_grandissement)
        # On ajoute la case à cocher au layout
        self.outils_layout.addWidget(self.auto_grandissement_entree)

        # Déclaration d'une case à cocher
        self.auto_stop_entree = QCheckBox(self)
        # Définition d'un conseil pour l'utilisateur
        self.auto_stop_entree.setStatusTip(
            "Quand est cochée, arrête automatiquement l'animation quand il " + 
            "n'y a plus de changement.")
        # Définition du texte de la case à cocher
        self.auto_stop_entree.setText("Auto stop")
        # On définit son état sur coché
        self.auto_stop_entree.setCheckState(Qt.CheckState.Checked)
        # Relie le signal à la fonction set_auto_stop
        self.auto_stop_entree.checkStateChanged.connect(
            self.set_auto_stop)
        # On ajoute la case à cocher au layout
        self.outils_layout.addWidget(self.auto_stop_entree)
        # Ajoute de l'espace après
        self.outils_layout.addSpacing(7)
        # Déclaration d'une ligne de séparation
        self.ligne_post_autos = QFrame(self)
        # Définition de la forme
        self.ligne_post_autos.setFrameShape(QFrame.Shape.HLine)
        # Définiton des ombres
        self.ligne_post_autos.setFrameShadow(QFrame.Shadow.Sunken)
        # Ajoute la ligne à outils_layout
        self.outils_layout.addWidget(self.ligne_post_autos)
        # Ajoute de l'espace après
        self.outils_layout.addSpacing(7)

        # Déclaration d'un layout horizontal
        self.zoom = QGridLayout()
        # Déclaration d'un label zoom
        self.zoom_label = QLabel(self)
        # Définitions du text du label
        self.zoom_label.setText("Zoom :")
        # Définition du style du texte et de sa taille
        self.zoom_label.setStyleSheet("font-style: bold; font-size: 11pt;")
        # Définition d'un conseil pour l'utilisateur
        self.zoom_label.setStatusTip("Interface de zoom")
        # On ajoute zoom_label dans la cellule (0;0) sur un espace de 1 ligne
        # et 2 colonnes
        self.zoom.addWidget(self.zoom_label, 0, 0, 1, 2)
        # Déclaration d'un bouton z_in (zoom in)
        self.z_in = QPushButton(self)
        # Définition d'un conseil pour l'utilisateur
        self.z_in.setStatusTip("Zoom dans la scène")
        # Définition du texte du bouton
        self.z_in.setText("+")
        # Relie le signal à la méthode zoom_in
        self.z_in.clicked.connect(self.zoom_in)
        # On ajoute z_in au layout zoom
        self.zoom.addWidget(self.z_in, 1, 0)
        # Déclaration d'un bouton z_out (zoom out)
        self.z_out = QPushButton(self)
        # Définition d'un conseil pour l'utilisateur
        self.z_out.setStatusTip("Dézoom dans la scène")
        # Définition du texte du bouton
        self.z_out.setText("-")
        # Relie le signal à la méthode zoom_out
        self.z_out.clicked.connect(self.zoom_out)
        # On ajoute z_out au layout zoom
        self.zoom.addWidget(self.z_out, 1, 1)
        # On ajoute zoom au layout du menu
        self.outils_layout.addLayout(self.zoom)
        # On ajoute de l'étirement qui à pour effet de prendre le plus de place
        # possible, ainsi, les prochains éléments seront le plus bas possible
        self.outils_layout.addStretch()

        # Déclaration d'un titre pour bar_info
        self.bar_info_titre = QLabel(self)
        # Définition du texte
        self.bar_info_titre.setText("Vue Info :")
        # Définition du style du texte et de sa taille
        self.bar_info_titre.setStyleSheet("font-style: bold; font-size: 11pt;")
        # Ajoute le titre à outils_layout
        self.outils_layout.addWidget(self.bar_info_titre)        
        # Déclaration de bar_info
        self.bar_info = QLabel(self)
        # Définit la taille minimum de bar_info en hauteur
        self.bar_info.setMinimumHeight(175)
        # On précise les marges du texte
        self.bar_info.setMargin(10)
        # Déclaration d'une Politique de taille et d'agrandissement
        bar_info_policy = QSizePolicy()
        # Spécifit que les demandes agrandissement sont ignorées
        # demandes effectuées à cause des marges
        bar_info_policy.setHorizontalPolicy(QSizePolicy.Policy.Ignored)
        # Attribution de la politique de taille à bar_info
        self.bar_info.setSizePolicy(bar_info_policy)
        # Définiton de l'attribut wordwrap sur True, pour les retous à la ligne
        self.bar_info.setWordWrap(True)
        # Précision de l'alignement du texte en haut à gauche
        self.bar_info.setAlignment(Qt.AlignmentFlag.AlignLeft | 
                                   Qt.AlignmentFlag.AlignTop)
        # Définition de la taille du texte
        self.bar_info.setStyleSheet("font-size: 10.5pt;")
        # Définition du format du texte comme étant Markdown
        self.bar_info.setTextFormat(Qt.TextFormat.MarkdownText)
        # Sélection du style du cadre (classe mère que QLabel)
        self.bar_info.setFrameStyle(QFrame.Shape.StyledPanel)
        # Définition du statusTip (Cf méthode event)
        self.bar_info.setStatusTip(
            "La *Vue Info* fournit une brève description de l'élément " +
            "de l'interface utilisateur sur lequel la souris se trouve " + 
            "actuellement.")
        # Ajoute bar_info à outils_layout
        self.outils_layout.addWidget(self.bar_info)

        # Initialisation de toutes les variables reliées aux champs d'entrées
        
        # Initialise auto_grandissement sur l'état de la case à cocher
        self.scene.auto_grandissement = bool(
            self.auto_grandissement_entree.checkState().value)
        # Initialise auto_stop sur l'état de la case à cocher
        self.scene.auto_stop = bool(self.auto_stop_entree.checkState().value)
        # Initialise periode sur la valeur de periode_entree
        self.scene.periode = int(self.periode_entree.value() * 1000)

        # Affiche la fenêtre
        self.show()
    
    def event(self, even: QEvent) -> bool:
        """
        Réimplémentation de event hérité de QMainWindow
        Entrées:
            self: JeuDeLaVieGUI
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
            # Définit le texte de bar_info sur le conseil de l'évènement
            self.bar_info.setText(even.tip())
            """
            Fonctionnement:
            Chaque objet possédant l'attribut statusTip émet un signal 
            QStatusTipEvent lorsque la souris le survole. Ce signal comporte un
            tip, un conseil, concernant le dit objet. Il est par défaut 
            réceptionné par statusBar de QMainWindow, mais il peut être 
            intercepté et affiché autre part.
            """
        
        # On rend l'évènement
        return super().event(even)

    def enregistrer(self) -> None:
        """
        Entrée:
            self: JeuDeLaVieGUI
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
            # On prévient l'utilisateur que le fichier a été enregistré
            self.event(QStatusTipEvent("Le fichier a été enregistré !"))
        # S'il n'y a pas de fichier ouvert
        else:
            # Appelle la méthode enregistrer_sous
            self.enregistrer_sous()

    def enregistrer_sous(self) -> None:
        """
        Entrée:
            self: JeuDeLaVieGUI
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
            self: JeuDeLaVieGUI
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
                tableau = []
                # Pour chaque ligne
                for i, ligne in enumerate(reader(donnees)):
                    # On ajoute une nouvelle ligne à la matrice
                    tableau.append([])
                    # Pour chaque élément de la ligne
                    for element in ligne:
                        # On ajoute l'élément converti en int
                        tableau[i].append(int(element))
                # On définit le plateau selon la matrice, sachant que l'élément 
                # vivant est 1
                self.scene.set_plateau(tableau, 1)
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
            self: JeuDeLaVieGUI
            etat: Qt.CheckState
        Sortie:
            None (modification en place)
        Rôle:
            Redéfinit la valeur de auto_grandissement selon etat
        """
        # | etat             | etat.value
        # | Unchecked        | 0
        # | Checked          | 2
        # bool(0) -> False, bool(2) -> True
        # Attribut une nouvelle valeur à auto_grandissement
        self.scene.auto_grandissement = bool(etat.value)
    
    def set_auto_stop(self, etat: Qt.CheckState) -> None:
        """
        Entrées:
            self: JeuDeLaVieGUI
            etat: Qt.CheckState
        Sortie:
            None (modification en place)
        Rôle:
            Redéfinit la valeur de auto_stop selon etat
        """
        # | etat             | etat.value
        # | Unchecked        | 0
        # | Checked          | 2
        # bool(0) -> False, bool(1) -> True
        # Attribut une nouvelle valeur à auto_stop
        self.scene.auto_stop = bool(etat.value)
    
    def set_periode(self, valeur: float) -> None:
        """
        Entrées:
            self: JeuDeLaVieGUI
            valeur: double
        Sortie:
            None (modification en place)
        Rôle:
            
        """
        self.scene.periode = int(valeur * 1000)
    
    def lance_anim(self) -> None:
        """
        Entrées:
            self: JeuDeLaVieGUI
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
        self.scene.chrono.start()
        # Executre le premier tour
        self.scene.execute_tour()

    def stop_anim(self):
        """
        Entrées:
            self: JeuDeLaVieGUI
        Sortie:
            None (modification en place)
        Rôle:
            Pause l'animation
        """
        # Arrête le chrono
        self.scene.chrono.stop()
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
            self: JeuDeLaVieGUI
        Sortie:
            None (modification en place)
        Rôle:
            Zoom dans la vue
        Apostille:
            Le nom est en anglais car le terme n'existe pas en français.
        """
        # Augmente les grandeurs de 10%
        self.vue.scale(1.1, 1.1)

    def zoom_out(self) -> None:
        """
        Entrées:
            self: JeuDeLaVieGUI
        Sortie:
            None (modification en place)
        Rôle:
            Dézoom dans la vue
        Apostille:
            Le nom est en anglais car le terme n'existe pas en français.
        """
        # Diminue les grandeurs de 10%
        self.vue.scale(0.9, 0.9)


# Si le présent fichier est executé avec python 3.10 ou plus
if __name__ == "__main__" and version_info >= (3, 10):
    # On instantie QApplication en lui passe argv (héritage du c++)
    app = QApplication(argv)
    # On instantie JeuDeLaVieGUI
    my_window = JeuDeLaVieGUI()

    # On execute l'application
    app.exec()
