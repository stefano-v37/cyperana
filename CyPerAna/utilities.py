import os

import yaml

THIS_DIR = os.path.dirname(os.path.realpath(__file__))


def get_configuration(athlete):
    conf_path = THIS_DIR + '\\configuration.yml'
    with open(conf_path) as configuration:
        configuration = yaml.safe_load(configuration)
    return configuration["athlete"][athlete]


def do_nothing(*args):
    pass
