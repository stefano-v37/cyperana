import logging


class Reader:
    def __init__(self, path, file_type):
        self.name = self.__class__.__name__
        self.path = path
        self.type = file_type
        self.data = None
        self.time_start = None
        self.wo_type = None
        self._log = logging.getLogger('CyPerAna.' + self.name)
        self._log.info('creating an instance of ' + self.name)

        self.load_file()

    def load_file(self):
        pass

    def output(self):
        return self.data, self.time_start, self.wo_type
