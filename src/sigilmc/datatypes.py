import json
import os
from enum import Enum

from sigilmc.exceptions import (
    ArcanumNotFoundError,
    CercleTropGrandError,
    CercleVideError,
    SigilTropGrandError,
    SigilVideError,
    StropheTropLongueError,
    StropheVideError,
)

ARCANUM_FILE_PATH = os.path.join(os.path.dirname(__file__), "../data/arcanums.json")
with open(ARCANUM_FILE_PATH) as arc:
    ARCANUMS = json.load(arc)

class Suite:
    x: float
    y: float
    taille: float
    def __init__(self, x: float, y:float, taille: float) -> None:
        self.x = x
        self.y = y
        self.taille = taille

class Arcanum:
    nom: str
    dessin: list[dict]
    suite: Suite
    def __init__(self, nom: str) -> None:
        if nom in dict(ARCANUMS["arcanums"]):
            self.nom = nom
        elif nom in dict(ARCANUMS["alias"]):
            self.nom = ARCANUMS["alias"][nom]
        else:
            raise ArcanumNotFoundError(nom)
        arc_data = dict(ARCANUMS["arcanums"][self.nom])
        self.dessin = arc_data["dessin"]
        suitedict = arc_data["suite"]
        self.suite = Suite(suitedict["x"], suitedict["y"], suitedict["taille"])

class Strophe:
    strophe: str
    nb_arcanums: int
    arcanums: list[Arcanum]
    def __init__(self, strophe:str) -> None:
        arcstrings = [a.strip() for a in strophe.lower().split("-")]
        self.nb_arcanums = len(arcstrings)
        if self.nb_arcanums > 3:
            raise StropheTropLongueError(strophe, self.nb_arcanums)
        elif self.nb_arcanums == 0:
            raise StropheVideError
        self.arcanums = [Arcanum(a) for a in arcstrings]
        self.strophe = strophe

class ContraintePlace(Enum):
    AUCUNE = 0
    HAUT = 1
    BAS = 2
    COTES = 3

class Cercle:
    nb_strophes: int
    strophes: list[Strophe]
    cercle: str
    contrainte: ContraintePlace
    def __init__(self, cercle: str, contrainte_sup: ContraintePlace) -> None:
        stpstrings = [s.strip() for s in cercle.lower().split(";")]
        # Gestion des multiples, pour pas avoir à taper la même strophe 3 fois
        for i in range(len(stpstrings)):
            if "*" in stpstrings[i]:
                stp = [s.strip() for s in stpstrings[i].split("*")]
                stpstrings.pop(i)
                for j in range(int(stp[0])):
                    stpstrings.insert(i, stp[1])
        self.nb_strophes = len(stpstrings)
        if self.nb_strophes > 3:
            raise CercleTropGrandError(cercle, self.nb_strophes)
        elif self.nb_strophes == 0:
            raise CercleVideError
        # Attribution des contraintes.
        # Cela permet aux cercles de pas se chevaucher
        # Ici, s'il n'y a qu'un tercet, il est en haut s'il en a la place
        # et s'il y en a 3 la "pointe" du triangle sera à l'opposée de la précédente
        elif self.nb_strophes != 2:
            if contrainte_sup == ContraintePlace.HAUT:
                self.contrainte = ContraintePlace.BAS
            else:
                self.contrainte = ContraintePlace.HAUT
        else:
            if contrainte_sup == ContraintePlace.COTES:
                # Manière dégueu de dire qu'il est à la verticale
                self.contrainte = ContraintePlace.BAS
            else:
                self.contrainte = ContraintePlace.COTES
        self.strophes = [Strophe(stp) for stp in stpstrings]
        self.cercle = cercle

class Sigil:
    nb_cercles: int
    cercles: list[Cercle]
    sigil: str
    def __init__(self, sigil: str) -> None:
        cclstrings = [c.strip() for c in sigil.lower().split("/")]
        self.nb_cercles = len(cclstrings)
        if self.nb_cercles > 3:
            raise SigilTropGrandError(sigil, self.nb_cercles)
        elif self.nb_cercles == 0:
            raise SigilVideError
        contrainte = ContraintePlace.AUCUNE
        self.cercles = []
        for c in cclstrings:
            nv_cercle = Cercle(c, contrainte)
            self.cercles.append(nv_cercle)
            contrainte = nv_cercle.contrainte
        self.sigil = sigil
