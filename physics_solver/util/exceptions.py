class ParseError(Exception):
    msg: str

    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class SolverError(Exception):
    # TODO: Show explanation on website.
    msg: str

    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg
