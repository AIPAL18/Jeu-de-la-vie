# Dérivé de pythonlangutil.overload
# https://github.com/ehsan-keshavarzian/pythonlangutil/blob/master/pythonlangutil/overload.py

# Importe Any depuis typing
from typing import Any


def signature(*types) -> callable:
    """
    Entrée(s):
        types: str
    Sortie:
        callable
    Rôle:
        Retourne la fonction dont signature est un décorateur avec une 
        propriété signature qui est un tuple des types
    Addendum:
        Mes excuses pour les explications et commentaires, mais le code n'étant 
        pas le mien, non commenté et parfois hors de ma porté, il a été 
        complexe à comprendre. La notion de décoration en python n'est déjà pas
        facile à implémenter, alors à mettre en oeuvre, c'est une autre 
        histoire.
    """
    def func(f: callable) -> callable:
        """
        Entrée:
            f: callable (fonction qui est décorée)
        Sortie:
            callable
        Rôle:
            Retourne la fonction dont signature est un décorateur avec une 
            propriété signature qui est un tuple des types
        """
        def inner_func(callingObj, *args, **kwargs) -> callable:
            """
            Entrées:
                callingObj: self (puisque f est une méthode Cf Overload)
                *args: arguments passé à f lors de son appelle
                **kwargs: couples (clé;argument) passé à f lors de son appelle
            Sortie:
                Sortie de f(callingObj, *args, **kwargs)
            Rôle:
                Retourne la valeur de f(callingObj, *args, **kwargs)
            """
            # retourne la valeur de retour de f, la fonction décorée, en lui 
            # passant en paramètre les arguments qui lui sont passés en 
            # paramètre
            return f(callingObj, *args, **kwargs)
        
        # Créer une propriété signature pour la fonction décorée et lui assigne
        # le tuple de types
        inner_func.signature = types  # types -> tuple

        # retourn l'objet inner_func
        return inner_func
    
    # retourne l'objet func
    return func


def get_signature_complete(obj, sig: tuple = ()) -> tuple[str]:
    """
    Entrées:
        obj: Any
            obj est une variable quelconque
        sig: tuple
            signature de obj jusqu'alors
    Sortie:
        tuple[str]
    Rôle:
        Retourne l'arbre de signature de obj
    Exemple:
        >>> a: int = 1
        >>> get_inherited_signature(a)
        ['int', 'object']
    Explications:
        Le but de cette fonction est de savoir de quelleS classeS hérite obj.
        Plus obj est abstrait, plus sont arbre de signature sera grand.
        L'arbre ne possède qu'une dimension pour facilité son traitement.
    Addendum:
        Cette fonction est la raison pour laquelle j'ai recodé ce module.
        Ce dernier ne permet pas de faire de surcharge 'intelligente'.
        Il est évident les parmatères suivants de type:
            list, int, int
        correspond à la signature suivante:
            list, int, object
        car int hérite de object. Or l'héritage doit respecter le principe de 
        substitution de Liskov.
    """
    # Si c'est le premier appelle
    if len(sig) == 0:
        # On redéfinit obj par sa classe
        obj = obj.__class__
        # on attribut le singleton du nom de la classe d'obj à sig
        sig = (obj.__name__,)
        # On retourne get_inherited_signature(obj, sig)
        return get_signature_complete(obj, sig)
    # Si obj est object
    elif obj.__name__ == object.__name__:
        # On retourne la signature complète plus object
        return sig + (obj.__name__,)
    # Sinon
    else:
        # parent_sig est initialisé avec les classes directement parentes d'obj
        parent_sig = obj.__bases__
        # Si obj à plus d'un parent directe
        if type(parent_sig) is tuple:
            # Pour chaque parent
            for par in parent_sig:
                # Si le parent est object
                if par.__name__ == object.__name__:
                    # on ajoute ('object',) à sig
                    sig += (par.__name__,)
                # Sinon
                else:
                    # on ajoute l'arbre de signature du parent 
                    sig += get_signature_complete(par, (par.__name__,))
            # On retourne l'arbre de signature de obj
            return sig
        # Si sig n'a qu'un parent directe
        else:
            # On retourne sig plus son type plus son arbre de signature
            return sig  + (obj.__name__,) + (
                get_signature_complete(parent_sig, sig),)


