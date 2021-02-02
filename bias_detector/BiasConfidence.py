import numpy as np
import scipy.stats


class BiasConfidence:

    alpha = 0.01

    def __init__(self, p_value: float, standard_error: float) -> None:
        self.p_value = p_value
        self.standard_error = standard_error

    def get_interval(self):
        two_tailed_z = scipy.stats.norm.ppf(1-(BiasConfidence.alpha/2))
        return two_tailed_z * self.standard_error


