import os

import yaml

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

def get_configuration():
    conf_path = THIS_DIR + '\\configuration.yml'
    with open(conf_path) as configuration:
        configuration = yaml.safe_load(configuration)
    return configuration

def get_configuration_entries(user='default'):
    configuration = get_configuration()
    path = configuration['output_path'][user]
    columns = configuration['columns']
    name = configuration['name'] + '.csv'
    return path, columns, name