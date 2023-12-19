from database import Database


_db = Database()


class Item:
    def __init__(self, item_id):
        global _db
        amount = _db.item_amount(item_id)
        name = _db.item_name(item_id)
        item_type = _db.item_type(item_id)

        self._id = item_id
        self._name = name
        self._type = item_type
        self._amount = amount
        # should be set by cargo
        self._max_amount = 900

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def max_amount(self) -> int:
        return self._max_amount

    @amount.setter
    def amount(self, amount):
        if amount > self.max_amount:
            raise ValueError(f"Can not assign more than max_amount: {self.max_amount}")
        global _db
        self._amount = amount
        if amount == 0:
            _db.item_delete(self.id)
        else:
            _db.item_set_amount(self.id, amount)

    @max_amount.setter
    def max_amount(self, max_amount):
        self._max_amount = max_amount

    def __str__(self):
        return f"{self.name} ({self.type}): {self.amount}"


class Resource(Item):
    def __init__(self, item_id):
        super().__init__(item_id)

    def contribute(self, building_id: int, contribution: int):
        """Contribute resource to a building."""
        global _db
        # 1. check if enough of resource
        # 2. add in contributions,
        #    - if already a resource with this name, alter its amount
        #    - else create a new item in database
        # 3. alter amount of resource
        if contribution > self.amount:
            raise ValueError(
                f"Be more modest. {contribution} is much more than what you have {amount}"
            )
        contributed_item_id = _db.contribution_exists(
            building_id=building_id, item_name=self.name
        )
        if contributed_item_id:
            contributed_item = Item(contributed_item_id)
            contributed_item.amount += contribution
        else:
            item_contributed_id = _db.store_item(
                name=self.name, item_type=self.type, amount=contribution
            )
            _db.store_contribution(item_contributed_id, building_id)

        self.amount -= contribution

    @classmethod
    def store(cls, name, amount, cargo_module_id) -> int:
        global _db
        item_id = _db.store_item(
            name=name,
            item_type="resource",
            amount=amount,
            cargo_module_id=cargo_module_id,
        )
        return item_id
