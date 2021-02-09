import pathlib

from surgeo.models.base_model import BaseModel

from bias_detector.common import *
import pandas as pd


class FullNameModel(BaseModel):

    def __init__(self):
        super().__init__()
        self._package_root = pathlib.Path(surgeo.__file__).parents[0]
        self._PROB_RACE_GIVEN_SURNAME = self._get_prob_race_given_surname()

    def get_probabilities(self, first_names, last_names):
        first_names_probs = self._get_first_names_probs(first_names)
        last_names_probs = self._get_last_name_probs(last_names)
        full_names_probs = self._combined_probs(first_names_probs, last_names_probs)
        result = self._adjust_frame(
            first_names_probs,
            last_names_probs,
            full_names_probs,
        )
        return result

    def _combined_probs(self,
                        first_names_probs: pd.DataFrame,
                        last_names_probs: pd.DataFrame) -> pd.DataFrame:
        full_names_numer = last_names_probs.iloc[:, 1:] * first_names_probs.iloc[:, 1:]
        full_names_denom = full_names_numer.sum(axis=1)
        full_names_probs = full_names_numer.div(full_names_denom, axis=0)
        return full_names_probs

    def _adjust_frame(self,
                      first_names_probs: pd.DataFrame,
                      last_names_probs: pd.DataFrame,
                      full_name_probs: pd.DataFrame) -> pd.DataFrame:
        full_name_data = pd.concat([
            first_names_probs['first_name'].to_frame(),
            last_names_probs['last_name'].to_frame(),
            full_name_probs
        ], axis=1)
        return full_name_data

    def _get_last_name_probs(self,
                           last_names: pd.Series) -> pd.DataFrame:
        last_names_probs = last_names.to_frame().merge(
            self._PROB_RACE_GIVEN_SURNAME,
            left_on='last_name',
            right_index=True,
            how='left',
        )
        return last_names_probs

    def _get_first_names_probs(self, first_names: pd.Series) -> pd.DataFrame:
        first_names_probs = first_names.to_frame().merge(
            p_first_name_given_race_df,
            left_on='first_name',
            right_index=True,
            how='left',
        )
        return first_names_probs
