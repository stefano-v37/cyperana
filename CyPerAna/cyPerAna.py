import logging

from .reader import FitReader
from .utilities import get_athlete_parameters, get_cardio_zones, get_cardio_zone


class Instance:
    def __init__(self, athlete='default'):
        self.logger = logging.getLogger('CyPerAna.' + self.__class__.__name__)
        self.athlete = athlete
        self.athlete_parameters = get_athlete_parameters(self.athlete)
        self.cardio_zones = get_cardio_zones(self.athlete_parameters["cardio-zones-model"])
        self.data = {}
        self.logger.info("Initialized instance of CyPerAna")

    def load(self, path):
        ext = path.split(".")[-1]
        if ext == "fit":
            reader = FitReader(path)
            self.data["#TODO"] = reader.data.set_index("timestamp")
            self.logger.info(path + " stored in self.data[#TODO]")
        else:
            self.logger.info("type f file not implemented yet")

        self.standardRoutine("#TODO")

    def standardRoutine(self, key):
        self.logger.info("Starting standard analysis ruotine")
        self.athleteSpecificAnalysis(key)

    def athleteSpecificAnalysis(self, key):
        self.logger.info("Excuting athlete-specific analysis")
        self.data[key]["cardio_zone"] = self.data[key]["heart_rate"].apply(
            lambda x: get_cardio_zone(x,
                                      self.athlete_parameters["max-hr"],
                                      self.cardio_zones))
        # TODO: very bad computational performance here

    def notAthleteSpecificAnalysis(self):
        pass

