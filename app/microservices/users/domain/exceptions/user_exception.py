
class CustomExcepcion(ValueError):
    def __init__(self, message, field: str = 'detail', *args):
        self.message = message
        self.error = {field: [message]}
        super().__init__(self.error, *args)

    def __str__(self):
        return str(self.message)


class UserNotFoundExcepcion(CustomExcepcion):
    pass
