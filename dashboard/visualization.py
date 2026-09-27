import numpy as np
import plotly.graph_objects as go

from trame.widgets import plotly as plotly_widget

class PowerlineView:
	def __init__(self, original_data, estimated_data):
		self.original_data = original_data
		self.estimated_data = estimated_data
		self.num_states = original_data.shape[1]
		self.x = np.linspace(0.0, 1.0, self.num_states)
		self.figure = go.Figure()

		self._build_scene()
		self._update_axes()
		self._build_sensor_figure()

	def _build_scene(self):
		self.figure.add_trace(
			go.Scatter(
				x=self.x,
				y=self.original_data[0],
				mode="lines",
				name="Original",
				line=dict(color="#00A8CC", width=3),
			)
		)

		self.figure.add_trace(
			go.Scatter(
				x=self.x,
				y=self.estimated_data[0],
				mode="lines",
				name="Reconstruction",
				line=dict(color="#2455D6", width=3),
			)
		)

		self.figure.update_layout(
			paper_bgcolor="white",
			plot_bgcolor="white",
			margin=dict(l=70, r=30, t=30, b=60),
			legend=dict(
				orientation="h",
				yanchor="bottom",
				y=1.02,
				xanchor="right",
				x=1,
			),
			hovermode="x unified",
			modebar=dict(orientation="v"),
		)


	def _update_axes(self):
		self.figure.update_xaxes(
			title_text="Position",
			
			showline=True,
			linewidth=1.5,
			linecolor="#374151",

			mirror=False,

			showgrid=True,
			gridwidth=1,
			gridcolor="#E5E7EB",

			zeroline=False,

			ticks="outside",
			tickwidth=1,
			tickcolor="#374151",

			fixedrange=False,
		)
		self.figure.update_yaxes(
			title_text="Displacement",
			range=[-0.1, 0.1],
			showline=True,
			linewidth=1.5,
			linecolor="#374151",

			showgrid=True,
			gridwidth=1,
			gridcolor="#E5E7EB",

			zeroline=True,
			zerolinewidth=1,
			zerolinecolor="#D1D5DB",

			ticks="outside",
			tickwidth=1,
			tickcolor="#374151",

			fixedrange=True,
		)



	def reset_camera(self):
		self.figure.update_xaxes(autorange=True)
		self.figure.update_yaxes(range=[-0.1, 0.1], autorange=False)
		self.view.update()

	def update(self, original, estimated):
		original = np.asarray(original)
		estimated = np.asarray(estimated)

		self.figure.data[0].y = original
		self.figure.data[1].y = estimated

	def _build_sensor_figure(self):
		self.sensor_figure = go.Figure()

		self.sensor_figure.add_trace(
			go.Scatter(
				x=self.x,
				y=np.zeros(self.num_states),
				mode="lines",
				line=dict(color="#D1D5DB", width=2),
				hoverinfo="skip",
				showlegend=False,
			)
		)
		self.sensor_figure.add_trace(
			go.Scatter(
				x=self.x,
				y=np.zeros(self.num_states),
				mode="markers",
				name="Inactive sensors",
				marker=dict(size=7, color="#D1D5DB"),
				hoverinfo="skip",
			)
		)
		self.sensor_figure.add_trace(
			go.Scatter(
				x=[],
				y=[],
				mode="markers",
				name="Active sensors",
				marker=dict(size=7, color="#374151"),
				hoverinfo="skip",
			)
		)
		self.sensor_figure.update_layout(
			paper_bgcolor="white",
			plot_bgcolor="white",
			height=80,
			margin=dict(l=70, r=30, t=10, b=20),
			showlegend=True,
			legend=dict(
				orientation="h",
				yanchor="bottom",
				y=1.0,
				xanchor="right",
				x=1,
				font=dict(size=11),
			)
		)
		self.sensor_figure.update_xaxes(visible=False, fixedrange=False)
		self.sensor_figure.update_yaxes(visible=False, fixedrange=False)

	def update_sensors(self, sensor_config):
		active = np.array(
			[(i+1) in sensor_config for i in range(self.num_states)]
		)
		
		self.sensor_figure.data[1].x = self.x[~active]
		self.sensor_figure.data[1].y = np.zeros(np.sum(~active))

		self.sensor_figure.data[2].x = self.x[active]
		self.sensor_figure.data[2].y = np.zeros(np.sum(active))
		
