import logging

from .utilities import calculate_energy, calculate_torque, get_cardio_zone


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

        self.total_energy = None
        self.fat_burned = None # kg
        self.avg_power = None
        self.max_power = None
        self.max_torque = None

        self._log = None
        self.init_logger()

    def add_energy(self):
        self.data["energy"] = calculate_energy(self.data["power"], self.data["duration"])
        self.total_energy = self.data["energy"].sum()
        self.fat_burned = self.total_energy / 37000000

    def add_torque(self):
        self.data["torque"] = calculate_torque(self.data["power"], self.data["cadence"])

    def init_logger(self):
        self._log = logging.getLogger("CyPerAna." + self.__class__.__name__)

    def set_id(self, id):
        self.id = id

    def set_data(self, data):
        self.data = data

    def set_date(self):
        self.date = self.data.index.min().date()

    def set_total_time(self):
        self.total_time = (self.data.index[-1] - self.data.index[0])

    def execute_athlete_specific_analysis(self, athlete_parameters, cardio_zones):
        self._log.info("Executing athlete-specific analysis on wo")
        self.data["cardio_zone"] = self.data["heart_rate"].apply(
            lambda x: get_cardio_zone(x, athlete_parameters["max-hr"], cardio_zones))
        # TODO: very bad computational performance here

    def execute_non_athlete_specific_analysis(self):
        self._log.info("Executing non athlete-specific analysis on wo")
        self.set_total_time()
        self.add_torque()
        self.add_energy()


class TrainerWorkOut(GenericWorkOut):
    def __init__(self, _data, _start, device = None, software = None):
        super().__init__(_data, _start)
        self.device = device
        self.software = software


class ZwiftWorkOut(TrainerWorkOut):
    def __init__(self, _data, _start, device = None):
        super().__init__(_data, _start, device = None, software = "zwift")
        self.world = None
