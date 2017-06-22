"""The info command."""

from json import dumps
from .base import Base

class Info(Base):
    """This command give aditional info of a given Stream"""

    def run(self):
        print "Command info"
