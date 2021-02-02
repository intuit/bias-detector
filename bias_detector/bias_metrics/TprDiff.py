import pandas as pd
import numpy as np

from bias_detector.GroupsResults import GroupsResults
from bias_detector.bias_metrics.BiasMetricImpl import BiasMetricImpl
from bias_detector.bias_metrics.BiasMetricInput import BiasMetricInput
from bias_detector.bias_metrics.BiasMetricOutput import BiasMetricOutput
from bias_detector.common import get_p_others


class TprDiff(BiasMetricImpl):

    def execute(self, input: BiasMetricInput) -> BiasMetricOutput:
        results = pd.Series(index=input.p_groups.columns)
        for group_name in input.p_groups.columns:
            group = input.p_groups[group_name]
            others = get_p_others(input.p_groups, group_name, input.privileged_race)
            tp = input.y_true.multiply(input.y_pred)
            group_tp = group.multiply(tp).sum()
            others_tp = others.multiply(tp).sum()
            fn = np.multiply(input.y_true.values, 1 - input.y_pred.values)
            group_fn = group.multiply(fn).sum()
            others_fn = others.multiply(fn).sum()
            group_tpr = group_tp / (group_tp + group_fn)
            others_tpr = others_tp / (others_tp + others_fn)
            group_size = (group_tp + group_fn)
            others_size = (others_tp + others_fn)
            results[group_name] = GroupsResults(group_tpr, others_tpr, group_size, others_size)
        return BiasMetricOutput(results)
