import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))


import numpy as np
import pandas as pd


def read_data(filename):
	filename = PROJECT_ROOT / "data" / str(filename)
	data = pd.read_csv(filename, sep=",").to_numpy()
	data = data*10**2
	data = data[10000:]
	return data.T

