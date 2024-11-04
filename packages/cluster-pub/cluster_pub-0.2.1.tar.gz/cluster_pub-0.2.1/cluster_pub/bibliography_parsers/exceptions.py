class InvalidBibliographyFileException(Exception):

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InvalidBibliographyFileTypeException(Exception):

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
