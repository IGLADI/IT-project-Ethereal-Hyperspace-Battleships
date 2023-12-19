from threading import Thread
import time

import data
from database import Database
from ship import Ship
from utils import get_betted_amount

_db = Database()


class Player:
    def __init__(self, discord_id):
        global _db
        ship_id = _db.player_ship_id(discord_id)
        money = _db.player_money(discord_id)
        x_pos, y_pos = _db.player_coordinates(discord_id)
        name = _db.player_name(discord_id)

        self._id = discord_id
        self._name = name
        self._ship = Ship(ship_id)
        self._money = money
        self._x_pos = x_pos
        self._y_pos = y_pos
        self._energy_thread = Thread(target=self.update_energy)
        self._energy_thread.daemon = True
        self._energy_thread.start()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def money(self):
        betted_amount = get_betted_amount(self.id)
        return self._money - betted_amount

    @property
    def x_pos(self):
        return self._x_pos

    @property
    def y_pos(self):
        return self._y_pos

    @x_pos.setter
    def x_pos(self, x_pos):
        _db.player_set_x_pos(self.id, x_pos)
        self._x_pos = x_pos

    @y_pos.setter
    def y_pos(self, y_pos):
        global _db
        _db.player_set_y_pos(self.id, y_pos)
        self._y_pos = y_pos

    @property
    def ship(self):
        return self._ship

    @money.setter
    def money(self, amount):
        global _db
        self._money = amount if self._money >= 0 else 0
        _db.player_set_money(self.id, self._money)

    # TODO make a secondary module like solar panels (slow but doesn't consume uranium=>players don't get stuck)
    def update_energy(self):
        while True:
            if self.ship.energy < 100:
                # generate solar energy
                self.ship.energy += self.ship.modules["EnergyGenerator"].generation
                # generate with energy generator
                if self.ship.modules["EnergyGenerator"].is_on:
                    # always use 1 uranium for now, will probably add a different rendement per level later on
                    uranium = self.ship.modules["Cargo"].resources.get("Uranium")
                    if uranium and uranium.amount >= 1:
                        self.ship.add_energy(
                            self.ship.modules["EnergyGenerator"].generation
                        )
                        uranium.amount -= 1
                time.sleep(60)

    def location_name(self) -> str:
        global _db
        return _db.player_location_name(self.id)

    @classmethod
    def register(cls, discord_id, discord_name, player_class, guild_name):
        """Registers a new player in the database."""
        global _db
        _db.store_player(discord_id, discord_name, player_class, guild_name)
        Ship.store(discord_id)

    @classmethod
    def exists(cls, discord_id) -> bool:
        """Returns if a player exists with discord_id."""
        global _db
        return _db.player_exists(discord_id)

    @classmethod
    def get(cls, discord_id):
        """Gets a player from the players cache, if player is not found add it to the cache.
        Note: This assumes player with discord_id exists in the database."""
        p = data.players.get(discord_id)
        if p is None:
            p = cls(discord_id)
            data.players[discord_id] = p
        return p
    
    def report_bug(self, bug_report: str):
        global _db
        _db.store_bug_report(bug_report, self.id)
