import numpy as np

def A_from_DMD(data, order, start):
	X = data[:, start:start+order]
	X_prime = data[:, start+1:start+order+1]
	X_pinv = np.linalg.pinv(X)
	A_dmd = np.dot(X_prime, X_pinv)
	return A_dmd, X_prime, X

def regularize_A(X, Y, lambda_reg):
	X_reg = X @ X.T + lambda_reg * np.eye(X.shape[0])
	X_pinv_reg = np.linalg.pinv(X_reg) @ X
	A_reg = Y @ X_pinv_reg.T
	return A_reg

def run_dmd(data, sensor_config, order, n_steps, start, epsilon, lambda_reg, q, r, p):
	data = data.T
	n_states = data.shape[0]
	n_sensors = len(sensor_config)
	if n_states < n_sensors:
		raise ValueError("Sensors cannot be greater than number of states.")
	A_dmd, X_prime, X = A_from_DMD(data, order, start)
	A_reg = regularize_A(X_prime, X, lambda_reg)
	estimated_states = run_kalman_filter(data, sensor_config, n_steps, A_reg, start, epsilon, q, r, p)
	return estimated_states

def run_kalman_filter(data, sensor_config, n_steps, A_reg, start, epsilon, q, r, p):
	n_states = data.shape[0]
	n_sensors = len(sensor_config)
	Q = np.eye(n_states)*q
	R = np.eye(n_sensors)*r
	P = np.eye(n_states)*p

	log_dict = {
		"n_states": n_states,
		"Q_shape": Q.shape,
		"Q_dtype": Q.dtype,
		"Q_size": Q.nbytes / 1024**2,
	}

	w = np.random.multivariate_normal(np.zeros(n_states), Q, 1).T
	v = np.random.multivariate_normal(np.zeros(n_sensors), R, 1).T

	H = np.zeros((n_sensors, n_states))
	for measurement_idx, sensor_idx in enumerate(sensor_config):
		H[measurement_idx, sensor_idx] = 1

	x_hat = data[:, start - 1]
	z = data[sensor_config, start:start + n_steps]
	A = A_reg
	estimated_states = np.zeros((n_states, n_steps))
	for k in range(n_steps):
		x_hat_pred = np.dot(A_reg, x_hat)
		P_pred = np.dot(np.dot(A,P),A.T) + Q + np.eye(n_states)*epsilon
		if np.trace(P_pred) > 1e10:
			P_pred = np.eye(n_states)*p
		y = z[:, k] - np.dot(H, x_hat_pred)
		S = np.dot(np.dot(H,P_pred),H.T) + R + np.eye(n_sensors)*epsilon
		det_S = np.linalg.det(S)
		K = np.dot(np.dot(P_pred,H.T),np.linalg.pinv(S + np.eye(S.shape[0])*epsilon))
		x_hat = x_hat_pred + np.dot(K,y)
		P = np.eye(n_states) - np.dot(np.dot(K,H),P_pred)
		estimated_states[:,k] = x_hat

	return estimated_states




