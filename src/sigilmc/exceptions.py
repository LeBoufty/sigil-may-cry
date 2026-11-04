class ArcanumNotFoundError(Exception):
    def __init__(self, nom: str) -> None:
        self.message = f"ERREUR / Arcanum non-reconnu : {nom}"
        super().__init__(self.message)

class StropheTropLongueError(Exception):
    def __init__(self, strophe: str, taille: int) -> None:
        super().__init__(f"La strophe « {strophe} » contient {taille} arcanums. Il doit y en avoir moins de 3.")

class CercleTropGrandError(Exception):
    def __init__(self, strophe: str, taille: int) -> None:
        super().__init__(f"Le cercle « {strophe} » contient {taille} strophes. Il doit y en avoir moins de 3.")

class SigilTropGrandError(Exception):
    def __init__(self, strophe: str, taille: int) -> None:
        super().__init__(f"Le sigil « {strophe} » contient {taille} cercles. Il doit y en avoir moins de 3.")

class StropheVideError(Exception):
    def __init__(self) -> None:
        super().__init__("La strophe est vide.")

class CercleVideError(Exception):
    def __init__(self) -> None:
        super().__init__("Le cercle est vide.")

class SigilVideError(Exception):
    def __init__(self) -> None:
        super().__init__("Le sigil est vide.")

class FormeInconnueError(Exception):
    def __init__(self, forme: str) -> None:
        super().__init__(f"Forme géométrique non-reconnue : {forme}")

class FormatNonSupporteError(Exception):
    def __init__(self, format: str) -> None:
        super().__init__(f"Format de fichier non supporté : {format}, seuls .png, .svg et .gif sont acceptés.")
