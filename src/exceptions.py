class UniversidadeInvalidaError(Exception):
    """Exception para PDFs com universidades invalidas ou sem universidade

    Attributes:
        message -- explicação do erro"""

    def __init__(self, message):
        self.message = message
