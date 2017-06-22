"""The list command."""

from json import dumps
from .base import Base
import boto3

class List(Base):
    """This command list all Kinesis Streams in the account"""

    def run(self):
        
        client = boto3.client('kinesis')
        print "Command list"
