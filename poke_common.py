#Type
#Attack
#SP Attack
# Defense
#SP Defense
# health
# speed
#Ability

import enum
import json
from pokemon_json import *
import numpy as np
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import MinMaxScaler


class Ability(enum.Enum):
    LEVITATE = 1
    ILLUSION = 2
    PRANKSTER = 3
    PURE_POWER = 4
    HARVEST = 5
    NATURAL_CURE = 6
    BIG_FIST = 7

class CurrentPokemon(enum.Enum):
    Pokemon_Slot_1 = 12
    Pokemon_Slot_2 = 13
    Pokemon_Slot_3 = 14
    Pokemon_Slot_4 = 15
    Pokemon_Slot_5 = 16
    Pokemon_Slot_6 = 17

class SelectedAttack(enum.Enum):
    Attack_Slot_1 = 1
    Attack_Slot_2 = 2
    Attack_Slot_3 = 3
    Attack_Slot_4 = 4


class ITEMS(enum.Enum):
    BLUE_BERRY = 1
    CHOICE_SCARF = 2
    LEFT_OVERS = 3
    TOXIC_ORB = 5
    WHITE_HERB = 6
    Z_STONE = 7

class VOLATILE_STATUS(enum.Enum):
    NOTHING = 'Nothing'
    CONFUSION = 'Confusion'


class Status(enum.Enum):
    NOTHING = 'Nothing'
    BURN = 'Burn'
    SLEEP = 'Sleep'
    FROZEN = 'Frozen'
    PARALYSIS = 'Paralysis'
    POISON = 'Poison'
    TOXIC = 'Badly Poison'

class WEATHER(enum.Enum):
    SUN = 0
    RAIN = 1
    HARSH_SUNLIGHT = 2
    DOWNPOUR = 3
    HAIL = 4
    SANDSTORM = 5

class TERRAIN(enum.Enum):
    NO_TERRAIN = 'noterrain'
    ELECTRIC_TERRAIN = 'electricterrain'
    GRASSY_TERRAIN = 'grassyterrain'
    MISTY_TERRAIN = 'mistyterrain'
    PSYCHIC_TERRAIN = 'psychicterrain'

class TARGET(enum.Enum):
    NORMAL = 'normal'
    SELF = 'self'
    ANY = 'any'
    ALL_ADJACENT_FOES = 'allAdjacentFoes'
    ALLY_SIDE = 'allySide'
    ALLY_TEAM = 'allyTeam'
    FOE_SIDE = 'foeSide'
    ADJACENT_FOE = 'adjacentFoe'
    ADJACENT_ALLY = 'adjacentAlly'
    ALL_ADJACENT = 'allAdjacent'
    ADJACENT_ALLY_OR_SELF = 'adjacentAllyOrSelf'
    ALL = 'all'
    SCRIPTED = 'scripted'
    RANDOM_NORMAL = 'randomNormal'

class ELEMENT_TYPE(enum.Enum):
    BUG = "Bug"
    DARK = "Dark"
    DRAGON = "Dragon"
    ELECTRIC = "Electric"
    FAIRLY = "Fairy"
    FIGHTING = "Fighting"
    FIRE = "Fire"
    FLYING = "Flying"
    GHOST = "Ghost"
    GRASS = "Grass"
    GROUND = "Ground"
    ICE = "Ice"
    NORMAL = "Normal"
    POISON = "Poison"
    PSYCHIC = "Psychic"
    ROCK = "Rock"
    STEEL = "Steel"
    WATER = "Water"
    TYPELESS = "Typeless"
    BIRD = "Bird"       # For missing No?

class ELEMENT_MODIFIER(enum.Enum):
    NUETRAL = 0
    SUPER_EFFECTIVE = 1
    RESISTED = 2
    IMMUNE = 3

def get_damage_modifier_for_type(target_pokemon_element, attack):
    damage_modifier = 1
    element_modifier = get_damage_taken(target_pokemon_element, attack.element_type.value)
    if element_modifier == ELEMENT_MODIFIER.NUETRAL:
        damage_modifier = 1
    if element_modifier == ELEMENT_MODIFIER.SUPER_EFFECTIVE:
        damage_modifier = 2
    if element_modifier == ELEMENT_MODIFIER.RESISTED:
        damage_modifier = 0.5
    if element_modifier == ELEMENT_MODIFIER.IMMUNE:
        damage_modifier = 0

    return damage_modifier




