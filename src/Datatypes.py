class Arcanum:
    nom: str
    def __init__(self, nom: str) -> None:
        self.nom = nom
    def draw(self) -> None:
        pass

class Strophe:
    nb_arcanums: int
    def __init__(self) -> None:
        pass
    def draw(self) -> None:
        pass

class Cercle:
    nb_strophes: int
    strophes: list[Strophe]
    def __init__(self) -> None:
        pass
    def draw(self) -> None:
        pass

class Sigil:
    nb_cercles: int
    cercles: list[Cercle]
    def __init__(self) -> None:
        pass
    def draw(self) -> None:
        pass
