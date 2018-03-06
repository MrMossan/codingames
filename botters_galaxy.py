import sys
import math

# Made with love by AntiSquid, Illedan and Wildum.
# You can help children learn to code while you participate by donating to CoderDojo.
from collections import namedtuple


def print_err(arg):
    print >> sys.stderr, arg

def print_out(arg):
    print_err(arg)
    print arg

my_team = int(input())
bush_and_spawn_point_count = int(input())  # usefrul from wood1, represents the number of bushes and the number of places where neutral units can spawn

Position = namedtuple("Position", ["x", "y"])

starting_point = {
    0: Position(200, 590),
    1: Position(1720, 590)
}

for i in range(bush_and_spawn_point_count):
    # entity_type: BUSH, from wood1 it can also be SPAWN
    entity_type, x, y, radius = input().split()
    x = int(x)
    y = int(y)
    radius = int(radius)

Item = namedtuple("Item", ["item_name", "item_cost", "damage", "health", "max_health", "mana", "max_mana", "move_speed",
                           "mana_regeneration", "is_potion"])
item_store = []
item_count = int(input())  # useful from wood2
for i in range(item_count):
    # item_name: contains keywords such as BRONZE, SILVER and BLADE, BOOTS connected by "_" to help you sort easier
    # item_cost: BRONZE items have lowest cost, the most expensive items are LEGENDARY
    # damage: keyword BLADE is present if the most important item stat is damage
    # move_speed: keyword BOOTS is present if the most important item stat is moveSpeed
    # is_potion: 0 if it's not instantly consumed
    item_name, item_cost, damage, health, max_health, mana, max_mana, move_speed, mana_regeneration, is_potion = input().split()
    item_cost = int(item_cost)
    damage = int(damage)
    health = int(health)
    max_health = int(max_health)
    mana = int(mana)
    max_mana = int(max_mana)
    move_speed = int(move_speed)
    mana_regeneration = int(mana_regeneration)
    is_potion = int(is_potion)
    item_store.append(Item(item_name, item_cost, damage, health, max_health, mana, max_mana, move_speed,
                           mana_regeneration, is_potion))

Unit = namedtuple("Unit", ["unit_id", "team", "unit_type", "x", "y", "attack_range", "health", "max_health", "shield",
                           "attack_damage", "movement_speed", "stun_duration", "gold_value", "count_down_1",
                           "count_down_2", "count_down_3", "mana", "max_mana", "mana_regeneration",
                           "hero_type", "is_visible", "items_owned"])

def distance(hero,unit):
    return math.sqrt((hero.x - unit.x) ** 2 + (hero.y - unit.y) ** 2)

def read_unit_input():
    # unit_type: UNIT, HERO, TOWER, can also be GROOT from wood1
    # shield: useful in bronze
    # stun_duration: useful in bronze
    # count_down_1: all countDown and mana variables are useful starting in bronze
    # hero_type: DEADPOOL, VALKYRIE, DOCTOR_STRANGE, HULK, IRONMAN
    # is_visible: 0 if it isn't
    # items_owned: useful from wood1
    unit_id, team, unit_type, x, y, attack_range, health, max_health, shield, attack_damage, movement_speed, stun_duration, gold_value, count_down_1, count_down_2, count_down_3, mana, max_mana, mana_regeneration, hero_type, is_visible, items_owned = input().split()
    unit_id = int(unit_id)
    team = int(team)
    x = int(x)
    y = int(y)
    attack_range = int(attack_range)
    health = int(health)
    max_health = int(max_health)
    shield = int(shield)
    attack_damage = int(attack_damage)
    movement_speed = int(movement_speed)
    stun_duration = int(stun_duration)
    gold_value = int(gold_value)
    count_down_1 = int(count_down_1)
    count_down_2 = int(count_down_2)
    count_down_3 = int(count_down_3)
    mana = int(mana)
    max_mana = int(max_mana)
    mana_regeneration = int(mana_regeneration)
    is_visible = int(is_visible)
    items_owned = int(items_owned)
    return Unit(unit_id, team, unit_type, x, y, attack_range, health, max_health, shield, attack_damage, movement_speed,
             stun_duration, gold_value, count_down_1, count_down_2, count_down_3, mana, max_mana, mana_regeneration,
             hero_type, is_visible, items_owned)


#
# BEGIN ALGORITHM CODE
#
previous_heroes_hp = {
    "IRONMAN": 820,
    "DOCTOR_STRANGE": 955
}


def hero_in_danger(hero):
    return hero.health < previous_heroes_hp[hero.hero_type]


