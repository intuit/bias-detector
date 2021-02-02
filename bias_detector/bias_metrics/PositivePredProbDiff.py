import numpy as np
import pandas as pd

from bias_detector.GroupsResults import GroupsResults
from bias_detector.bias_metrics.BiasMetricImpl import BiasMetricImpl
from bias_detector.bias_metrics.BiasMetricInput import BiasMetricInput
from bias_detector.bias_metrics.BiasMetricOutput import BiasMetricOutput
from bias_detector.common import get_p_others



class PositivePredProbDiff(BiasMetricImpl):

    def execute(self, input: BiasMetricInput) -> BiasMetricOutput:
        results = pd.Series(index=input.p_groups.columns)
        for group_name in input.p_groups.columns:
            group = input.p_groups[group_name]
            others = get_p_others(input.p_groups, group_name, input.privileged_race)
            group_p = group.multiply(input.y_pred).sum() / group.sum()
            others_p = others.multiply(input.y_pred).sum() / others.sum()
            group_size = group.sum()
            others_size = others.sum()
            results[group_name] = GroupsResults(group_p, others_p, group_size, others_size)
        return BiasMetricOutput(results)
