from location import Location
from database import Database

from module import (
    Module,
    SolarPanel,
    TravelModule,
    MiningModule,
    Canon,
    Shield,
    Fuel,
    Cargo,
    Radar,
    EnergyGenerator,
    DEFAULT_MODULES,
)

_db = Database()


class Ship:
    def __init__(self, ship_id):
        global _db
        modules = _db.ship_modules()

        self.id = ship_id
        self._modules = modules
        # TODO make this in apart battery module
        self._energy = 100
        self._energy_capacity = 100

    @property
    def energy_capacity(self) -> int:
        return self._energy_capacity

    @property
    def energy(self) -> int:
        return self._energy

    @property
    def modules(self) -> dict:
        return self._modules

    def change_energy(self, amount):
        self._energy += amount

    def remove_resource(self, resource_name, amount):
        for resource in self.modules["Cargo"]._capacity:
            if resource.name == resource_name:
                resource.amount -= amount
                break

    def add_resource(self, resource_name, amount):
        for resource in self.modules["Cargo"]._capacity:
            if resource.name == resource_name:
                resource.amount += amount
                break

    @classmethod
    def store(cls, discord_id):
        """Registers a new ship with default modules."""
        global _db
        _db.store_ship(discord_id)

        ship_id = _db.player_ship_id(discord_id)
        for module in DEFAULT_MODULES:
            module.store(ship_id)
