from datetime import datetime as dt
import os
from pandas import to_datetime as td
import yaml

THIS_DIR = os.path.dirname(os.path.realpath(__file__))


def get_configuration():
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


def get_age(birth):
    now = dt.now()
    birth_dt = td(birth)
    age = now.year - birth_dt.year
    if birth_dt.month >= now.month:
        if birth_dt.month == now.month:
            if birth_dt.day > now.day:
                age -= 1
    return age
