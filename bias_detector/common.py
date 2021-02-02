
import pandas as pd
from typing import Sequence
import os
import numpy as np
import surgeo

races = ['white', 'black', 'api', 'hispanic', 'native']
curr_path = os.path.dirname(os.path.realpath(__file__)) if '__file__' in globals() else os.getcwd()


def read_p_groups_file(name, index_col):
    return pd.read_csv(curr_path + '/resources/{name}'.format(name=name), index_col=index_col, keep_default_na=False).apply(pd.to_numeric, errors='coerce')


p_gender_given_first_name_df = read_p_groups_file('p_gender_given_first_name.csv', index_col='first_name')
p_race_given_first_name_df = read_p_groups_file('p_race_given_first_name.csv', index_col='first_name')
p_first_name_given_race_df = read_p_groups_file('p_first_name_given_race.csv', index_col='first_name')

all_first_names = np.unique(p_gender_given_first_name_df.index.str.lower())
# Used to find names in email addresses
all_first_names_long_to_short = sorted(all_first_names, key=len, reverse=True)
all_first_names_set = set(all_first_names)
longest_first_name_len = len(all_first_names_long_to_short[0])
shortest_first_name_len = len(all_first_names_long_to_short[-1])
# Used for race, 'last_name' and 'first_name' are indexes, respectively
last_name_model = surgeo.SurnameModel()
all_last_names_long_to_short = sorted(last_name_model._PROB_RACE_GIVEN_SURNAME.index.str.lower(), key=len, reverse=True)
all_last_names_set = set(all_last_names_long_to_short)
longest_last_name_len = len(all_last_names_long_to_short[0])
shortest_last_name_len = len(all_last_names_long_to_short[-1])


def get_p_others(groups: pd.DataFrame, group_name: str, privileged_race: str) -> pd.Series:
    other_groups_names = get_other_groups_names(group_name, privileged_race)
    return groups[other_groups_names].sum(axis=1)


def get_other_groups_names(group_name: str, privileged_race: str) -> Sequence[str]:
    if group_name == 'male':
        return ['female']
    elif group_name == 'female':
        return ['male']
    elif group_name in races:
        if privileged_race is None or group_name == privileged_race:
            return [race for race in races if race != group_name]
        else:
            return [privileged_race]
