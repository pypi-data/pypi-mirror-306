

class InitiativeException(Exception):
    """ Common base class for all non-exit exceptions. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
