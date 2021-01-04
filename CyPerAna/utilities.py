from datetime import datetime as dt
import os
import numpy as np
from pandas import to_datetime as td
import yaml

THIS_DIR = os.path.dirname(os.path.realpath(__file__))


def calculate_torque(power, rpm):
    """
    Accepts scalars and np.array() as input
    :param power: (W)
    :param rpm: (1/60s)
    :return torque: (Nm)
    """
    torque = power / (2*np.pi*(rpm/60))
    return torque

def calculate_energy(power, duration):
    """
    Accepts scalars and np.array() as input
    :param power: (W)
    :param duration: (s)
    :return torque: (J)
    """
    energy = power * duration
    return energy


def generate_id(_id_keys, _wo_type, _start):
    _id_list = [_wo_type,
                _start.strftime("%Y%m%d")]

    _multiple = sum(["-".join(x.split("-")[0:2]) == "-".join(_id_list) for x in _id_keys])

    if _multiple:
        _id_list.append(str(_multiple))

    _id = "-".join(_id_list)

    return _id


def get_configuration(path=None):
    if path:
        conf_path = path
    else:
        conf_path = THIS_DIR + '\\configuration.yml'
    with open(conf_path) as configuration:
        configuration = yaml.safe_load(configuration)
    return configuration


def get_athlete_parameters(athlete):
    athlete_parameters = get_configuration()["athlete"][athlete]
    if not athlete_parameters["max-hr"]:
        athlete_parameters["max-hr"] = calculate_max_hr(athlete_parameters["birth"])

    return athlete_parameters


def get_cardio_zones(model):
    configuration = get_configuration()
    return configuration["cardio-zones"][model]


def get_cardio_zone(hr, hr_max, cardio_zones):
    """
    From https://www.garmin.com/en-US/blog/general/get-zone-train-using-heart-rate/
    Zone 1: light intensity, walking pace;
    Zone 2: warm-up, cool-down;
    Zone 3: long effort;
    Zone 4: tempo effort;
    Zone 5: sprint effort;
    """

    pcg = hr / hr_max
    zone = 0
    for key in cardio_zones.keys():
        if pcg > float(cardio_zones[key][0]):
            zone += 1

    if pcg > 1:
        zone = "over-max"

    return zone


def do_nothing(*args):
    pass


def calculate_max_hr(birth):
    """
    From Garmin blog
    """
    age = get_age(birth)
    return 220 - age

def calculate_slope(distance_travelled, altitude_climbed):
    slope = np.tan(np.arcsin(altitude_climbed/distance_travelled))
    return slope


def get_age(birth):
    now = dt.now()
    birth_dt = td(birth)
    age = now.year - birth_dt.year
    if birth_dt.month >= now.month:
        if birth_dt.month == now.month:
            if birth_dt.day > now.day:
                age -= 1
    return age


def make_list_tuples_from_dict(input_dict):
    tuples = []
    for lvl1 in input_dict.keys():
        temp_tuple = [lvl1]
        if type(input_dict[lvl1]) is dict:
            for lvl2 in input_dict[lvl1].keys():
                tuples.append(tuple(temp_tuple + [lvl2]))
        else:
            tuples.append(tuple(temp_tuple + [""]))

    return tuples
