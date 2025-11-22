# THIS CLASS IS JUST A PLACEHOLDER!!!!!!!!!!!!
class UpgradeData:
    """Holds data for a single upgrade choice."""
    def __init__(self, name, description, effect_func, icon_color=(200, 200, 200)):
        self.name = name
        self.description = description

        self.effect_func = effect_func

        self.icon_color = icon_color


def effect_might(player):
    print(f"Might chosen! Damage is now {player.base_damage}")

def effect_swiftness(player):
    print(f"Swiftness chosen! Speed is now {player.speed}")

def effect_health(player):
    print(f"Health potion! HP is now {player.health}")


UPGRADE_POOL = [
    UpgradeData("Might I", "Increases base damage by 50.", effect_might, (220, 50, 50)),
    UpgradeData("Swiftness I", "Increases movement speed by 15%.", effect_swiftness, (50, 50, 220)),
    UpgradeData("Full Roast", "Heals 30% of HP.", effect_health, (50, 220, 50)),
]