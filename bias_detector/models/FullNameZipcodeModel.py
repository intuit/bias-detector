from surgeo.models.base_model import BaseModel

from bias_detector.common import *
import pandas as pd
import surgeo
import pathlib


class FullNameZipcodeModel(BaseModel):

    def __init__(self):
        super().__init__()
        self._package_root = pathlib.Path(surgeo.__file__).parents[0]
        self._PROB_RACE_GIVEN_SURNAME = self._get_prob_race_given_surname()
        self._PROB_ZCTA_GIVEN_RACE = self._get_prob_zcta_given_race()

    def get_probabilities(self, first_names, last_names, zip_codes):
        first_names_probs = self._get_first_names_probs(first_names)
        last_names_probs = self._get_last_names_probs(last_names)
        zip_codes_probs = self._get_zip_codes_probs(zip_codes)
        names_zip_codes_probs = self._combined_probs(first_names_probs, last_names_probs, zip_codes_probs)
        result = self._adjust_frame(
            first_names_probs,
            last_names_probs,
            zip_codes_probs,
            names_zip_codes_probs
        )
        return result

    #See: https://www.tandfonline.com/doi/full/10.1080/2330443X.2018.1427012
    def _combined_probs(self,
                        first_names_probs: pd.DataFrame,
                        last_name_probs: pd.DataFrame,
                        zip_code_probs: pd.DataFrame) -> pd.DataFrame:
        names_zip_codes_numer = last_name_probs.iloc[:, 1:] * first_names_probs.iloc[:, 1:] * zip_code_probs.iloc[:, 1:]
        names_zip_codes_denom = names_zip_codes_numer.sum(axis=1)
        names_zip_codes_probs = names_zip_codes_numer.div(names_zip_codes_denom, axis=0)
        return names_zip_codes_probs

    def _adjust_frame(self,
                      first_names_probs: pd.DataFrame,
                      last_names_probs: pd.DataFrame,
                      zip_codes_probs: pd.DataFrame,
                      names_zip_codes_probs: pd.DataFrame) -> pd.DataFrame:
        names_zip_codes_data = pd.concat([
            first_names_probs['first_name'].to_frame(),
            last_names_probs['last_name'].to_frame(),
            zip_codes_probs['zip_code'].to_frame(),
            names_zip_codes_probs
        ], axis=1)
        return names_zip_codes_data

    def _get_last_names_probs(self,
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

    def _get_zip_codes_probs(self, zip_codes: pd.Series) -> pd.DataFrame:
        zip_codes_probs = zip_codes.to_frame().merge(
            self._PROB_ZCTA_GIVEN_RACE,
            left_on='zip_code',
            right_index=True,
            how='left',
        )
        return zip_codes_probs
