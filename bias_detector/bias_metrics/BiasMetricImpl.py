from bias_detector.bias_metrics.BiasMetricInput import BiasMetricInput
from bias_detector.bias_metrics.BiasMetricOutput import BiasMetricOutput


class BiasMetricImpl:

    def __init__(self) -> None:
        super().__init__()
        self.medium_bias_factor = 1
        self.high_bias_factor = 5

    def execute(self, bias_metric_input: BiasMetricInput) -> BiasMetricOutput:
        raise NotImplemented
