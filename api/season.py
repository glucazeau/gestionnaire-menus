from dataclasses import dataclass


@dataclass
class Season:
    name: str
    icon: str


def list_seasons():
    return [
        Season("Printemps", "🌱"),
        Season("Été", "☀"),
        Season("Automne", "🍂"),
        Season("Hiver", "🌨️"),
    ]
