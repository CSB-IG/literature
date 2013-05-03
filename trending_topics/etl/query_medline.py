# loads sqlite database from medline.txt file

from elixir import *
from models.medline import *
import time, datetime
import pprint
metadata.bind = 'sqlite:///data/medline.sqlite'

setup_all()

