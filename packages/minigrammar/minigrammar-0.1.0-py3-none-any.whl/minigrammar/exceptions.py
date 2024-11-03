class CannotParseException(Exception):
    def __init__(self):
        super().__init__("Can't parse the given entity")
