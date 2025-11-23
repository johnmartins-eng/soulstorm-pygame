# THIS CLASS IS JUST A PLACEHOLDER!!!!!!!!!!!!
from entities.orbitals.fire import Fire


class UpgradeData:
    """Holds data for a single upgrade choice."""
    def __init__(self, name, description, effect_func, icon_color=(200, 200, 200)):
        self.name = name
        self.description = description

        self.effect_func = effect_func

        self.icon_color = icon_color

def effect_fire_circle(player, all_sprites, attacks, orbitals):
    new_fire = Fire(player)
    orbitals.add(new_fire)
    all_sprites.add(new_fire)
    attacks.add(new_fire)


def effect_might(player, *args, **kwargs):
    print(f"Might chosen! Damage is now {player.base_damage}")

def effect_swiftness(player, *args, **kwargs):
    print(f"Swiftness chosen! Speed is now {player.speed}")

def effect_health(player, *args, **kwargs):
    print(f"Health potion! HP is now {player.health}")


UPGRADE_POOL = [
    UpgradeData("Might I", "Increases base damage by 50.", effect_might, (220, 50, 50)),
    UpgradeData("Fire Ring", "A spinning fire that circles you.", effect_fire_circle, (255, 100, 0)),
    UpgradeData("Full Roast", "Heals 30% of HP.", effect_health, (50, 220, 50)),
]