
import names
import pandas as pd
import numpy as np
import random
import os
import sys
from bias_detector.BiasDetector import BiasDetector

curr_path = os.path.dirname(os.path.realpath(__file__)) if '__file__' in globals() else os.getcwd()
zip_codes = pd.read_csv(curr_path + '/../bias_detector/resources/us-zip-code-latitude-and-longitude.csv', sep=';', usecols=['Zip'])['Zip'].astype(str).str.zfill(5)


def mock_first_names(n: int=10000):
    first_names = []
    for i in range(n):
        first_names.append(names.get_first_name())
    return pd.Series(first_names).str.lower().rename('first_name')


def mock_last_names(n: int=10000):
    last_names = []
    for i in range(n):
        last_names.append(names.get_last_name())
    return pd.Series(last_names).str.lower().rename('last_name')


def mock_zip_codes(n: int=10000):
    return zip_codes.sample(n, replace=True).rename('zip_code')


def mock_emails(first_names_mock, last_names_mock, n: int=10000):
    patterns = ['{first_name}_{last_name}@domain.com',
                '{last_name}_{first_name}@domain.com',
                '{first_name}{last_name}@domain.com',
                '{last_name}{first_name}@domain.com',
                '{first_name}a@domain.com',
                'a{last_name}@domain.com']
    emails = []
    for i in range(n):
        pattern = random.choice(patterns)
        emails.append(pattern.format(first_name=first_names_mock.loc[i], last_name=last_names_mock.loc[i],))
    return pd.Series(emails).str.lower().rename('email')


def mock_y_scores_and_y_pred(first_names_mock, n: int=10000):
    p_groups = BiasDetector(country='US').get_p_groups(first_names_mock)
    y_scores = np.array([random.uniform(0, 1) if i % 10 != 0 else random.uniform(p_groups.at[i, 'male'], 1) for i in range(n)])
    y_scores = pd.Series(y_scores).rename('y_score')
    y_pred = pd.Series(y_scores >= 0.5).astype(int).rename('y_pred')
    return y_scores, y_pred


def mock_y_true(n: int=10000):
    y_true = np.random.rand(n)
    return pd.Series(y_true >= 0.5).astype(int).rename('y_true')


def generate_mocks(n=10000):
    first_names_mock = mock_first_names(n)
    last_names_mock = mock_last_names(n)
    zip_codes_mock = mock_zip_codes(n)
    emails_mock = mock_emails(first_names_mock, last_names_mock, n)
    y_scores_mock, y_pred_mock = mock_y_scores_and_y_pred(first_names_mock, n)
    y_true_mock = mock_y_true(n)
    return first_names_mock, last_names_mock, zip_codes_mock, emails_mock, y_scores_mock, y_pred_mock, y_true_mock


if "pytest" not in sys.modules:
    first_names_mock, last_names_mock, zip_codes_mock, emails_mock, y_scores_mock, y_pred_mock, y_true_mock = generate_mocks()
    first_names_mock.to_csv('mocks/first_names.csv', index=False)
    last_names_mock.to_csv('mocks/last_names.csv', index=False)
    zip_codes_mock.to_csv('mocks/zip_codes.csv', index=False)
    emails_mock.to_csv('mocks/emails.csv', index=False)
    y_scores_mock.to_csv('mocks/y_scores.csv', index=False)
    y_pred_mock.to_csv('mocks/y_pred.csv', index=False)
    y_true_mock.to_csv('mocks/y_true.csv', index=False)