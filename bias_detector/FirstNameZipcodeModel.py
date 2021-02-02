from surgeo.models.base_model import BaseModel

from bias_detector.common import *
import pandas as pd
import surgeo
import pathlib


class FirstNameZipcodeModel(BaseModel):

    def __init__(self):
        super().__init__()
        self._package_root = pathlib.Path(surgeo.__file__).parents[0]
        self._PROB_ZCTA_GIVEN_RACE = self._get_prob_zcta_given_race()

    def get_probabilities(self, first_names, zip_codes):
        first_names_probs = self._get_first_names_probs(first_names)
        zip_codes_probs = self._get_zip_codes_probs(zip_codes)
        first_names_zip_codes_probs = self._combined_probs(first_names_probs, zip_codes_probs)
        result = self._adjust_frame(
            first_names_probs,
            zip_codes_probs,
            first_names_zip_codes_probs
        )
        return result

    def _combined_probs(self,
                        first_names_probs: pd.DataFrame,
                        zip_code_probs: pd.DataFrame) -> pd.DataFrame:
        first_names_zip_codes_numer = first_names_probs.iloc[:, 1:] * zip_code_probs.iloc[:, 1:]
        first_names_zip_codes_denom = first_names_zip_codes_numer.sum(axis=1)
        first_names_zip_codes_probs = first_names_zip_codes_numer.div(first_names_zip_codes_denom, axis=0)
        return first_names_zip_codes_probs

    def _adjust_frame(self,
                      first_names_probs: pd.DataFrame,
                      zip_codes_probs: pd.DataFrame,
                      first_names_zip_codes_probs: pd.DataFrame) -> pd.DataFrame:
        names_zip_codes_data = pd.concat([
            first_names_probs['first_name'].to_frame(),
            zip_codes_probs['zip_code'].to_frame(),
            first_names_zip_codes_probs
        ], axis=1)
        return names_zip_codes_data

    def _get_first_names_probs(self,
                           first_names: pd.Series) -> pd.DataFrame:
        first_names_probs = first_names.to_frame().merge(
            p_race_given_first_name_df,
            left_on='first_name',
            right_index=True,
            how='left',
        )
        return first_names_probs

    def _get_zip_codes_probs(self, zip_codes: pd.Series) -> pd.DataFrame:
        zip_codes_probs = zip_codes.to_frame().merge(
            self._PROB_ZCTA_GIVEN_RACE,
            left_on='zip_code',
            right_index=True,
            how='left',
        )
        return zip_codes_probs
