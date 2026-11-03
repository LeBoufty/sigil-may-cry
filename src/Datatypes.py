import json

from Exceptions import ArcanumNotFoundError

with open("src/arcanums.json") as arc:
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
        self.suite = arc_data["suite"]

class Strophe:
    nb_arcanums: int
    def __init__(self) -> None:
        pass

class Cercle:
    nb_strophes: int
    strophes: list[Strophe]
    def __init__(self) -> None:
        pass

class Sigil:
    nb_cercles: int
    cercles: list[Cercle]
    def __init__(self) -> None:
        pass
