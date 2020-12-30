import logging

from .reader import FitReader
from .utilities import get_athlete_parameters, get_cardio_zones, get_cardio_zone
from .workOut import ZwiftWorkOut


class Instance:
    def __init__(self, athlete='default'):
        self._log = logging.getLogger('CyPerAna.' + self.__class__.__name__)
        self.athlete = athlete
        self.athlete_parameters = get_athlete_parameters(self.athlete)
        self.cardio_zones = get_cardio_zones(self.athlete_parameters["cardio-zones-model"])
        self.wo = {}
        # TODO: create class of wo before
        self._log.info("Initialized instance of CyPerAna")

    def load(self, path):
        ext = path.split(".")[-1]
        if ext == "fit":
            reader = FitReader(path)
            _data, _start, _wo_type = reader.output()
            self._log.info(path + " stored in .data")

            if _wo_type == "zwift":
                self.wo["#TODO"] = ZwiftWorkOut(_data, _start)
                self.standard_routine("#TODO")
            else:
                self._log.info("workout type: + " + _wo_type + " not implemented yet")
        else:
            self._log.info("type f file not implemented yet")

    def standard_routine(self, key):
        self._log.info("Starting standard analysis ruotine")
        self.athlete_specific_analysis(key)
        self.non_athlete_specific_analysis(key)

    def athlete_specific_analysis(self, key):
        self._log.info("Starting athlete-specific analysis")
        self.wo[key].execute_athlete_specific_analysis(self.athlete_parameters,self.cardio_zones)

    def non_athlete_specific_analysis(self, key):
        self._log.info("Starting non athlete-specific analysis")
        self.wo[key].execute_non_athlete_specific_analysis()
