from .read import Reader
from fitdecode import FitReader as fr
import pandas as pd

from ..utilities import do_nothing


class FitReader(Reader):
    def __init__(self, path):
        super().__init__(path, file_type="fit")

    def load_file(self):
        rows = []
        with fr(self.path) as fit:
            names = []
            unique_row_types = []
            row_w_fields = []
            row_dicts = []
            for frame in fit:
                row_type = frame.__class__.__name__
                rows.extend([row_type])

                if row_type not in unique_row_types:
                    unique_row_types.extend([row_type])
                    try:
                        do_nothing(frame.fields) # test for the existence of fields attribute
                        row_w_fields.extend([row_type])
                    except:
                        pass

                if row_type in row_w_fields:
                    name = frame.name
                    names.extend([name])
                    fieldnames = [x.name for x in frame.fields]
                    row_dict = {"type": name}
                    for fieldname in fieldnames:
                        value = frame.get_value(fieldname)
                        if value != None:
                            row_dict[fieldname] = value
                    row_dicts.extend([row_dict])

            # row_wo_fields = [x for x in unique_row_types if x not in row_w_fields]
        self.data = pd.DataFrame([x for x in row_dicts if x["type"] == "record"])
        self.data = self.data.loc[:, [x for x in self.data.columns if x != "type"]]
        self.logger.info('.fit records stored in self.data')