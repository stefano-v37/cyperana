import logging

from .reader import FitReader
from .utilities import get_athlete_parameters, get_cardio_zones, get_cardio_zone
from .workOut import ZwiftWorkOut


class Instance:
    def __init__(self, athlete='default'):
        self.logger = logging.getLogger('CyPerAna.' + self.__class__.__name__)
        self.athlete = athlete
        self.athlete_parameters = get_athlete_parameters(self.athlete)
        self.cardio_zones = get_cardio_zones(self.athlete_parameters["cardio-zones-model"])
        self.wo = {}
        # TODO: create class of wo before
        self.logger.info("Initialized instance of CyPerAna")

    def load(self, path):
        ext = path.split(".")[-1]
        if ext == "fit":
            reader = FitReader(path)
            _data, _start, _wo_type = reader.output()
            self.logger.info(path + " stored in .data")

            if _wo_type == "zwift":
                self.wo["#TODO"] = ZwiftWorkOut(_data, _start)
                self.standard_routine("#TODO")
            else:
                self.logger.info("workout type: + " + _wo_type + " not implemented yet")
        else:
            self.logger.info("type f file not implemented yet")

    def standard_routine(self, key):
        self.logger.info("Starting standard analysis ruotine")
        self.athlete_specific_analysis(key)
        self.not_athlete_specific_analysis(key)

    def athlete_specific_analysis(self, key):
        self.logger.info("Executing athlete-specific analysis")
        self.wo[key].execute_athlete_specific_analysis(self.athlete_parameters,self.cardio_zones)

    def not_athlete_specific_analysis(self, key):
        self.logger.info("Executing not-athlete-specific analysis")
        self.wo[key].execute_not_athlete_specific_analysis()
