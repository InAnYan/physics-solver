class ParseError(Exception):
    pass


class SolverError(Exception):
    msg: str

    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg
