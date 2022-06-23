import numpy as np
from scipy.stats import expon
from tqdm import tqdm

class Ant:
    """
    Toy model of an ant exploring a new space.
    
    Arguments:
        :callable log_probability: log probability density to explore
        :iterable bounds:          bounds of the box to explore
        :iterable mean_free_path:  length of mean free path
        :iterable dx:              local hypercube to search
        
    Returns:
        :Ant: instance of Ant class
    """
    def __init__(self, log_probability,
                       bounds,
                       mean_free_path,
                       dx,
                       ):
                       
        self.log_probability = log_probability
        self.bounds          = np.atleast_2d(bounds)
        self.rand_walker     = expon(mean_free_path).rvs
        self.dx              = dx
        
        self.initialise_ant()
        
    def self.initialise_ant(self):
        """
        Put the ant in a new spot
        """
        self.position = np.random.uniform(low = self.bounds[:,0], high = self.bounds[:,1])

    def mark(self, marked_points):
        """
        Decide if the position of the ant needs to be marked or not, according to logP.
        
        Arguments:
            :list marked_points: list of marked points
        
        Returns:
            :list: updated list of marked points
        """
        logP = self.log_probability(self.position)
        if logP > self.max_logP:
            self.max_logP = logP
        if 1 - np.exp(logP - self.max_logP) > np.random.uniform():
            marked_points.append(self.position)
        return marked_points
    
    def n_marks(self, position, marked_points):
        """
        Count the number of marked points near the ant's head.
        
        Arguments:
            :iterable position:  ant's position
            :list marked_points: list of marked points
        
        Returns:
            :int: local number of marked points
        """
        local_bounds = np.array([position - dx, position + dx]).T
        return len(np.where((np.prod(bounds[:,0] < x, axis = 1) & np.prod(x < bounds[:,1], axis = 1)))[0])
        
    def move(self, marked_points):
        """
        Update the ant's position. Unlike Metropolis-Hastings algorithms, here a rejected point is not a step.
        
        Arguments:
            :list marked_points: list of marked points
        """
        old_marks = n_marks(self.position, marked_points)
        while True:
            new_position = position + rand_walker()
            if np.prod([b[0] < xi < b[1] for xi, b in zip(new_position, self.bounds)]:
                new_marks  = n_marks(new_position, marked_points)
                if new_marks == 0 or old_marks/new_marks > np.random.uniform():
                    break
        self.position = new_position

class AntSampler:
    """
    Sampler based on a toy model of an ant exploring a new space.
    
    Arguments:
        :callable log_probability: log probability density to explore
        :iterable bounds:          bounds of the box to explore
        :iterable mean_free_path:  length of mean free path
        :iterable dx:              local hypercube to search
        :int n_steps:              number of steps
        :int n_ants:               number of ants
        
    Returns:
        :Ant: instance of Ant class
    """
    def __init__(self, log_probability,
                       bounds,
                       mean_free_path,
                       dx,
                       n_steps_exp,
                       n_draws,
                       thinning = 1,
                       ):
        
        self.log_probability = log_probability
        self.bounds          = np.atleast_2d(bounds)
        self.mean_free_path  = mean_free_path
        self.dx              = dx
        self.n_steps_exp     = int(n_steps_exp)
        self.n_draws         = int(n_draws)
        self.n_ants          = n_ants
        self.thinning        = thinning
    
        self.ant_hill      = [Ant(self.log_probability, self.bounds, self.mean_free_path, self.dx) for _ in range(self.n_ants)]
        
    def initialise(self, clear_marks = False):
        """
        Initialise the ants and forget the sampled points.
        
        Arguments:
            :bool clear_marks: If True, removes the marked points
        """
        [ant.initialise_ant() for ant in self.ant_hill]
        self.points        = []
        if clear_marks:
            self.marked_points = []

    
    def run(self, explore = True):
        """
        Explore and sample the probability density.
        
        Arguments:
            :bool explore: whether or not to explore the space (default: True)
        """
        if explore:
            for _ in tqdm(range(n_steps_exp), desc = 'Exploring'):
                for ant in self.ant_hill:
                    ant.move(self.marked_points)
                    ant.mark(self.marked_points)
        
        for _ in tqdm(range(n_draws), desc = 'Sampling'):
            for ant in self.ant_hill:
                for _ in range(self.thinning):
                    ant.move(self.marked_points)
                self.points.append(ant.position)
