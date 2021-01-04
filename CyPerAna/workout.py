import logging
from collections import OrderedDict
from pandas import DataFrame, MultiIndex

from .utilities import calculate_energy, calculate_torque, get_cardio_zone, THIS_DIR, get_configuration, \
    make_list_tuples_from_dict, calculate_slope


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
        self.avg_hr = None
        self.avg_power = None
        self.avg_torque = None
        self.avg_w_kg = None
        self.max_hr = None
        self.max_power = None
        self.max_torque = None
        self.max_w_kg = None

        self._log = None
        self.init_logger()

    @property
    def data_avg(self):
        conf = get_configuration(THIS_DIR + "\\reader\\configuration.yml")
        time_series = conf["time_series"]
        _cols = {item[0]: item[1] if not item[1] else time_series for item in conf["columns"].items()}
        _mi = MultiIndex.from_tuples(make_list_tuples_from_dict(_cols))
        _data = self.data.copy()
        _data.columns = MultiIndex.from_tuples((x, "") for x in _data.columns)
        _data = DataFrame(columns=_mi).append(_data)
        avg_cols = [x for x in _data.columns if x[1] == "raw"]
        _data[avg_cols] = _data[[(x[0], "") if (x[0], "") in _data.columns else (x[0], "raw") for x in avg_cols]]
        _data = _data.loc[:, [x for x in _data.columns if x not in [(x[0], "") for x in avg_cols]]]

        for key in _data.columns:
            if (key[1] in time_series.keys()) & (key[1] != "raw"):
                _data.loc[:, (key[0], key[1])] = _data[key[0]]["raw"].rolling(key[1]).mean()

        return _data[_mi]

    def add_avg_hr(self):
        # TODO: distinguish in full, only workout, cool-down ecc.
        self.avg_hr = self.data["heart-rate"].mean()

    def add_avg_power(self):
        # TODO: distinguish in full, only workout, cool-down ecc.
        self.avg_power = self.data["power"].mean()

    def add_avg_torque(self):
        # TODO: distinguish in full, only workout, cool-down ecc.
        self.avg_torque = self.data["torque"].mean()

    def add_avg_w_kg(self):
        # TODO: distinguish in full, only workout, cool-down ecc.
        self.avg_w_kg = self.data["w/kg"].mean()

    def add_energy(self):
        self.data["energy"] = calculate_energy(self.data["power"], self.data["duration"])
        self.total_energy = self.data["energy"].sum()
        self.fat_burned = self.total_energy / 37000000

    def add_max_hr(self):
        self.max_hr = {x[0] : x[1] for x in self.data_avg["heart-rate"].max().to_dict(into=OrderedDict).items() if x[0] != "raw"}

    def add_max_power(self):
        self.max_power = {x[0] : x[1] for x in self.data_avg["power"].max().to_dict(into=OrderedDict).items() if x[0] != "raw"}

    def add_max_torque(self):
        self.max_torque = {x[0] : x[1] for x in self.data_avg["torque"].max().to_dict(into=OrderedDict).items() if x[0] != "raw"}

    def add_max_w_kg(self):
        self.max_w_kg = {x[0] : x[1] for x in self.data_avg["w/kg"].max().to_dict(into=OrderedDict).items() if x[0] != "raw"}

    def add_torque(self):
        self.data["torque"] = calculate_torque(self.data["power"], self.data["cadence"])

    def add_slope(self):
        self.data["slope"] = calculate_slope(self.data["distance-travelled"], self.data["altitude-climbed"])

    def add_altitude_climbed(self):
        self.data["altitude-climbed"] = (self.data["altitude"] - self.data["altitude"].shift(+1)).fillna(0)

    def add_distance_travelled(self):
        self.data["distance-travelled"] = self.data["distance"] - self.data["distance"].shift(+1).fillna(0)

    def add_w_kg(self, weight):
        self.data["w/kg"] = self.data["power"]/weight

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
        self.data["cardio-zone"] = self.data["heart-rate"].apply(
            lambda x: get_cardio_zone(x, athlete_parameters["max-hr"], cardio_zones))
        # TODO: very bad computational performance here
        self.add_w_kg(athlete_parameters["weight"])

    def execute_non_athlete_specific_analysis(self):
        self._log.info("Executing non athlete-specific analysis on wo")
        self.set_total_time()
        self.add_torque()
        self.add_energy()
        self.add_avg_hr()
        self.add_avg_power()
        self.add_avg_torque()
        self.add_avg_w_kg()
        self.add_max_hr()
        self.add_max_power()
        self.add_max_torque()
        self.add_max_w_kg()
        self.add_altitude_climbed()
        self.add_distance_travelled()
        self.add_slope()


class TrainerWorkOut(GenericWorkOut):
    def __init__(self, _data, _start, device = None, software = None):
        super().__init__(_data, _start)
        self.device = device
        self.software = software


class ZwiftWorkOut(TrainerWorkOut):
    def __init__(self, _data, _start, device = None):
        super().__init__(_data, _start, device = None, software = "zwift")
        self.world = None
