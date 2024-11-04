import numpy as np
from types import SimpleNamespace
from skopt.space import Space
from skopt.plots import plot_evaluations
import matplotlib.pyplot as plt

def plot_performance(optimizer):
    """Plots the minimum objective function value achieved over iterations.
    
    Parameters:
        optimizer: Optimizer object with Y_iters attribute containing objective func values.
        
    The plot shows the convergence of the optimization process by tracking the
    minimum value found up to each iteration.
    """
    min_f = np.minimum.accumulate(optimizer.Y_iters)

    plt.plot(min_f, marker='o', label='f(x)')
    plt.xlabel('Number of steps (n)')
    plt.ylabel('min f(x) after n steps')
    plt.title('Performance Improvement Over Iteration')
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_opt_process(optimizer):
    """Plots the optimization process by showing objective function values over iterations.
    
    Parameters:
        optimizer: Optimizer object with Y_iters attribute containing objective func values.
        
    The plot visualizes how the objective function values change across optimization steps.
    """
    plt.plot(optimizer.Y_iters, marker='o', label='f(x)')
    plt.xlabel('Number of steps (n)')
    plt.ylabel('f(x) after n steps')
    plt.title('Optimization Process')
    plt.grid(True)
    plt.legend()
    plt.show()

def custom_plot_evaluation(optimizer, bins=20, dimensions=None, plot_dims=None):
    """
    Plots the evaluated points during the optimization process.

    This function creates a plot to visualize the evaluations of the optimization process,
    showing the distribution of evaluated points in the search space.

    Parameters:
        optimizer: Optimizer object with attributes containing evaluated points and best parameters.
        bins (int, optional): The number of bins to use for the histogram. Default is 20.
        dimensions: Labels of the dimension variables.
        plot_dims: List of dimension names or dimension indices from the search-space dimensions to be included in the plot.
        
    The plot is generated using the plot_evaluations function from the skopt library.
    """
    result = SimpleNamespace()
    result.x_iters = optimizer.X_iters.tolist()  
    result.x = optimizer.best_params            
    result.space = Space(optimizer.search_space)   
    plot_evaluations(result, bins=bins, dimensions=dimensions, plot_dims=plot_dims)
    plt.show()
