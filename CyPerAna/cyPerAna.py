import logging

from .reader import FitReader
from .utilities import get_configuration


class Instance:
    def __init__(self, athlete='default'):
        self.logger = logging.getLogger('CyPerAna.' + self.__class__.__name__)
        self.athlete = athlete
        self.athlete_parameters = get_configuration(self.athlete)
        self.data = {}
        self.logger.info("Initialized instance of CyPerAna")

    def load(self, path):
        ext = path.split(".")[-1]
        if ext == "fit":
            reader = FitReader(path)
            self.data["#TODO"] = reader.data
            self.logger.info(path + " stored in self.data[#TODO]")
        else:
            self.logger.info("type f file not implemented yet")

