# PYGBM

A python package to create simulations of geometric browninan motion

## Features
It can be used as a python package by importing it, as shown in the test, or it can be used inline in linux.

## Installation

Download the pygbm repo and use `pip install -e .`.

## Usage
The class GBMSimulator is initialised with the starting location, the drift and the diffusion of the system, and then the method simulate_path can be run to get the path.

An example simulation is below:

```python
from pygbm.gbm_simulator import GBMSimulator
import matplotlib.pyplot as plt

# Parameters for GBM
y0 = 1.0
mu = 0.05
sigma = 0.2
T = 1.0
N = 100

# Initialize simulator
simulator = GBMSimulator(y0, mu, sigma )

# Simulate path
t_values, y_values = simulator.simulate_path_analytical(T, N)

# Plot the simulated path
plt.plot(t_values , y_values , label ="GBM Path")
plt.xlabel(" Time ")
plt.ylabel("Y(t)")
plt.title("Simulated Geometric Brownian Motion Path")
plt.legend()
plt.show()
```

This program can also be run on the cli by using the pygbm command, with the method subargument, as below
```bash
pygbm euler --y0 1.0 --mu 0.05 --sigma 0.2 --T 1.0 --N 100 --output gbm_plot.png
```

## Documentation

To change
Link to the [documentation page](https://pygbmdariodis2024.readthedocs.io/en/latest/#).

## Contributing

Contributions via pull requests are welcome!

## License

This project is licensed under the MIT License - see the LICENSE file for details.