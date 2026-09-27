import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
from trame.ui.vuetify3 import VAppLayout
from trame.widgets import vuetify3 as v3
from trame.widgets import vtk as trame_vtk
from trame.widgets import html, client
from trame.widgets import plotly as plotly_widget

css_path = PROJECT_ROOT / "dashboard" / "style.css"

def build_main_ui(server, state, viz, ctrl, config):
	with VAppLayout(server) as layout:
		with layout.root:
			html.Script("document.title = 'Intelligent Monitoring';")
			client.Style(css_path.read_text())
			with v3.VApp() as app:
				with html.Div(classes="dashboard"):
					with html.Div(classes="sidebar"):
						ui_build_title()
						ui_build_parameters(state, config)
					with html.Div(classes="main"):
						with html.Div(classes="timeline"):
							ui_build_time_scrubber(state)
						with html.Div(classes="viewer"):
							ui_build_window(ctrl, viz)
						ui_build_metrics(state)

def ui_build_window(ctrl, viz):
	with html.Div(classes="plot-container"):
		view = plotly_widget.Figure(viz.figure,)
	with html.Div(classes="sensor-container"):
		sensor_view = plotly_widget.Figure(viz.sensor_figure,)
	ctrl.view_update = view.update
	ctrl.sensor_view_update = sensor_view.update
	ctrl.reset_camera = viz.reset_camera
	
def ui_build_title():
	v3.VCardTitle(
		"Intelligent Monitoring",
		classes="sidebar-title",
	)


def ui_build_time_scrubber(state):
	v3.VSlider(
	v_model=("time_step", 0),
	min=0,
	max = ("max_time_step", 1),
	step=1,
	label="Timeline",
	thumb_label="always",
	density="compact",
	hide_details=True
)



def ui_build_parameters(state, config):
	v3.VSelect(
		v_model= ("active_mode",),
		items=("mode_options",),
		label="Choose Mode",
		hide_details=True,
		classes="param-box",
	)
	v3.VTextField(
		v_model_number=("n_steps", state.n_steps),
		label="Number of Steps",
		type="number",
		hide_details=True,
		classes="param-box",
	)
	v3.VTextField(
		v_model_number=("order", state.order),
		label="Order",
		type="number",
		hide_details=True,
		classes="param-box",
	)
	v3.VTextField(
		v_model_number=("q", state.q),
		label="Process Noise",
		type="number",
		hide_details=True,
		classes="param-box",
	)
	v3.VTextField(
		v_model_number=("r", state.r),
		label="Measurement Noise",
		type="number",
		hide_details=True,
		classes="param-box",
	)
	v3.VTextField(
		v_model_number=("p", state.p),
		label="Initial Covariance",
		type="number",
		hide_details=True,
		classes="param-box",
	)
	v3.VTextField(
		v_model_number=("kf_r", state.kf_r),
		label="KF Regularization",
		type="number",
		hide_details=True,
		classes="param-box",
	)
	v3.VTextField(
		v_model_number=("lambda_reg", state.lambda_reg),
		label="State Transition Regularization",
		type="number",
		hide_details=True,
		classes="param-box",
	)
	v3.VTextField(
		v_model=("sensor_input",),
		label="Sensor Configuration (1 - 100)",
		hide_details=True,
		classes="param-box",
		disabled=("use_all_sensors || use_half_sensors",),	
	)
	v3.VCheckbox(
		v_model=("use_all_sensors",),
		label="Use all sensors",
		disabled=("use_half_sensors",),
		hide_details=True,
		density="compact",
	)
	v3.VCheckbox(
		v_model=("use_half_sensors",),
		label="Use half sensors",
		disabled=("use_all_sensors",),
		hide_details=True,
		density="compact",
	)
	v3.VBtn(
		"Run Reconstruction",
		block=True,
		classes="run-button",
		click=config["run_reconstruction"],
	)

def ui_build_metrics(state):
	v3.VTextField(
		label="MAE",
		v_model=("mae",),
		readonly=True,
		hide_details=True,
		classes="metric-box",
	)
































