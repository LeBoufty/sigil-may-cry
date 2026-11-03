class ArcanumNotFoundError(Exception):
    def __init__(self, nom:str) -> None:
        self.message = f"ERREUR / Arcanum non-reconnu : {nom}"
        super().__init__(self.message)
