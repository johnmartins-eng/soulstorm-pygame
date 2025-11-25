# THIS CLASS IS JUST A PLACEHOLDER!!!!!!!!!!!!
from entities.orbitals.fire import Fire
from utils.game_context import GameContext


class UpgradeData:
    """Holds data for a single upgrade choice."""
    def __init__(self, name, description, effect_func, icon_path=None):
        self.name = name
        self.description = description

        self.effect_func = effect_func

        self.icon_path = icon_path


def effect_fire_circle(game_context):
    player = game_context.player
    new_fire = Fire(player)
    game_context.orbitals.add(new_fire)
    game_context.all_sprites.add(new_fire)
    game_context.attacks.add(new_fire)

def effect_might(game_context):
    player = game_context.player
    player.base_damage += 50
    print(f"Might chosen! Damage is now {player.base_damage}")

def effect_health(game_context):
    player = game_context.player
    heal_amount = player.max_health * 0.30
    player.health = min(player.health + heal_amount, player.max_health)
    print(f"Health potion! HP is now {player.health}")


UPGRADE_POOL = [
    UpgradeData("Might I", "Increases base damage by 50.", effect_might, "assets/icons/might.png"),
    UpgradeData("Fire Ring", "A spinning fire that circles you.", effect_fire_circle, "assets/icons/fire_ring.png"),
    UpgradeData("Heal", "Heals 30% of HP.", effect_health, "assets/icons/potion_regen_life.png"),
]