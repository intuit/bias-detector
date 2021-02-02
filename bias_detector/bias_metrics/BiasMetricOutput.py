from typing import Sequence

import pandas as pd


class BiasMetricOutput:

    def __init__(self, results: pd.Series) -> None:
        self.results = results
