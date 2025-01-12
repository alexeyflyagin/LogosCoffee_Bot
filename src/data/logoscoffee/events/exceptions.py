class SkipHandler(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class DuplicateEventHandlerError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
