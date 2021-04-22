
import pandas as pd
import os

from .common import *
from bias_detector.BiasDetector import BiasDetector
from bias_detector.BiasReport import BiasReport

curr_path = os.path.dirname(os.path.realpath(__file__)) if '__file__' in globals() else os.getcwd()

bias_report = BiasDetector(country='US').get_bias_report(first_names=first_names_mock,
                                            last_names=last_names_mock, y_true=y_true_mock, y_pred=y_pred_mock,
                                            y_scores=y_scores_mock, privileged_race='white')

from unittest.mock import patch


class TestBiasReport:

    @patch("matplotlib.pyplot.show")
    def test_plot_groups(self, mock_show):
        bias_report.plot_groups()

    @patch("matplotlib.pyplot.show")
    def test_plot_y_pred(self, mock_show):
        bias_report.plot_y_pred()

    @patch("matplotlib.pyplot.show")
    def test_plot_y_scores(self, mock_show):
        bias_report.plot_y_scores()

    @patch("matplotlib.pyplot.show")
    def test_plot_summary(self, mock_show):
        bias_report.plot_summary()

    def test_get_summary(self):
        summary = bias_report.get_summary()
        assert summary['Statistical Parity'][0] == 'P(pred=1|Male)-P(pred=1|Female)=0.55-0.49=0.053±0.026 (p-value=1.1e-07)'
        assert summary['Equal Opportunity'][0] == 'TPR<sub>Male</sub>-TPR<sub>Female</sub>=0.56-0.51=0.047±0.036 (p-value=0.00099)'
        assert summary['Predictive Equality'][0] == 'FPR<sub>Male</sub>-FPR<sub>Female</sub>=0.54-0.48=0.06±0.036 (p-value=2.1e-05)'

    def test_get_summary_html(self):
        html = bias_report.get_summary_html()
        assert len(html) > 0

    def test_get_bias_metrics_results(self):
        assert len(bias_report.get_bias_metrics_results()) > 0

    def test_get_estimated_groups_sizes(self):
        assert len(bias_report.get_estimated_groups_sizes()) > 0

    def test_get_p_groups(self):
        assert len(bias_report.get_p_groups()) > 0
