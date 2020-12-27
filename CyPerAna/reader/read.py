import logging


class Reader:
    def __init__(self, path, file_type):
        self.name = self.__class__.__name__
        self.path = path
        self.type = file_type
        self.data = None
        self.logger = logging.getLogger('CyPerAna.' + self.name)
        self.logger.info('creating an instance of ' + self.name)

        self.load_file()

    def load_file(self):
        pass