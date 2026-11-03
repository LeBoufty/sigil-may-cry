class ArcanumNotFoundError(Exception):
    def __init__(self, nom:str) -> None:
        self.message = f"ERREUR / Arcanum non-reconnu : {nom}"
        super().__init__(self.message)

class StropheTropLongueError(Exception):
    def __init__(self, strophe:str, taille: int) -> None:
        super().__init__(f"La strophe « {strophe} » contient {taille} arcanums. Il doit y en avoir moins de 3.")

class StropheVideError(Exception):
    def __init__(self) -> None:
        super().__init__("La strophe est vide.")
