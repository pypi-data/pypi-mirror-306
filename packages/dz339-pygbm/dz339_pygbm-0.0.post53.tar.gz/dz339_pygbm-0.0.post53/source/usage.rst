Usage
=====

.. _installation:

Installation
------------

To use pygbm, first install the repo:

.. code-block:: console

   (.venv) ~$ git clone https://github.com/Dario-Zela/pygbm.git

Then install it:

.. code-block:: console

   (.venv) ~$ cd pygbm
   (.venv) ~/pygbm$ pip install -e .

Run a simulation in the CLI
----------------

To create a simulation in the CLI, the following methods are used:

.. automodule:: pygbm.cli
    :members:
    :undoc-members:

In the console this can be used via:

.. code-block:: console

   (.venv) $ pygbm euler --y0 1.0 --mu 0.05 --sigma 0.2 --T 1.0 --N 100 --output gbm_plot.png

The `--y0`, `--mu`, and `--sigma` arguments are required, while the program will default a `--T` to 10, `--N` to 100 and `output` to "output.png"

Run a simulation
----------------

To create a simulation in a python script the ``GBMSimulator`` class must be used:

.. automodule:: pygbm.gbm_simulator
    :members:
    :undoc-members:


For example:

.. code-block:: python

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
    t_values, y_values = simulator.simulate_path_analytical(T, N)

    # Plot the simulated path
    plt.plot(t_values , y_values , label ="GBM Path")
    plt.xlabel(" Time ")
    plt.ylabel("Y(t)")
    plt.title("Simulated Geometric Brownian Motion Path")
    plt.legend()
    plt.show()

