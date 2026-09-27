import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import vtk
from trame.app import get_server
from model.utils import read_data
from dashboard.ui import build_main_ui
from model.dmd_kf import run_dmd
from dashboard.visualization import PowerlineView
from dashboard.utils import intitialize, get_data, default_sensors, calculate_mae
server = get_server()
server.title = "Intelligent Monitoring"
state, ctrl = server.state, server.controller

config= {}

def run_reconstruction():
	global data, estimated_data
	data_run = get_data(state)
	
	estimated_data_run = run_dmd(
		data_run,
		state.sensor_config,
		state.order,
		state.n_steps,
		state.start,
		state.kf_r,
		state.lambda_reg,
		state.q,
		state.r,
		state.p
	)
	estimated_data_run = estimated_data_run.T
	data = data_run
	estimated_data = estimated_data_run
	
	state.time_step = 0
	state.max_time_step = estimated_data_run.shape[0] - 1
	idx = 0
	new_data = data_run[state.start:state.start + state.n_steps,:]
	state.mae = float(calculate_mae(new_data, estimated_data))
	viz.update(new_data[0], estimated_data_run[0])
	ctrl.view_update()

config["run_reconstruction"] = run_reconstruction

@state.change("time_step")
def update_mesh(time_step, **kwargs):
	idx = int(time_step)
	new_data = data[state.start:state.start + state.n_steps,:]
	viz.update(new_data[idx], estimated_data[idx])
	ctrl.view_update()

@state.change("sensor_input", "use_all_sensors", "use_half_sensors")
def validate_sensors(sensor_input, use_all_sensors, use_half_sensors, **kwargs):
	if use_all_sensors and not use_half_sensors:
		state.sensor_config = list(range(1,101))
		viz.update_sensors(state.sensor_config)
		ctrl.sensor_view_update()
		return
	elif use_half_sensors and not use_all_sensors:
		state.sensor_config = list(range(1,52))
		viz.update_sensors(state.sensor_config)
		ctrl.sensor_view_update()
		return

	
	try:
		parsed = [int(x.strip()) for x in sensor_input.split(",") if x.strip()]
		if parsed and all(0 < num < 101 for num in parsed):
			state.sensor_config = parsed
			viz.update_sensors(state.sensor_config)
			ctrl.sensor_view_update()
			return
	except:
		pass

	default_sensors(state)


if __name__ == "__main__":
	intitialize(state)
	data = get_data(state)
	
	estimated_data = run_dmd(
		data,
		state.sensor_config,
		state.order,
		state.n_steps,
		state.start,
		state.kf_r,
		state.lambda_reg,
		state.q,
		state.r,
		state.p
	)
	new_data = data[state.start:state.start+state.n_steps,:]
	
	num_states = data.shape[1]
	x_coords = np.linspace(0, 1, num_states)
	estimated_data = estimated_data.T
	config["estimated_data"] = estimated_data
	state.mae = float(calculate_mae(new_data, estimated_data))
	viz = PowerlineView(data[state.start:state.start+state.n_steps,:], estimated_data)
	viz.update_sensors(state.sensor_config)
	build_main_ui(server, state, viz, ctrl, config)
	server.start(port=1234)



