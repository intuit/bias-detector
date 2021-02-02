
import os
import pandas as pd

curr_path = os.path.dirname(os.path.realpath(__file__)) if '__file__' in globals() else os.getcwd()
emails_mock = pd.read_csv(curr_path + '/mocks/emails.csv', skip_blank_lines=False)['email']
first_names_mock = pd.read_csv(curr_path + '/mocks/first_names.csv', skip_blank_lines=False)['first_name']
last_names_mock = pd.read_csv(curr_path + '/mocks/last_names.csv', skip_blank_lines=False)['last_name']
zip_codes_mock = pd.read_csv(curr_path + '/mocks/zip_codes.csv', skip_blank_lines=False, dtype={'zip_code': str}, keep_default_na=False)['zip_code'].astype(str)
y_scores_mock = pd.read_csv(curr_path + '/mocks/y_scores.csv')['y_score']
y_pred_mock = pd.read_csv(curr_path + '/mocks/y_pred.csv')['y_pred']
y_true_mock = pd.read_csv(curr_path + '/mocks/y_true.csv')['y_true']
