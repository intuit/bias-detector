from .mocks_generator import *

def test_generate_mocks():
    first_names_mock, last_names_mock, zip_codes_mock, emails_mock, y_scores_mock, y_pred_mock, y_true_mock = generate_mocks(10)
    assert len(first_names_mock) == 10
    assert len(last_names_mock) == 10
    assert len(zip_codes_mock) == 10
    assert len(emails_mock) == 10
    assert len(y_scores_mock) == 10
    assert len(y_pred_mock) == 10
    assert len(y_true_mock) == 10