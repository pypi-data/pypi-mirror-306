import abc
from typing import Optional


class game:
    __metaclass__ = abc.ABCMeta

    displayname: str
    snapshotFilename: Optional[str]

    def __init__(self, displayname):
        self.displayname = displayname
        self.snapshotFilename = None

    @abc.abstractmethod
    def start(self):
        pass