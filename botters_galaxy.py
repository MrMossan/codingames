import sys
import math

# Made with love by AntiSquid, Illedan and Wildum.
# You can help children learn to code while you participate by donating to CoderDojo.
from collections import namedtuple


def print_err(arg):
    print >> sys.stderr, arg

def print_out(arg):
    print arg
    print_err(arg)

my_team = int(raw_input())
bush_and_spawn_point_count = int(raw_input())  # useful from wood1, represents the number of bushes and the number of places where neutral units can spawn

Position = namedtuple("Position", ["x", "y"])

starting_point = {
    0: Position(200, 590),
    1: Position(1720, 590)
}

turret = {
    0: Position(100, 590),
    1: Position(1820, 590)
}

for i in xrange(bush_and_spawn_point_count):
    # entity_type: BUSH, from wood1 it can also be SPAWN
    entity_type, x, y, radius = raw_input().split()
    x = int(x)
    y = int(y)
    radius = int(radius)

Item = namedtuple("Item", ["item_name", "item_cost", "damage", "health", "max_health", "mana", "max_mana", "move_speed",
                           "mana_regeneration", "is_potion"])
item_store = []
item_count = int(raw_input())  # useful from wood2
for i in xrange(item_count):
    # item_name: contains keywords such as BRONZE, SILVER and BLADE, BOOTS connected by "_" to help you sort easier
    # item_cost: BRONZE items have lowest cost, the most expensive items are LEGENDARY
    # damage: keyword BLADE is present if the most important item stat is damage
    # move_speed: keyword BOOTS is present if the most important item stat is moveSpeed
    # is_potion: 0 if it's not instantly consumed
    item_name, item_cost, damage, health, max_health, mana, max_mana, move_speed, mana_regeneration, is_potion = raw_input().split()
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
    unit_id, team, unit_type, x, y, attack_range, health, max_health, shield, attack_damage, movement_speed, stun_duration, gold_value, count_down_1, count_down_2, count_down_3, mana, max_mana, mana_regeneration, hero_type, is_visible, items_owned = raw_input().split()
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


def buy_health_potion_if_can(_gold):
    try:
        potion = next(item for item in item_store if item.is_potion == 1 and item.health > 0)
        print_out("BUY " + potion.item_name)
        return True
    except StopIteration:
        return False

def itemize_or_wait(gameturn, h):

    if h.health < h.max_health:
         if buy_health_potion_if_can(gameturn.gold):
             return
    print_out("WAIT")



class PriorityLevel(object):
    NONE = 0
    LOW = 15
    MEDIUM_LOW = 30
    MEDIUM = 45
    MEDIUM_HIGH = 60
    HIGH = 75
    MAX = 100


class Action(object):

    def can_realize(self):
        pass

    def get_priority(self):
        pass

    def apply_action(self):
        pass


class RetreatToTower(Action):

    def __init__(self, game_turn):
        self.game_turn = game_turn

    def __repr__(self):
        return "RetreatToTower"

    def can_realize(self):
        return any(distance(h, turret[my_team]) > 100 for h in self.game_turn.my_heroes)

    def get_priority(self):
        if len(self.game_turn.my_heroes) < len(self.game_turn.enemy_heroes):
            return PriorityLevel.MAX

        if any(h.health < 0.3 * h.max_health for h in self.game_turn.my_heroes):
            return PriorityLevel.MEDIUM_HIGH

        else:
            return PriorityLevel.NONE

    def apply_action(self):
        print_err("APPLYING RetreatToTower")
        for h in self.game_turn.my_heroes:
            if h.hero_type == "IRONMAN" and h.mana > 16 and h.count_down_1 == 0:
                print_out("BLINK " + str(turret[my_team].x) + " " + str(turret[my_team].y))
            else:
                print_out("MOVE " + str(turret[my_team].x) + " " + str(turret[my_team].y))


class MoveBehindWave(Action):

    def __init__(self, game_turn):
        self.game_turn = game_turn
        self.my_units = [u for u in self.game_turn.units if u.unit_type == "UNIT" and u.attack_range == 90 and u.team == my_team]
        self.enemy_units = [u for u in self.game_turn.units if u.unit_type == "UNIT" and u.attack_range == 90 and u.team == 1 - my_team]
        self.enemy_turret = turret[1-my_team]

    def __repr__(self):
        return "MoveBehindWave"

    def can_realize(self):
        return True

    def get_priority(self):

        if self.my_units and self.enemy_units:

            closest_allied_minion_distance = max(min(distance(h, u) for u in self.my_units) for h in self.game_turn.my_heroes)
            closest_enemy_minion_distance = min(min(distance(h, u) for u in self.enemy_units) for h in self.game_turn.my_heroes)

            if closest_enemy_minion_distance < closest_allied_minion_distance:
                return PriorityLevel.HIGH
            else:
                return PriorityLevel.MEDIUM

        if not self.my_units:
            return PriorityLevel.HIGH

        return PriorityLevel.MEDIUM_LOW

    def apply_action(self):

        if self.my_units:
            front_minion = min(self.my_units, key=lambda u: distance(self.enemy_turret, u))
        else:
            front_minion = starting_point[my_team]

        for h in self.game_turn.my_heroes:
            target_pos = Position(math.floor(front_minion.x - math.copysign(h.attack_range - 90, front_minion.x - starting_point[my_team].x)), front_minion.y)

            if self.enemy_units:

                if h.hero_type == "IRONMAN" and h.mana > 16 and h.count_down_1 == 0:
                    print_err("BLINK CD: " + h.hero_type + " " + str(h.count_down_1))
                    print_out("BLINK " + str(target_pos.x) + " " + str(target_pos.y))
                else:
                    closest_enemy = min(self.enemy_units + self.game_turn.enemy_heroes, key=lambda x: distance(x, target_pos))
                    print_out("MOVE_ATTACK " + str(target_pos.x) + " " + str(target_pos.y) + " " + str(closest_enemy.unit_id))
            else:
                print_out("MOVE " + str(target_pos.x) + " " + str(target_pos.y))


