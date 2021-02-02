import pandas as pd
import numpy as np

from bias_detector.GroupsResults import GroupsResults
from bias_detector.bias_metrics.BiasMetricImpl import BiasMetricImpl
from bias_detector.bias_metrics.BiasMetricInput import BiasMetricInput
from bias_detector.bias_metrics.BiasMetricOutput import BiasMetricOutput
from bias_detector.common import get_p_others


class FprDiff(BiasMetricImpl):

    def execute(self, input: BiasMetricInput) -> BiasMetricOutput:
        results = pd.Series(index=input.p_groups.columns)
        for group_name in input.p_groups.columns:
            group = input.p_groups[group_name]
            others = get_p_others(input.p_groups, group_name, input.privileged_race)
            fp = np.multiply(1 - input.y_true.values, input.y_pred.values)
            group_fp = group.multiply(fp).sum()
            others_fp = others.multiply(fp).sum()
            tn = np.multiply(1 - input.y_true.values, 1 - input.y_pred.values)
            group_tn = group.multiply(tn).sum()
            others_tn = others.multiply(tn).sum()
            group_fpr = group_fp / (group_fp + group_tn)
            others_fpr = others_fp / (others_fp + others_tn)
            group_size = (group_fp + group_tn)
            others_size = (others_fp + others_tn)
            results[group_name] = GroupsResults(group_fpr, others_fpr, group_size, others_size)
        return BiasMetricOutput(results)
