class InvalidTypeError(TypeError):
    """Exception raised for errors in the input type."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return "InvalidTypeError"