"""
    second param is string in case someone wants to test against things like
    paralysis, prankster etc. Not just elements
"""
def get_damage_taken(element_type, to_test_against_name):
    modifier = ELEMENT_MODIFIER.NUETRAL
    element_damage_map = damage_taken_dict[element_type.value]
    if to_test_against_name in element_damage_map:
        element_damage_map = ELEMENT_MODIFIER(element_damage_map[to_test_against_name])
    return element_damage_map


class CATEGORY(enum.Enum):
    STATUS = 'Status'
    PHYSICAL = 'Physical'
    SPECIAL = 'Special'

class Secondary():
    def __init__(self, chance='100', boosts=[], status=None, volatileStatus=None, is_target_self=False):
        self.chance = float(chance) / 100
        self.boosts = boosts
        self.status = status
        self.volatileStatus = volatileStatus
        self.is_target_self = is_target_self

class Attack():
    def __init__(self, id, attack_name, num, pp, element_type, power, accuracy, ignoreImmunity, status, category, priority, is_zmove, target="normal", boosts=None, secondary=None, flags=None, volatileStatus=None, has_recoil=False):
        self.id = id
        self.num = num
        self.attack_name = attack_name
        self.pp  = pp
        self.element_type = element_type
        self.power = power
        self.accuracy = accuracy
        self.status = status
        self.ignoreImmunity = ignoreImmunity
        self.category = category
        self.priority = priority
        self.is_zmove = is_zmove
        self.target = target
        self.boosts = boosts
        self.secondary = secondary
        self.flags = flags
        self.volatileStatus = volatileStatus
        self.has_recoil = has_recoil


class Pokemon():
    def __init__(self, name, num, level, element_1st_type, element_2nd_type, health, atk, spatk, defense, spdef, speed, weight, ability, attacks=[None,None,None,None]):
        self.name = name
        self.num = num
        self.level  = level
        self.max_health = health
        self.curr_health = health
        self.atk = atk
        self.spatk = spatk
        self.defense = defense
        self.spdef = spdef
        self.speed = speed
        self.weight = weight
        self.ability = ability
        self.element_1st_type = element_1st_type
        self.element_2nd_type = element_2nd_type
        self.attacks = attacks
        self.accuracy_modifier = 1
        self.attack_modifier = 1
        self.spatk_modifier = 1
        self.defense_modifier = 1
        self.spdef_modifier = 1
        self.speed_modifier = 1
        self.evasion_modifier = 1
        self.volatileStatus = VOLATILE_STATUS.NOTHING
        self.status = Status.NOTHING
        self.item = ''




# 'side_conditions': {'stealthrock': 0, 'spikes': 0, 'toxic_spikes':0}, 'trapped': False, attack_locked:False,
# Attack_Slot_1_disabled:False, Attack_Slot_2_disabled:False, Attack_Slot_4_disabled:False, Attack_Slot_4_disabled:False, },
# 'weather': None, 'terrain': None, 'forceSwitch': False, 'wait': False}

class Ability(enum.Enum):
    LEVITATE = 1
    ILLUSION = 2
    PRANKSTER = 3
    PURE_POWER = 4
    HARVEST = 5
    NATURAL_CURE = 6
    BIG_FIST = 7

class ITEMS(enum.Enum):
    BLUE_BERRY = 1
    CHOICE_SCARF = 2
    LEFT_OVERS = 3
    TOXIC_ORB = 5
    WHITE_HERB = 6
    Z_STONE = 7

def pokemon_from_json(pokemon_data, attacks=None):
    name = pokemon_data['species']
    num = pokemon_data['num']
    # for one hot encoding of pokemon
    all_pokemon_names.add(num)
    level  = 5
    health = pokemon_data['baseStats']['hp']
    atk = pokemon_data['baseStats']['atk']
    spatk = pokemon_data['baseStats']['spa']
    defense = pokemon_data['baseStats']['def']
    spdef = pokemon_data['baseStats']['spd']
    speed = pokemon_data['baseStats']['spe']
    weight = pokemon_data['weightkg']
    ability = pokemon_data['abilities']['0']
    element_1st_type = ELEMENT_TYPE(pokemon_data['types'][0])
    element_2nd_type = None
    if len(pokemon_data['types']) > 1:
        element_2nd_type = ELEMENT_TYPE(pokemon_data['types'][1])

    pokemon = Pokemon(name, num, level, element_1st_type, element_2nd_type, health=health, atk=atk, spatk=spatk, defense=defense, spdef=spdef, speed=speed, weight=weight, ability=ability)
    pokemon.attacks = attacks
    return pokemon

