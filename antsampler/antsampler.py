import numpy as np
from scipy.stats import expon

class AntSampler:
    """
    Sampler based on a toy model of an ant exploring a new space.
    
    Arguments:
        :callable probability:    probability density to explore
        :iterable bounds:         bounds of the box to explore
        :iterable mean_free_path: length of mean free path
        :iterable dx:             local hypercube to search
        :int n_steps:             number of steps
        
    Returns:
        :AntSampler: instance of AntSampler class
    """
    def __init__(self, probability,
                       bounds,
                       mean_free_path,
                       dx,
                       n_steps
                       ):
                       
        self.probability   = probability
        self.bounds        = np.atleast_2d(bounds)
        self.rand_walker   = expon(mean_free_path).rvs
        self.dx            = dx
        
        self.n_steps = n_steps
        
        self.marked_points   = []
        self.saved_points    = []
        
        self.old_point = np.random.uniform(low = bounds[:,0], high = bounds[:,1])

    def mark_point(self, new_point):
    
    def move(self, old_point):
        """
        Updates the ant's position. Unlike Metropolis-Hastings algorithms, here a rejected point is not a step.
        
        Arguments:
            :iterable old_point: initial position of the ant
        
        Returns:
            :iterable: new position
        """
        while True:
            new_point = old_point + rand_walker()
            
