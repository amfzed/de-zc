import sys
import pandas as pd
from datetime import datetime


# example of a script to run on starting up a docker container
print(sys.argv)
print('job finished at {}'.format(datetime.now()))