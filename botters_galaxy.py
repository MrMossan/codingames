import sys
import math

# Made with love by AntiSquid, Illedan and Wildum.
# You can help children learn to code while you participate by donating to CoderDojo.
from collections import namedtuple

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

print("IRONMAN")
print("DOCTOR_STRANGE")
# game loop
while True:
    gold = int(input())
    enemy_gold = int(input())
    round_type = int(input())  # a positive value will show the number of heroes that await a command
    entity_count = int(input())
    units = []
    for i in range(entity_count):
        units.append(read_unit_input())

    my_heroes = filter(lambda u: u.team == my_team and u.unit_type == "HERO", units)

    if my_heroes:
        for h in my_heroes:
            allies = [u for u in units if u.team == my_team and u.unit_type == "UNIT"]
            enemies = [u for u in units if u.team == 1 - my_team]
            ce = min(enemies, key=lambda u: distance(h, u))

            def in_front_of_hero(a):
                return distance(a, starting_point[1 - my_team]) < distance(h, starting_point[1 - my_team])

            hero_in_front = not any(map(in_front_of_hero, allies))

            def can_buy_damage():
                if h.items_owned < 4:
                    try:
                        item = next(i for i in item_store if "Blade" in i.item_name and i.item_cost < gold)
                        return item
                    except StopIteration:
                        return None

            damage_item = can_buy_damage()

            if hero_in_front:
                # move behind wave
                print("MOVE_ATTACK " + str(starting_point[my_team].x) + " " + str(starting_point[my_team].y) + " " + str(ce.unit_id))
            elif damage_item is not None:
                print("BUY " + damage_item.item_name)

            elif distance(h, ce) < h.attack_range:
                target = None
                try:
                    target = next(e for e in enemies if distance(e,h) < h.attack_range and e.health <= h.attack_damage)
                except StopIteration:
                    if sum(a.health for a in allies) > sum(e.health for e in enemies if e.unit_type == "UNIT"):
                        target = None
                    else:
                        target = ce
                if target is not None:
                    print("ATTACK " + str(target.unit_id))
                else:
                    print("WAIT")
            else:
                start = starting_point[my_team]
                front = max(allies, key=lambda a: distance(a, start))
                new_x = start.x + (front.x - start.x) * 0.9
                new_y = start.y + (front.y - start.y) * 0.9
                print("MOVE_ATTACK " + str(new_x) + " " + str(new_y) + " " + str(ce.unit_id))
    else:
        print("WAIT")
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)


    # If roundType has a negative value then you need to output a Hero name, such as "DEADPOOL" or "VALKYRIE".
    # Else you need to output roundType number of any valid action, such as "WAIT" or "ATTACK unitId"