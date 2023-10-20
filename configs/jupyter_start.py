
import os, sys
from pathlib import Path
import shutil
import json

from dateutil.relativedelta import relativedelta
from datetime import datetime


# PYTHONPATH
sys.path.insert(0, os.path.abspath(r'C:\Users\pedro\Desktop\hub\projects\wind-forecasting'))
sys.path.insert(0, os.path.abspath(r'C:\Users\pedro\Desktop\hub\projects'))


# Warnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)


# Data
import numpy as np
import pandas as pd


# Pandas options
pd.options.display.max_columns = None
pd.options.display.max_rows = None


# Reload python packages
from IPython import get_ipython
ipython = get_ipython()
if 'ipython' in globals():
    ipython.run_line_magic('load_ext', 'autoreload')
    ipython.run_line_magic('autoreload', '2')


# Visualization
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