class Farming(Action):

    def __init__(self, game_turn):
        self.game_turn = game_turn
        self.my_units = [u for u in self.game_turn.units if u.unit_type == "UNIT" and u.team == my_team]
        self.enemy_units = [u for u in self.game_turn.units if u.unit_type == "UNIT" and u.team == 1 - my_team]
        self.all_units = [u for u in self.game_turn.units if u.unit_type == "UNIT"]

    def __repr__(self):
        return "Farming"

    def can_realize(self):
        """Only possible to retreat if not under the tower already"""
        return any(distance(h, u) < h.attack_range for h in self.game_turn.my_heroes for u in self.all_units)

    def get_priority(self):
        return PriorityLevel.MEDIUM_HIGH

    def apply_action(self):
        for h in self.game_turn.my_heroes:
            try:
                target = next(u for u in self.enemy_units if u.health < h.attack_damage and distance(u,h) < h.attack_range)
                print_out("ATTACK " + str(target.unit_id))
                return
            except StopIteration:
                pass

            try:
                target = next(u for u in self.enemy_units if u.health < 40 and distance(u, h) < h.attack_range)
                print_out("ATTACK " + str(target.unit_id))
            except StopIteration:
                pass

            if any(distance(h, u) < h.attack_range for u in self.enemy_units):
                target = min(self.enemy_units, key=lambda u: distance(h, u))
                print_out("ATTACK " + str(target.unit_id))

            itemize_or_wait(self.game_turn, h)


class AttackEnemyHeroes(Action):

    def __init__(self, game_turn):
        self.game_turn = game_turn

    def __repr__(self):
        return "AttackEnemyHeroes"

    def can_realize(self):
        """Only possible if enemy in range"""
        return any(distance(h, eh) < 500 for h in self.game_turn.my_heroes
                   for eh in self.game_turn.enemy_heroes)

    def get_priority(self):
        """
        If they are in tower range, should focus them
        """
        if any(distance(h, turret[1 - my_team]) < 400 for h in self.game_turn.my_heroes):
            return PriorityLevel.NONE

        if len(self.game_turn.enemy_heroes) < len(self.game_turn.my_heroes):
            return PriorityLevel.MAX

        if any(distance(h, turret[my_team]) < 400 for h in self.game_turn.enemy_heroes):
            return PriorityLevel.HIGH

        my_units = [u for u in self.game_turn.units if u.unit_type == "UNIT" and u.team == my_team]

        their_distance_to_my_wave = min(distance(u,eh) for u in my_units for eh in self.game_turn.enemy_heroes)

        if their_distance_to_my_wave < 300:
            return PriorityLevel.HIGH

        return PriorityLevel.MEDIUM_LOW

    def apply_action(self):

        target = min(self.game_turn.enemy_heroes, key=lambda _h: _h.health)

        for h in self.game_turn.my_heroes:
            if h.hero_type == "IRONMAN":
                if h.mana > 50 and h.count_down_3 == 0 and distance(h, target) < 250:
                    print_out("BURNING " + str(target.x) + " " + str(target.y))
                elif h.mana > 60 and h.count_down_2 == 0 and distance(h, target) < 900:
                    print_out("FIREBALL " + str(target.x) + " " + str(target.y))
                else:
                    print_out("ATTACK " + str(target.unit_id))
            elif h.hero_type == "VALKYRIE":
                if h.mana > 20 and h.count_down_1 == 0 and distance(h, target) < 155:
                    print_out("SPEARFLIP " + str(target.unit_id))
                elif h.mana > 35 and h.count_down_2 == 0 and distance(h, target) < 250:
                    print_out("JUMP " + str(target.x) + " " + str(target.y))
                elif h.mana > 50 and h.count_down_3 == 0 and distance(h, target) < 150:
                    print_out("POWERUP")
                else:
                    print_out("MOVE_ATTACK " + str(target.x) + " " + str(target.y) + " "+ str(target.unit_id))

print("IRONMAN")
print("VALKYRIE")
heroes_picked = ["VALKYRIE", "IRONMAN"]


ACTIONS = [RetreatToTower, MoveBehindWave, Farming, AttackEnemyHeroes]


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
        self.enemy_heroes = [u for u in self.units if u.hero_type == h and u.team == (1 - my_team)]
        print_err(" ".join(_h.hero_type for _h in self.my_heroes) + " heroes in my team.")

    def play_turn(self):

        actions = [cls(self) for cls in ACTIONS]
        possible_actions = [a for a in actions if a.can_realize()]

        if possible_actions:
            picked_action = max(possible_actions, key=lambda a: a.get_priority())
            for _a in possible_actions:
                print_err(str(_a) + ": " + str(_a.get_priority()))
            print_err("APPLYING " + str(picked_action))
            picked_action.apply_action()
        else:
            itemize_or_wait(self, self.my_heroes[0])
            itemize_or_wait(self, self.my_heroes[1])


# game loop
while True:
    g = GameTurn()

    g.play_turn()

