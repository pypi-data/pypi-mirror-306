import numpy as np

"""
pygmb - Python library to simulate geometric brownian motion.

To use the code set up the simulation parameters via the GBMSimulator class
.. code-block:: python

    # Import GBMSimulator
    from pygbm.gbm_simulator import GBMSimulator

    # Parameters for GBM
    y0 = 1.0
    mu = 0.05
    sigma = 0.2

    # Initialize simulator
    simulator = GBMSimulator(y0, mu, sigma)

Finally, to run the simulation call the simulate_path method on the time span and the number of steps the simulation is going to take

.. code-block:: python
    # Parameters for the simulation
    T = 1.0
    N = 100

    # Simulate path
    t_values, y_values = simulator.simulate_path(T, N)
"""

class GBMSimulator:

    """
    The class used to encapsulate the parameters for the simulation and solve the GBM equation.
    """

    def __init__(self, y0, mu, sigma):
        """
        Sets up the physics of the enviroment the simulation will run in

        :param y0: Starting location of the simulation.
        :type y0: float

        :param mu: The drift of the simulation.
        :type mu: float

        :param sigma: The diffusion of the simulation.
        :type sigma: float
        """
        #Store the simulation parameters as attributes of the class
        self.y0 = y0
        self.mu = mu
        self.sigma = sigma

    def browninan(self, dt, N_steps):
        """
        Creates the browninan noise used in the simulation

        :param dt: The length of time between time steps.
        :type dt: float

        :param N_steps: The total number of time steps.
        :type N_steps: int
        """
        
        #Produce the brownian noise and return it
        B = np.random.normal(0, np.sqrt(dt), size=N_steps)
        return B

    def simulate_path(self, T_Final, N_steps):
        """
        Runs the simulation on the input given by the user, using analytical solution
        
        :param T_Final: The lenght of time should the program simulate.
        :type T_Final: float

        :param N_steps: The number of simualtion steps.
        :type N_steps: int
        """
        
        #Get the time step
        dt = T_Final / N_steps

        #Calculate the change in y between each time step
        Y = np.exp((self.mu - self.sigma ** 2 / 2) * dt + self.sigma * self.browninan(dt, N_steps - 1))

        #Add a 1 at the beginning to start from y0
        Y = np.hstack((np.array([1]), Y))

        #"Add" the changes by multiplying them.
        Y = self.y0 * np.cumprod(Y)

        #Get the time passed in the simulation.
        T = np.linspace(0, T_Final, N_steps)
        return T, Y

    def simulate_path_euler(self, T_Final, N_steps):
        """
        Runs the simulation on the input given by the user, using Euler-Maruyama method
        
        :param T_Final: The lenght of time should the program simulate.
        :type T_Final: float

        :param N_steps: The number of simualtion steps.
        :type N_steps: int
        """
        
        #Get the time step
        dt = T_Final / N_steps

        #Get dB(t)
        dB = self.browninan(dt, N_steps - 1)

        #Create Y array
        Y = [self.y0]

        #Use the Euler-Maruyama method
        for i in range(N_steps - 1):
            Y.append(Y[i] + self.mu * Y[i] * dt + self.sigma * Y[i] * dB[i])

        #Get the time passed in the simulation.
        T = np.linspace(0, T_Final, N_steps)

        return T, np.array(Y)

    def simulate_path_milstein(self, T_Final, N_steps):
        """
        Runs the simulation on the input given by the user, using Milstein method
        
        :param T_Final: The lenght of time should the program simulate.
        :type T_Final: float

        :param N_steps: The number of simualtion steps.
        :type N_steps: int
        """
        
        #Get the time step
        dt = T_Final / N_steps

        #Get dB(t)
        dB = self.browninan(dt, N_steps - 1)

        #Create Y array
        Y = [self.y0]

        #Use the Milstein method
        for i in range(N_steps - 1):
            Y.append(
                Y[i] +
                self.mu * Y[i] * dt + 
                self.sigma * Y[i] * dB[i] +
                1/2.0 * self.sigma ** 2 * Y[i] * (dB[i] ** 2 - dt)
                )

        #Get the time passed in the simulation.
        T = np.linspace(0, T_Final, N_steps)

        return T, np.array(Y)