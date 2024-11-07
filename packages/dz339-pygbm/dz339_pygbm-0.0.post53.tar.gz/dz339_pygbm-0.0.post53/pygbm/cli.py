import argparse
import matplotlib.pyplot as plt
from pygbm.gbm_simulator import GBMSimulator

def simulate_analytical(y0, mu, sigma, T, N, output):
    """
    Runs the simulation on the input given by the user using analytical solution and saves the resulting simulation in the output file

    :param y0: Starting location of the simulation.
    :type y0: float

    :param mu: The drift of the simulation.
    :type mu: float

    :param sigma: The diffusion of the simulation.
    :type sigma: float

    :param T: The lenght of time should the program simulate.
    :type T: float or None

    :param N: The number of simualtion steps.
    :type N: int or None

    :param output: The location the file will be saved in.
    :type output: str or None
    """

    # Initialize simulator
    simulator = GBMSimulator(y0, mu, sigma )

    # Simulate path
    t_values, y_values = simulator.simulate_path(T, N)

    # Plot the simulated path
    plt.plot(t_values , y_values , label ="GBM Path")
    plt.xlabel(" Time ")
    plt.ylabel("Y(t)")
    plt.title("Simulated Geometric Brownian Motion Path")
    plt.legend()
    plt.savefig(output)

def simulate_euler(y0, mu, sigma, T, N, output):
    """
    Runs the simulation on the input  given by the user using Euler-Maruyama approximation and saves the resulting simulation in the output file

    :param y0: Starting location of the simulation.
    :type y0: float

    :param mu: The drift of the simulation.
    :type mu: float

    :param sigma: The diffusion of the simulation.
    :type sigma: float

    :param T: The lenght of time should the program simulate.
    :type T: float or None

    :param N: The number of simualtion steps.
    :type N: int or None

    :param output: The location the file will be saved in.
    :type output: str or None
    """

    # Initialize simulator
    simulator = GBMSimulator(y0, mu, sigma )

    # Simulate path
    t_values, y_values = simulator.simulate_path_euler(T, N)

    # Plot the simulated path
    plt.plot(t_values , y_values , label ="GBM Path")
    plt.xlabel(" Time ")
    plt.ylabel("Y(t)")
    plt.title("Simulated Geometric Brownian Motion Path")
    plt.legend()
    plt.savefig(output)

def simulate_milstein(y0, mu, sigma, T, N, output):
    """
    Runs the simulation on the input given by the user using Milstein approximation and saves the resulting simulation in the output file

    :param y0: Starting location of the simulation.
    :type y0: float

    :param mu: The drift of the simulation.
    :type mu: float

    :param sigma: The diffusion of the simulation.
    :type sigma: float

    :param T: The lenght of time should the program simulate.
    :type T: float or None

    :param N: The number of simualtion steps.
    :type N: int or None

    :param output: The location the file will be saved in.
    :type output: str or None
    """

    # Initialize simulator
    simulator = GBMSimulator(y0, mu, sigma )

    # Simulate path
    t_values, y_values = simulator.simulate_path_milstein(T, N)

    # Plot the simulated path
    plt.plot(t_values , y_values , label ="GBM Path")
    plt.xlabel(" Time ")
    plt.ylabel("Y(t)")
    plt.title("Simulated Geometric Brownian Motion Path")
    plt.legend()
    plt.savefig(output)


def main():
    """
    Main function for the CLI tool.
    """
    parser = argparse.ArgumentParser(description="pygbm CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Sub-command to start the analytical simulation
    parser_info = subparsers.add_parser("analytical", help="Simulate Geometric Brownian motion using analytical simulation")
    parser_info.add_argument("--y0", type=float, required=True, help="Starting location of the simulation")
    parser_info.add_argument("--mu", type=float, required=True, help="The drift")
    parser_info.add_argument("--sigma", type=float, required=True, help="The diffusion")
    parser_info.add_argument("--T", type=float, default=10, help="What lenght of time should the program simulate")
    parser_info.add_argument("--N", type=int, default=100, help="The number of simualtion steps")
    parser_info.add_argument("--output", type=str, default="output.png", help="Where should the simualtion be saved in")

    # Sub-command to start the Euler-Maruyama simulation
    parser_info = subparsers.add_parser("euler", help="Simulate Geometric Brownian motion using Euler-Maruyama approximation")
    parser_info.add_argument("--y0", type=float, required=True, help="Starting location of the simulation")
    parser_info.add_argument("--mu", type=float, required=True, help="The drift")
    parser_info.add_argument("--sigma", type=float, required=True, help="The diffusion")
    parser_info.add_argument("--T", type=float, default=10, help="What lenght of time should the program simulate")
    parser_info.add_argument("--N", type=int, default=100, help="The number of simualtion steps")
    parser_info.add_argument("--output", type=str, default="output.png", help="Where should the simualtion be saved in")

    # Sub-command to start the Milstein simulation
    parser_info = subparsers.add_parser("milstein", help="Simulate Geometric Brownian motion using Milstein approximation")
    parser_info.add_argument("--y0", type=float, required=True, help="Starting location of the simulation")
    parser_info.add_argument("--mu", type=float, required=True, help="The drift")
    parser_info.add_argument("--sigma", type=float, required=True, help="The diffusion")
    parser_info.add_argument("--T", type=float, default=10, help="What lenght of time should the program simulate")
    parser_info.add_argument("--N", type=int, default=100, help="The number of simualtion steps")
    parser_info.add_argument("--output", type=str, default="output.png", help="Where should the simualtion be saved in")

    args = parser.parse_args()

    #Run the simulation
    if args.command == "analytical":
        simulate_analytical(args.y0, args.mu, args.sigma, args.T, args.N, args.output)
    elif args.command == "euler":
        simulate_euler(args.y0, args.mu, args.sigma, args.T, args.N, args.output)
    elif args.command == "milstein":
        simulate_milstein(args.y0, args.mu, args.sigma, args.T, args.N, args.output)


if __name__ == "__main__":
    main()