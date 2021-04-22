import pytest

from bias_detector.BiasDetector import *
from .common import *

from bias_detector.BiasMetric import BiasMetric

bias_detector = BiasDetector(country='US')


class TestBiasDetector:

    def test_get_p_groups(self):
        p_groups = bias_detector.get_p_groups(first_names=first_names_mock, last_names=last_names_mock, zip_codes=zip_codes_mock)
        assert p_groups.at[0, 'male'] == 0.0
        assert p_groups.at[0, 'female'] == 1.0
        assert p_groups.at[0, 'white'] == 0.22120724490233212
        p_groups = bias_detector.get_p_groups(first_names=first_names_mock, zip_codes=zip_codes_mock)
        assert p_groups.at[0, 'male'] == 0.0
        assert p_groups.at[0, 'female'] == 1.0
        assert p_groups.at[0, 'white'] == 0.37026898144716697
        p_groups = bias_detector.get_p_groups(first_names=first_names_mock, last_names=last_names_mock)
        assert p_groups.at[0, 'male'] == 0.0
        assert p_groups.at[0, 'female'] == 1.0
        assert p_groups.at[0, 'white'] == 0.5408381893515636

    def test_get_bias_report(self):
        bias_report = bias_detector.get_bias_report(first_names=first_names_mock,
                                                    last_names=last_names_mock, zip_codes=zip_codes_mock,
                                                    y_true=y_true_mock, y_pred=y_pred_mock, privileged_race='white')
        bias_metrics_results = bias_report.bias_metrics_results
        assert bias_metrics_results.at[BiasMetric.statistical_parity.name, 'male'].get_diff() == 0.053134892796120714
        assert bias_metrics_results.at[BiasMetric.predictive_equality.name, 'white'].get_diff() == 0.016030656112268837
        assert bias_metrics_results.at[BiasMetric.equal_opportunity.name, 'white'].get_diff() == -0.00666254800184618
        assert bias_metrics_results.at[BiasMetric.statistical_parity.name, 'male'].bias_confidence.p_value == 1.0503689323091784e-07
        full_name = bias_detector.fuzzily_get_emails_full_names(emails_mock)
        bias_report = bias_detector.get_bias_report(first_names=full_name['first_name'],
                                                    last_names=full_name['last_name'], y_true=y_true_mock,
                                                    y_pred=y_pred_mock, privileged_race='white')
        bias_metrics_results = bias_report.bias_metrics_results
        assert bias_metrics_results.at[BiasMetric.statistical_parity.name, 'male'].get_diff() == 0.048666861482969725

    def test_get_bias_report_edge_cases(self):
        with pytest.raises(ValueError, match='Country must be US, other countries are not supported'):
            BiasDetector(country='FR').get_bias_report(first_names=first_names_mock,
                                                       last_names=last_names_mock)
        with pytest.raises(ValueError, match='y_pred/y_scores were not provided'):
            bias_detector.get_bias_report(first_names=first_names_mock,
                                          last_names=last_names_mock, y_pred=None)

    def test_get_features_correlation(self):
        p_groups = bias_detector.get_p_groups(first_names=first_names_mock, last_names=last_names_mock,
                                                zip_codes=zip_codes_mock)
        features = p_groups.rename(columns=lambda x: 'feature_' + x)
        features_groups_correlation = bias_detector.get_features_groups_correlation(first_names=first_names_mock, last_names=last_names_mock,
                                                                                    zip_codes=zip_codes_mock, features=features)
        assert np.diag(features_groups_correlation).sum() == len(p_groups.columns)
        with pytest.raises(ValueError, match='first_names/last_names/zip_codes must be provided'):
            bias_detector.get_features_groups_correlation(first_names=None, last_names=None,
                                                          zip_codes=None, features=features)
        with pytest.raises(ValueError, match='features DataFrame must be provided'):
            bias_detector.get_features_groups_correlation(first_names=first_names_mock, last_names=last_names_mock,
                                                          zip_codes=zip_codes_mock, features=None)
        with pytest.raises(ValueError, match='Input data has different lengths'):
            bias_detector.get_features_groups_correlation(first_names=first_names_mock.head(1), last_names=last_names_mock,
                                                          zip_codes=zip_codes_mock, features=features)
        with pytest.raises(ValueError, match="method should be 'pearson'/'kendall'/'spearman'"):
            bias_detector.get_features_groups_correlation(first_names=first_names_mock, last_names=last_names_mock,
                                                          zip_codes=zip_codes_mock, features=features, method='other')


def test_get_first_names_p_gender_df():
    assert p_gender_given_first_name_df.at['MOSHE', 'male'] == 1.0
    assert p_gender_given_first_name_df.at['SARAH', 'female'] == 1.0
    assert p_gender_given_first_name_df.at['RAY', 'male'] == 0.9683544303797468