def buy_health_potion_if_can(_gold):
    try:
        potion = next(item for item in item_store if item.is_potion == 1 and item.health > 0)
        print_out("BUY " + potion.item_name)
        return True
    except StopIteration:
        return False


def save_hero(current_hero, threatened_hero, _gold):
    if current_hero.unit_id == threatened_hero.unit_id and current_hero.hero_type == "IRONMAN" \
            and current_hero.mana > 16 and current_hero.count_down_1 == 0:
        print_out("BLINK " + str(starting_point[my_team].x) + " " + str(starting_point[my_team].y))
        return True
    elif current_hero.hero_type == "DOCTOR_STRANGE":
        if current_hero.mana > 20 and current_hero.count_down_2 == 0 and distance(threatened_hero, current_hero) < 500:
            print_out("SHIELD " + str(threatened_hero.unit_id))
            return True
        elif current_hero.mana > 30 and current_hero.count_down_1 == 0 and distance(threatened_hero, current_hero) < 250:
            print_out("AOEHEAL " + str(threatened_hero.x) + " " + str(threatened_hero.y))
            return True
    else:
        print_out("MOVE " + str(starting_point[my_team].x) + " " + str(starting_point[my_team].y))
        return True


print("IRONMAN")
print("DOCTOR_STRANGE")
heroes_picked = ["DOCTOR_STRANGE", "IRONMAN"]

class GameTurn(object):

    def __init__(self):
        self.gold = int(input())
        self.enemy_gold = int(input())
        self.round_type = int(input())  # a positive value will show the number of heroes that await a command
        entity_count = int(input())
        self.units = []
        for _ in range(entity_count):
            self.units.append(read_unit_input())

        self.my_heroes = [next(u for u in self.units if u.hero_type == h and u.team == my_team) for h in heroes_picked if any(u.hero_type == h and u.team == my_team for u in self.units)]
        print_err(" ".join(_h.hero_type for _h in self.my_heroes) + " heroes in my team.")

    def pick_action(self, hero):

        print_err(hero.hero_type + " picking an action.")

        allies = [u for u in self.units if u.team == my_team and u.unit_type == "UNIT"]
        enemies = [u for u in self.units if u.team == 1 - my_team]
        ce = min(enemies, key=lambda u: distance(hero, u))

        def in_front_of_hero(a):
            return distance(a, starting_point[1 - my_team]) < distance(hero, starting_point[1 - my_team])

        hero_in_front = not any(map(in_front_of_hero, allies))

        def can_buy_damage():
            if hero.items_owned < 4:
                try:
                    item = next(i for i in item_store if "Blade" in i.item_name and i.item_cost < self.gold)
                    return item
                except StopIteration:
                    return None

        damage_item = can_buy_damage()

        if any(hero_in_danger(_h) for _h in self.my_heroes):
            threatened_hero = next(_h for _h in self.my_heroes if hero_in_danger(_h))
            print_err(hero.hero_type + " trying to save someone: " + threatened_hero.hero_type)
            return save_hero(hero, threatened_hero, self.gold)

        if hero_in_front:
            # move behind wave
            print_out("MOVE_ATTACK " + str(starting_point[my_team].x) + " " + str(starting_point[my_team].y) + " " + str(
                ce.unit_id))
            return True
        elif damage_item is not None:
            print_err(hero.hero_type + " buying item.")
            print_out("BUY " + damage_item.item_name)
            self.gold -= damage_item.item_cost
            return True
        elif distance(hero, ce) < hero.attack_range:
            try:
                target = next(e for e in enemies if distance(e, hero) < hero.attack_range and e.health <= hero.attack_damage)
            except StopIteration:
                if sum(a.health for a in allies) > sum(e.health for e in enemies if e.unit_type == "UNIT"):
                    target = None
                else:
                    target = ce
            if target is not None:
                print_out("ATTACK " + str(target.unit_id))
                return True
            else:
                print_out("WAIT")
                return True
        else:
            start = starting_point[my_team]
            front = max(allies, key=lambda a: distance(a, start))
            new_x = start.x + (front.x - start.x) * 0.9
            new_y = start.y + (front.y - start.y) * 0.9
            print_out("MOVE_ATTACK " + str(new_x) + " " + str(new_y) + " " + str(ce.unit_id))
            return True

        print_err(hero.hero_type + " did not pick an action.")
        return False

    def play_turn(self):
        for h in self.my_heroes:
            if not self.pick_action(h):
                print_out("WAIT")


# game loop
while True:
    g = GameTurn()

    g.play_turn()

    previous_heroes_hp.update(dict((h.hero_type, h.health) for h in g.my_heroes))
