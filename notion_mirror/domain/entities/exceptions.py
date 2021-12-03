class CannotGetPageContentError(Exception):
    def __init__(self, error_message: str):
        super(CannotGetPageContentError, self).__init__(error_message)
