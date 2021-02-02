
from bias_detector.common import *


class FirstNameModel:

    def get_probabilities(self, first_names):
        first_names_probs = first_names.to_frame().merge(
            p_race_given_first_name_df,
            left_on='first_name',
            right_index=True,
            how='left',
        )
        return first_names_probs