class Overload(object):
    """
    Hérite de:
        object
    Rôle:
        Permet de surcharger une (uniquement) méthode (uniquement) et met en 
        oeuvre le principe de substitution de Liskov.
    Exemple:
        >>> @Overload  # (il est préférable de l'utiliser en décorateur)
        >>> @signature(int)  # (obligatoire !!!)
        >>> def double(valeur: int) -> int:
        >>>     return int(valeur * 2)
        >>> @double.overload  # Pas de majuscule à overload
        >>> @signature(float)  # (obligatoire !!!)
        >>> def double(valeur: float) -> float:
        >>>     return float(valeur * 2)
        >>> double(.2)  # .2 est de type float
        0.4  # float
        >>> double(5)  # 5 est de type int
        10  # int
    Addendum:
        Overload est dérivée, comme signature, de pythonlangutil.overload donc
        les variables sont en englais.
    """
    def __init__(self, func: callable) -> None:
        """
        Entrées:
            self: Overload
            func: callable (fonction à surcharger)
        Sortie:
            None (ctor)
        Rôle:
            Construit un nouvel objet Overload
        """
        # Déclaration de l'attribut owner pour la méhtode magique __get__
        self.owner = None
        # Déclaration d'une liste de tuple où les tuples sont les signatures 
        # des méthodes qui se surchargent
        self.signatures: list[tuple] = []
        # Liste des méthodes qui se surchargent
        self.methods: list[callable] = []
        # On ajoute la méthode surchargée à methods
        self.methods.append(func)
        # On ajoute la signature de la méthode à signatures
        self.signatures.append(func.signature)
        
    def __get__(self, owner: object | None, ownerType: Any = None) -> object:
        """
        Entrée:
            self: Overload
            owner: object | None
            owerType: None | Any
        Sortie:
            Overload
        Rôle:
            Retourne l'objet Overload et définit l'attribut owner.
        Description:
    https://python-reference.readthedocs.io/en/latest/docs/dunderdsc/get.html
        """
        # owner n'est pas définit, self.owner = self, sinon, self.owner = owner
        self.owner = owner or self

        # retourne l'objet Overload
        return self
    
    def __call__(self, *args, **kwargs):
        """
        Entrée:
            self: Overload
            args: Any  (arguments passés à la fonction surchargée)
            kwargs: Any (couples (clé;arg) passés à la fonction surchargée)
        Sortie:
            Résultat de la fonction surchargé qui correspond à la signature des 
            arguments passés en paramètre.
        Rôle:
            Trouve la fonction correspondant à la signature des arguments 
            passés en paramètre, l'execute et retourne sa valeur de retour.
        """
        # Signature des arguments
        signature = []
        # Pour chaque argument sans clé
        for arg in args:
            # On ajoute le type des arguments sans clé
            signature.append(arg.__class__.__name__)
        # Pour chaque clé (_), argument (v)
        for _, v in kwargs:
            # On ajoute le type des arguments qui ont une clé
            signature.append(v.__class__.__name__)
        # Signature doit être un tuple car les signatures sont stockée sous 
        # forme de tuple
        signature = tuple(signature)
        # si la signature exacte est enregistrée
        if signature in self.signatures:
            # On trouve l'indice correspondant à cet signature
            index = self.signatures.index(signature)
        # si la signature exacte est n'est pas enregistrée
        else:
            # extrait l'arbre d'héritage pour chaque argument de la signature
            inherited_signature = []
            # Pour chaque argument sans clé
            for arg in args:
                # On ajoute l'arbre d'héritage des arguments sans clé
                inherited_signature.append(get_signature_complete(arg))
            # Pour chaque clé (_), argument (v)
            for _, v in kwargs:
                # On ajoute l'arbre d'héritage des arguments qui ont une clé
                signature.append(get_signature_complete(v))
            
            # signature éligibles
            sig_eligibles = []
            # Pour chaque signature des signatures enregistrées
            for sig in self.signatures:
                # Si son nombre d'argument correspond à la signature des args
                if len(inherited_signature) == len(sig):
                    # On l'ajoute aux signature éligibles
                    sig_eligibles.append(sig)
            
            # Index négatif -> erreur
            index = -1
            # Variable d'arrêt, False s'il n'y a pas de signature éligible
            existe = len(sig_eligibles) > 0  # bool
            # Itérateur i
            i = 0
            # Pour chaque signature
            while i < len(sig_eligibles) and existe:
                # Itérateur j
                j = 0
                # Variable d'arrêt de la seconde boucle
                correspond = True
                # Pour chaque type de la signature
                while j < len(sig_eligibles[i]) and correspond:
                    # Si le type n'est pas dans les type hérité du paramètre
                    # c'est que ce n'est pas le bon type
                    if sig_eligibles[i][j] not in inherited_signature[j]:
                        # On stop la boucle
                        correspond = False
                    # Incrémentation de l'itérateur
                    j += 1
                # Si la signature correspond
                if correspond:
                    # On recherche l'indice car la signature est unique 
                    # (cf self.overload)
                    index = self.signatures.index(sig_eligibles[i])
                # Incrémentation de l'itérateur
                i += 1
            # Si la signature ne correspond à aucune des méthodes enregistrées
            if not existe or index < 0:
                # On lève une exception
                raise Exception("There is no overload for this method with " + 
                                "this signature.")
        
        # On execute la méthode avec ses arguments et on retourne sa valeur de 
        # retour
        return self.methods[index](self.owner, *args, **kwargs)
    
    def overload(self, func: callable):
        """
        Entrée:
            self: Overload
            func: callable
        Sortie:
            Overload
        Rôle:
            Ajoute une nouvelle surcharge
        Explications:
            Faire:
            >>> @Overload
            >>> @signature(int)
            >>> def double(valeur: int) -> int:
            >>>     return int(valeur * 2)
            C'est faire:
            >>> def double(valeur: int) -> int:
            >>>     return int(valeur * 2)
            >>> double = signature('int', double)
            >>> double = Overload(double)

            Donc quand on fait
            >>> @double.overload  # appelle la méthode overload
            >>> @signature(float)
            >>> def double2(valeur: float) -> float:
            >>>     return float(valeur * 2)
            On fait:
            >>> def double2(valeur: float) -> float:
            >>>     return float(valeur * 2)
            >>> double2 = signature(double2)
            >>> double2 = double.overload(double2)# appelle la méthode overload
            En pratique, il ne faut pas changer le nom de la méthode quand on 
            la surcharge.

            https://www.geeksforgeeks.org/decorators-in-python/
        """
        # Si la signature est unique
        if func.signature not in self.signatures:
            # On ajoute la méthode à methods
            self.methods.append(func)
            # On ajoute la signature de func à signatures
            self.signatures.append(func.signature)
            # Retourne l'objet Overload
            return self
        # Si la signature n'est pas unique
        else:
            # On lève une exception
            raise Exception("There is no overload for this method with this" + 
                            " signature: the signature is already taken.")
