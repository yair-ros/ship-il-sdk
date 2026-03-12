from enum import Enum


class Environment(str, Enum):
    DEV = "https://newbetaapi.ship.co.il"
    PROD = "https://api.ship.co.il"
