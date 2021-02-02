from enum import Enum, auto


# See https://en.wikipedia.org/wiki/Fairness_(machine_learning)
class BiasMetric(Enum):
    statistical_parity = auto(), #positive pred prob diff
    equal_opportunity = auto(), #tpr diff
    predictive_equality = auto(), #fpr diff


metrics = [BiasMetric.statistical_parity, BiasMetric.equal_opportunity, BiasMetric.predictive_equality]


def get_bias_metric(name: str) -> BiasMetric:
    for metric in metrics:
        if metric.name == name:
            return metric


def get_bias_metric_description(bias_metric: BiasMetric, group_name: str) -> str:
    if bias_metric == BiasMetric.statistical_parity:
        return 'P(pred=1|{group_name})'.format(group_name=group_name)
    elif bias_metric == BiasMetric.equal_opportunity:
        return 'TPR<sub>{group_name}</sub>'.format(group_name=group_name)
    elif bias_metric == BiasMetric.predictive_equality:
        return 'FPR<sub>{group_name}</sub>'.format(group_name=group_name)


def get_bias_metric_short_description(bias_metric: BiasMetric) -> str:
    if bias_metric == BiasMetric.statistical_parity:
        return 'P(pred=1)'
    elif bias_metric == BiasMetric.equal_opportunity:
        return 'TPR'
    elif bias_metric == BiasMetric.predictive_equality:
        return 'FPR'
