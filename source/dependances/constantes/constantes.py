# Import Enum depuis enum
from enum import Enum


class Etat(Enum):
    """
    Hérite de:
        Enum
    Rôle:
        Abstaitiste les états de la cellule pour simplifier la lecture du code
    """
    # Déclaration de Vivant
    Vivant = True
    # Déclaration de Mort
    Mort = False


class Direction(Enum):
    """
    Hérite de:
        Enum
    Rôle:
        Abstaitiste les directions pour simplifier la lecture du code
    """
    # Déclaration de Nord
    Nord = 0
    # Déclaration de Est
    Est = 1
    # Déclaration de Sud
    Sud = 2
    # Déclaration de Ouest
    Ouest = 3