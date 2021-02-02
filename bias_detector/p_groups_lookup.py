import pandas as pd
import numpy as np
import os
import sys

curr_path = os.path.dirname(os.path.realpath(__file__)) if '__file__' in globals() else os.getcwd()
races_columns = ['white', 'black', 'api', 'hispanic', 'native', 'multiple']


def read_census_first_names_file(path: str) -> pd.DataFrame:
    names_df = pd.read_csv(curr_path + path, sep=r'\s+', header=None,
                           names=['name', 'frequency', 'cumulative_frequency', 'rank'],
                           usecols=['name', 'frequency'], index_col='name', keep_default_na=False)
    names_df.index = names_df.index.str.upper()
    names_df['frequency'] = names_df['frequency'] / 100.0
    return names_df


def read_p_race_given_first_name_file():
    rename_dict = {'firstname': 'first_name', 'obs': 'count',
                   'pctwhite': 'white', 'pctblack': 'black',
                   'pctapi': 'api', 'pcthispanic': 'hispanic',
                   'pctaian': 'native', 'pct2prace': 'multiple'}
    p_race_given_first_name_df = pd.read_csv(curr_path + '/resources/firstnames.csv', index_col='firstname').rename(columns=rename_dict)
    p_race_given_first_name_df.index = p_race_given_first_name_df.index.str.upper()
    p_race_given_first_name_df[races_columns] = p_race_given_first_name_df[races_columns] / 100.0
    return p_race_given_first_name_df[['count'] + races_columns]

# Used for gender, 'first_name' is index
male_first_names_frequency_df = read_census_first_names_file(
    '/resources/dist.male.first.txt')  # https://www2.census.gov/topics/genealogy/1990surnames/
female_first_names_frequency_df = read_census_first_names_file(
    '/resources/dist.female.first.txt')  # https://www2.census.gov/topics/genealogy/1990surnames/
all_first_names = np.unique(np.append(male_first_names_frequency_df.index, female_first_names_frequency_df.index))

p_race_given_first_name_df = read_p_race_given_first_name_file()


def get_p_gender_given_first_name_df() -> pd.DataFrame:
    # We use bayes rule: P(A|B) = P(B|A)*P(A)/P(B)
    p_gender_given_first_name_df = pd.DataFrame(index=all_first_names, columns=['male', 'female'])
    p_male = 0.5
    p_female = 1 - p_male
    first_names_df = p_gender_given_first_name_df.index.to_frame()
    p_names_given_male = first_names_df.join(male_first_names_frequency_df)['frequency']
    p_names_given_female = first_names_df.join(female_first_names_frequency_df)['frequency']
    p_first_name = (p_names_given_male * p_male).add(p_names_given_female * p_female, fill_value=0)
    p_gender_given_first_name_df['male'] = (p_names_given_male * p_male).div(p_first_name, axis=0).fillna(value=0)
    p_gender_given_first_name_df['female'] = (p_names_given_female * p_female).div(p_first_name, axis=0).fillna(value=0)
    return p_gender_given_first_name_df


def get_p_first_name_given_race_df():
    #p(first|race) = (p(race|first) * p(first)) / p(race)
    total_count = p_race_given_first_name_df['count'].sum()
    p_first_name = p_race_given_first_name_df['count'] / total_count
    p_race = p_race_given_first_name_df[races_columns].multiply(p_race_given_first_name_df['count'].values, axis=0).sum(axis=0).div(total_count)
    p_first_name_given_race_df = p_race_given_first_name_df[races_columns].multiply(p_first_name, axis=0).div(p_race, axis=1).fillna(value=0)
    return p_first_name_given_race_df


p_gender_given_first_name_df = get_p_gender_given_first_name_df()
p_first_name_given_race_df = get_p_first_name_given_race_df()

if "pytest" not in sys.modules:
    p_gender_given_first_name_df.to_csv('resources/p_gender_given_first_name.csv', index_label='first_name')
    p_race_given_first_name_df[races_columns].to_csv('resources/p_race_given_first_name.csv', index_label='first_name')
    p_first_name_given_race_df.to_csv('resources/p_first_name_given_race.csv', index_label='first_name')