def attacks_from_json(attack_data, key=None):
    id = attack_data['id']
    # Dont mix num and strings hidden power ruins this
    if 'num' not in attack_data or True:
        num = key
    else:
        num = attack_data['num']
    all_pokemon_attacks.add(num)
    basePower = attack_data['basePower']
    category = CATEGORY(attack_data['category'])
    accuracy = attack_data['accuracy']
    if accuracy is not True:
        accuracy = accuracy / 100.0
    name = attack_data['name']
    pp = attack_data['pp']
    element_type = ELEMENT_TYPE(attack_data['type'])
    ignoreImmunity = False
    if 'ignoreImmunity' in attack_data:
        ignoreImmunity = True
    status = None
    if 'status' in attack_data:
        status = attack_data['status']
    priority = attack_data['priority']
    is_zmove = 'isZ' in attack_data
    target = TARGET(attack_data['target'])
    boosts = None
    volatileStatus = None
    has_recoil = True if 'recoil' in attack_data else False
    if 'boosts' in attack_data:
        boosts = attack_data['boosts']
    if 'volatileStatus' in attack_data:
        volatileStatus = attack_data['volatileStatus']
    secondary = None
    if 'secondary' in attack_data and attack_data['secondary'] is not False:
        sec_boosts = []
        status = None
        is_target_self = False
        if 'boosts' in attack_data['secondary']:
            sec_boosts = attack_data['secondary']['boosts']
        if 'status' in attack_data['secondary']:
            status = attack_data['secondary']['status']

        if 'self' in attack_data['secondary']:
            is_target_self = True
            if 'boosts' in attack_data['secondary']['self']:
                sec_boosts = attack_data['secondary']['self']['boosts']
            if 'status' in attack_data['secondary']['self']:
                status = attack_data['secondary']['self']['status']

        secondary = Secondary(attack_data['secondary']['chance'], sec_boosts, status, volatileStatus, is_target_self)

    flags = []
    flag_keys = attack_data['flags'].keys()
    for key in flag_keys:
        flags.append((key, attack_data['flags'][key]))

    return Attack(id=id, attack_name=name, num=num, pp=pp, element_type=element_type, power=basePower, accuracy=accuracy, ignoreImmunity=ignoreImmunity, status=status, category=category, priority=priority, is_zmove=is_zmove, boosts=boosts, secondary=secondary, flags=flags, volatileStatus=volatileStatus, has_recoil=has_recoil)


#configured by adding pokemon
all_items = set()
all_pokemon_attacks = set()
all_abilities = set()
all_pokemon_names = set()
all_weather = set()
all_status = set()
all_element_types = set()
all_terrains = set()
all_targets = set()
all_categories = set()
all_effectiveness = set()
all_pokemon_slots = set()
all_attack_slots = set()

all_items_labels = None
all_pokemon_attacks_labels = None
all_abilities_labels = None
all_pokemon_names_labels = None
all_weather_labels = None
all_status_labels = None
all_element_types_labels = None
all_terrains_labels = None
all_targets_labels = None
all_categories_labels = None
all_effectiveness_labels = None
all_pokemon_slot_labels = None
all_attack_slot_labels = None

damage_taken_json = json.loads(damage_taken_json_str)
damage_taken_dict = {}
for element in damage_taken_json.keys():
    damage_taken_dict[element] = damage_taken_json[element]['damageTaken']


pokemon_data_json = json.loads(pokemon_data_json_str)
all_pokemon = {}
pokemon_from_json(pokemon_data_json['venusaur'])

for pokemon_key in pokemon_data_json.keys():
  all_pokemon[pokemon_key] = pokemon_from_json(pokemon_data_json[pokemon_key])

attacks_data_json = json.loads(attacks_json_str)
all_attacks = {}
for attack_key in attacks_data_json.keys():
  all_attacks[attack_key] = attacks_from_json(attacks_data_json[attack_key], key=attack_key)

