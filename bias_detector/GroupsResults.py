import numpy as np
import scipy.stats
import scipy.stats

from bias_detector.BiasConfidence import BiasConfidence


class GroupsResults:

    def __init__(self, group_p: float, others_p: float, group_size: float, others_size: float) -> None:
        self.group_p = group_p
        self.others_p = others_p
        self.group_size = group_size
        self.others_size = others_size
        self.bias_confidence = self.get_bernoulli_mean_diff_bias_confidence()

    def get_diff(self) -> float:
        return self.group_p - self.others_p

    def get_bernoulli_mean_diff_bias_confidence(self) -> BiasConfidence:
        if self.group_size < 30 or self.others_size < 30:
            return None
        group_success_count = self.group_p * self.group_size
        others_success_count = self.others_p * self.others_size
        pooled_p = (group_success_count + others_success_count) / (self.group_size + self.others_size)
        pooled_variance = pooled_p * (1 - pooled_p)
        if pooled_variance == 0:
            return None
        standard_error = np.sqrt(pooled_variance * ((1 / self.group_size) + (1 / self.others_size)))
        abs_result = np.abs(self.group_p - self.others_p)
        z_score = abs_result / standard_error
        p_value = (scipy.stats.norm.sf(z_score) * 2)
        return BiasConfidence(p_value, standard_error)
