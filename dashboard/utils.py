import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import vtk
from trame.app import get_server
from model.utils import read_data

def intitialize(state):
	state.time_step = 0
	state.active_mode = "Normal"
	state.mode_options = ["Normal", "Midspan Mass", "Reversed"]
	state.order = 50
	state.n_steps = 10000
	state.start = 0
	state.kf_r = 1.000
	state.lambda_reg = 0.000
	state.q = 0.001
	state.r = 0.01
	state.p = 1000
	state.max_time_step = state.n_steps - 1
	state.sensor_config = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	state.sensor_input = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	state.use_all_sensors = False
	state.use_half_sensors = False
	state.mae = 0.0

def default_sensors(state):
	state.sensor_config = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def get_data(state):
	if state.active_mode == "Normal":
		file_name = "101_points.csv"
	elif state.active_mode == "Midspan Mass":
		file_name = "m_10_L_2.csv"
	elif state.active_mode == "Reversed":
		file_name = "reversed_101.csv"

	data = read_data(file_name)
	data = data[:, 10000:]
	return data.T

def calculate_mae(original, estimated):
	mae = np.mean(np.abs(original - estimated))
	return mae