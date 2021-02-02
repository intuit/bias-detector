from typing import Sequence

import pandas as pd


class BiasMetricInput:

    def __init__(self, p_groups: pd.DataFrame,
                 y_true: pd.Series,
                 y_pred: pd.Series,
                 y_scores: pd.Series,
                 privileged_race: str = None) -> None:
        self.y_true = y_true
        self.y_pred = y_pred
        self.y_scores = y_scores
        self.p_groups = p_groups
        self.privileged_race = privileged_race
