import numpy as np
from scipy.stats import multivariate_normal as mn
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
    def __init__(self,
                 log_probability,
                 bounds,
                 mean_free_path,
                 dx,):
                       
        self.log_probability = log_probability
        self.bounds = np.atleast_2d(bounds)
        dim = len(dx)
        self.rand_walker = mn(np.zeros(dim),
                              np.identity(dim)*mean_free_path).rvs
        self.dx = dx
        
        self.initialise_ant()
        self.max_logP = -np.inf

        self.position = None
        
    def initialise_ant(self):
        """
        Put the ant in a new spot
        """
        self.position = np.atleast_1d(
            np.random.uniform(low=self.bounds[:, 0],
                              high=self.bounds[:, 1]))

    def mark(self, marked_points):
        """
        Decide if the position of the ant needs to be marked or not,
        according to logP.
        
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
        local_bounds = np.array([position - self.dx, position + self.dx]).T
        if len(marked_points) > 0:
            return len(np.where(
                (np.prod(local_bounds[:, 0] < marked_points, axis=1) &
                 np.prod(marked_points < local_bounds[:, 1], axis=1)))[0])
        return 0
        
    def move(self, marked_points):
        """
        Update the ant's position. Unlike Metropolis-Hastings algorithms,
        here a rejected point is not a step.
        
        Arguments:
            :list marked_points: list of marked points
        """
        old_marks = self.n_marks(self.position, marked_points)
        flag = True
        while flag:
            new_position = self.position + self.rand_walker()
            if np.prod([b[0] < xi < b[1]
                        for xi, b in zip(new_position, self.bounds)]):
                new_marks = self.n_marks(new_position, marked_points)
                if new_marks == 0 or old_marks/new_marks > np.random.uniform():
                    flag = False
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
    def __init__(self,
                 log_probability,
                 bounds,
                 mean_free_path,
                 dx,
                 n_steps_exp,
                 n_draws,
                 burnin=1000,
                 thinning=1,
                 n_ants=1,):
        
        self.log_probability = log_probability
        self.bounds = np.atleast_2d(bounds)
        self.mean_free_path = mean_free_path
        self.dx = dx
        self.n_steps_exp = int(n_steps_exp)
        self.n_draws = int(n_draws)
        self.n_ants = n_ants
        self.thinning = thinning
        self.burnin = burnin
    
        self.ant_hill = [
            Ant(self.log_probability,
                self.bounds,
                self.mean_free_path,
                self.dx) for _ in range(self.n_ants)
        ]
        self.points = []
        self.marked_points = []

    def initialise(self, clear_marks=False):
        """
        Initialise the ants and forget the sampled points.
        
        Arguments:
            :bool clear_marks: If True, removes the marked points
        """
        [ant.initialise_ant() for ant in self.ant_hill]
        self.points = []
        if clear_marks:
            self.marked_points = []

    def run(self, explore=True):
        """
        Explore and sample the probability density.
        
        Arguments:
            :bool explore: whether or not to explore the space
            (default: True)
        
        Returns:
            :np.ndarray: samples
        """
        if explore:
            for _ in tqdm(range(self.n_steps_exp//self.n_ants),
                          desc='Exploring'):
                for ant in self.ant_hill:
                    ant.move(self.marked_points)
                    ant.mark(self.marked_points)
        self.initialise()
        for ant in tqdm(self.ant_hill,
                        desc='Termalizing'):
            for _ in range(self.thinning):
                ant.move(self.marked_points)
        
        for _ in tqdm(range(self.n_draws//self.n_ants),
                      desc='Sampling'):
            for ant in self.ant_hill:
                for _ in range(self.thinning):
                    ant.move(self.marked_points)
                self.points.append(ant.position)

        return np.array(self.points)
