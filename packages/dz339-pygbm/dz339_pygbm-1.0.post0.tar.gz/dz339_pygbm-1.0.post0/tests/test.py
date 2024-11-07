from pygbm.gbm_simulator import GBMSimulator
import matplotlib.pyplot as plt

# Parameters for GBM
y0 = 1.0
mu = 0.05
sigma = 0.2
T = 1.0
N = 100

# Initialize simulator
simulator = GBMSimulator(y0, mu, sigma)

# Simulate path
t_values, y_values = simulator.simulate_path(T, N)
t_values_euler, y_values_euler = simulator.simulate_path_euler(T, N)
t_values_milstein, y_values_milstein = simulator.simulate_path_milstein(T, N)

# Plot the simulated path
plt.plot(t_values, y_values, label ="GBM Analytical Path")
plt.plot(t_values_euler, y_values_euler, label ="GBM Euler Path")
plt.plot(t_values_milstein, y_values_milstein, label ="GBM Milstein Path")
plt.xlabel(" Time ")
plt.ylabel("Y(t)")
plt.title("Simulated Geometric Brownian Motion Path")
plt.legend()
plt.show()