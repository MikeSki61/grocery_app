import mkl.constants as constants


class GroceryItem:
    def __init__(self):
        self._name = constants.NAME_DEFAULT
        self._store = constants.STORE_DEFAULT
        self._cost = constants.COST_DEFAULT
        self._amount = constants.AMOUNT_DEFAULT
        self._priority = constants.PRIORITY_DEFAULT
        self._buy = constants.BUY_DEFAULT
        self._id = constants.ID_DEFAULT

    # Getters==================================
    @property
    def name(self):
        return self._name

    @property
    def store(self):
        return self._store

    @property
    def cost(self):
        return self._cost

    @property
    def amount(self):
        return self._amount

    @property
    def priority(self):
        return self._priority

    @property
    def buy(self):
        return self._buy

    @property
    def id(self):
        return self._id

    # Setters=================================
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        self._name = value

    @store.setter
    def store(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        self._store = value

    @cost.setter
    def cost(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError(f"Cost must be an int or float.")
        self._cost = float(value)

    @amount.setter
    def amount(self, value):
        if not isinstance(value, int):
            raise ValueError(f"Amnount must be an int.")
        self._amount = int(value)

    @priority.setter
    def priority(self, value):
        p_min = constants.PRIORITY_MIN
        p_max = constants.PRIORITY_MAX

        if not value:
            pass

        if not isinstance(value, int):
            raise ValueError(f"Priority must be an int, {value}")

        if p_min <= value <= p_max:
            pass
        else:
            raise ValueError("Priority must be between {p_min} and {p_max} ")
        self._priority = value

    @buy.setter
    def buy(self, value):
        if not isinstance(value, bool):
            raise ValueError("Buy must be a boolean.")
        self._buy = value

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("ID must be a valid UUID>")
        self._id = value
        