random_pokemon_moves_json = json.loads(random_pokemon_moves)

def get_random_moves_for_pokemon(pokemon_name):
    move_names = random_pokemon_moves_json[pokemon_name]['randomBattleMoves'][:4]
    return move_names

def get_moves_for_pokemon(pokemon_name):
    move_names = random_pokemon_moves_json[pokemon_name]['randomBattleMoves'][:4]
    return [attacks_from_json(attacks_data_json[move_name]) for move_name in move_names]


def get_random_pokemon_team(counta=6):
    rand_poke_names = np.random.choice(elgible_random_pokemon, counta)
    random_pokemon = [pokemon_from_json(pokemon_data_json[pkmn], get_moves_for_pokemon(pkmn)) for pkmn in rand_poke_names]
    return random_pokemon


#configured by adding moves
#handling differently
player_flinched = 1
agent_flinched = 1
player_confused = 1
agent_confused = 1


"""
all_status.add('brn')
all_status.add('par')
all_status.add('slp')
all_status.add('frz')
all_status.add('psn')
all_status.add('tox')
all_status.add('nothing')
"""
def fill_all_category_sets():
    all_status.add(Status.NOTHING.value)
    all_status.add(Status.BURN.value)
    all_status.add(Status.SLEEP.value)
    all_status.add(Status.FROZEN.value)
    all_status.add(Status.PARALYSIS.value)
    all_status.add(Status.POISON.value)
    all_status.add(Status.TOXIC.value)

    pokemon_abilities_json = json.loads(pokemon_abilities_str)
    for ability_key in pokemon_abilities_json.keys():
      all_abilities.add(pokemon_abilities_json[ability_key]['num'])

    pokemon_items_json = json.loads(pokemon_items_str)
    for item_key in pokemon_items_json.keys():
      all_items.add(pokemon_items_json[item_key]['num'])

    weather_data_json = json.loads(pokemon_weather_str)
    for weather_key in weather_data_json.keys():
      all_weather.add(weather_data_json[weather_key]['id'])


    all_terrains.add(TERRAIN.NO_TERRAIN.value)
    all_terrains.add(TERRAIN.ELECTRIC_TERRAIN.value)
    all_terrains.add(TERRAIN.GRASSY_TERRAIN.value)
    all_terrains.add(TERRAIN.MISTY_TERRAIN.value)
    all_terrains.add(TERRAIN.PSYCHIC_TERRAIN.value)

    all_targets.add(TARGET.NORMAL.value)
    all_targets.add(TARGET.SELF.value)
    all_targets.add(TARGET.ANY.value)
    all_targets.add(TARGET.ALL_ADJACENT_FOES.value)
    all_targets.add(TARGET.ALLY_SIDE.value)
    all_targets.add(TARGET.ALLY_TEAM.value)
    all_targets.add(TARGET.FOE_SIDE.value)
    all_targets.add(TARGET.ADJACENT_FOE.value)
    all_targets.add(TARGET.ADJACENT_ALLY.value)
    all_targets.add(TARGET.ALL_ADJACENT.value)
    all_targets.add(TARGET.ADJACENT_ALLY_OR_SELF.value)
    all_targets.add(TARGET.ALL.value)
    all_targets.add(TARGET.SCRIPTED.value)
    all_targets.add(TARGET.RANDOM_NORMAL.value)

    #configured by elements map - Typeless and Bird might not be in map...
    all_element_types.add(ELEMENT_TYPE.BUG.value)
    all_element_types.add(ELEMENT_TYPE.DARK.value)
    all_element_types.add(ELEMENT_TYPE.DRAGON.value)
    all_element_types.add(ELEMENT_TYPE.ELECTRIC.value)
    all_element_types.add(ELEMENT_TYPE.FAIRLY.value)
    all_element_types.add(ELEMENT_TYPE.FIGHTING.value)
    all_element_types.add(ELEMENT_TYPE.FIRE.value)
    all_element_types.add(ELEMENT_TYPE.FLYING.value)
    all_element_types.add(ELEMENT_TYPE.GHOST.value)
    all_element_types.add(ELEMENT_TYPE.GRASS.value)
    all_element_types.add(ELEMENT_TYPE.GROUND.value)
    all_element_types.add(ELEMENT_TYPE.ICE.value)
    all_element_types.add(ELEMENT_TYPE.NORMAL.value)
    all_element_types.add(ELEMENT_TYPE.POISON.value)
    all_element_types.add(ELEMENT_TYPE.PSYCHIC.value)
    all_element_types.add(ELEMENT_TYPE.ROCK.value)
    all_element_types.add(ELEMENT_TYPE.STEEL.value)
    all_element_types.add(ELEMENT_TYPE.WATER.value)
    all_element_types.add(ELEMENT_TYPE.TYPELESS.value)
    all_element_types.add(ELEMENT_TYPE.BIRD.value)

    all_categories.add(CATEGORY.STATUS.value)
    all_categories.add(CATEGORY.PHYSICAL.value)
    all_categories.add(CATEGORY.SPECIAL.value)

    all_effectiveness.add(ELEMENT_MODIFIER.NUETRAL.value)
    all_effectiveness.add(ELEMENT_MODIFIER.SUPER_EFFECTIVE.value)
    all_effectiveness.add(ELEMENT_MODIFIER.RESISTED.value)
    all_effectiveness.add(ELEMENT_MODIFIER.IMMUNE.value)

    all_pokemon_slots.add(CurrentPokemon.Pokemon_Slot_1.value)
    all_pokemon_slots.add(CurrentPokemon.Pokemon_Slot_2.value)
    all_pokemon_slots.add(CurrentPokemon.Pokemon_Slot_3.value)
    all_pokemon_slots.add(CurrentPokemon.Pokemon_Slot_4.value)
    all_pokemon_slots.add(CurrentPokemon.Pokemon_Slot_5.value)
    all_pokemon_slots.add(CurrentPokemon.Pokemon_Slot_6.value)

    all_attack_slots.add(SelectedAttack.Attack_Slot_1.value)
    all_attack_slots.add(SelectedAttack.Attack_Slot_2.value)
    all_attack_slots.add(SelectedAttack.Attack_Slot_3.value)
    all_attack_slots.add(SelectedAttack.Attack_Slot_4.value)

