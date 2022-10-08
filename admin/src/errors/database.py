class DbError(Exception):
    pass


class ExistingData(DbError):
    def __init__(
        self,
        info="",
        message=""
    ):
        self.info = info
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        if self.info != "":
            msg = f"{self.info} -> {self.message}"
        else:
            msg = f"Los datos ya existen"
        return msg

class AmountValueError(DbError):
    def __init__(
        self,
        message="El monto no puede ser menor que 0"
    ):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
