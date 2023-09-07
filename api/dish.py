from dataclasses import dataclass


@dataclass
class Dish:
    name: str


def list_dishes():
    return [
        Dish("Pâtes carbonara"),
        Dish("Spaghetti bolognaise"),
        Dish("Sushi"),
        Dish("Pizza"),
    ]