def get_encodings_for_all_sets():
    # one-hot encode the zip code categorical data (by definition of
    # one-hot encoding, all output features are now in the range [0, 1])

    all_items_labels = LabelBinarizer().fit(list(all_items))
    all_abilities_labels = LabelBinarizer().fit(list(all_abilities))
    all_pokemon_names_labels = LabelBinarizer().fit(list(all_pokemon_names))
    all_weather_labels = LabelBinarizer().fit(list(all_weather))
    all_status_labels = LabelBinarizer().fit(list(all_status))
    all_element_types_labels = LabelBinarizer().fit(list(all_element_types))
    all_terrains_labels = LabelBinarizer().fit(list(all_terrains))
    all_targets_labels = LabelBinarizer().fit(list(all_targets))
    all_categories_labels = LabelBinarizer().fit(list(all_categories))
    all_effectiveness_labels = LabelBinarizer().fit(list(all_effectiveness))
    all_pokemon_slot_labels = LabelBinarizer().fit(list(all_pokemon_slots))
    all_attack_slot_labels = LabelBinarizer().fit(list(all_attack_slots))
    all_pokemon_attacks_labels = LabelBinarizer().fit(list(all_pokemon_attacks))



    return all_items_labels, all_abilities_labels, all_pokemon_names_labels, all_weather_labels, \
        all_status_labels, all_element_types_labels, all_terrains_labels, all_targets_labels, \
        all_categories_labels, all_effectiveness_labels, all_pokemon_slot_labels, all_attack_slot_labels, all_pokemon_attacks_labels

fill_all_category_sets()
all_items_labels, all_abilities_labels, all_pokemon_names_labels, all_weather_labels, \
all_status_labels, all_element_types_labels, all_terrains_labels, all_targets_labels, \
all_categories_labels, all_effectiveness_labels, all_pokemon_slot_labels, all_attack_slot_labels, all_pokemon_attacks_labels = get_encodings_for_all_sets()

def flatten(items):
    new_items = []
    for x in items:
        if isinstance(x, list) or isinstance(x, np.ndarray):
            new_items.extend(x[0])
        else:
            new_items.append(x)
    return new_items        


