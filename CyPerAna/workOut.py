import logging

from .utilities import get_cardio_zone
from .reader import FitReader


class GenericWorkOut:
    def __init__(self, _data, _start):
        self.id = None
        self.type = "generic"
        self.data = _data
        self.date = _start.date()
        self.total_time = None
        self.wu_duration = None
        self.duration = None
        self.cd_duration = None

        self.logger = None
        self.init_logger()

    def init_logger(self):
        self.logger = logging.getLogger("CyPerAna." + self.__class__.__name__)

    def set_id(self, id):
        self.id = id

    def set_data(self, data):
        self.data = data

    def set_date(self):
        self.date = self.data.index.min().date()

    def set_total_time(self):
        self.total_time = (self.data.index[-1] - self.data.index[0])

    def execute_athlete_specific_analysis(self, athlete_parameters, cardio_zones):
        self.data["cardio_zone"] = self.data["heart_rate"].apply(
            lambda x: get_cardio_zone(x, athlete_parameters["max-hr"], cardio_zones))
        # TODO: very bad computational performance here

    def execute_not_athlete_specific_analysis(self):
        self.set_total_time()


class TrainerWorkOut(GenericWorkOut):
    def __init__(self, _data, _start):
        super().__init__(_data, _start)
        self.device = None
        self.software = None


class ZwiftWorkOut(TrainerWorkOut):
    def __init__(self, _data, _start):
        super().__init__(_data, _start)
        self.world = None
