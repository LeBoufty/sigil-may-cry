import json

from Exceptions import ArcanumNotFoundError, StropheTropLongueError, StropheVideError

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
        suitedict = arc_data["suite"]
        self.suite = Suite(suitedict["x"], suitedict["y"], suitedict["taille"])

class Strophe:
    strophe: str
    nb_arcanums: int
    arcanums: list[Arcanum]
    def __init__(self, strophe:str) -> None:
        arcstrings = strophe.strip().lower().split(" - ")
        self.nb_arcanums = len(arcstrings)
        if self.nb_arcanums > 3:
            raise StropheTropLongueError(strophe, self.nb_arcanums)
        elif self.nb_arcanums == 0:
            raise StropheVideError
        self.arcanums = [Arcanum(a) for a in arcstrings]
        self.strophe = strophe

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
