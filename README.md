

[![codecov](https://codecov.io/gh/intuit/bias-detector/branch/main/graph/badge.svg)](https://codecov.io/gh/intuit/bias-detector)
[![CircleCI](https://circleci.com/gh/intuit/bias-detector.svg?style=shield)](https://circleci.com/gh/intuit/bias-detector)
[![GitHub release](https://img.shields.io/github/release/intuit/bias-detector.svg)](https://github.com/intuit/bias-detector/releases)
[![GitHub issues](https://img.shields.io/github/issues/intuit/bias-detector)](https://github.com/intuit/bias-detector/issues)
[![License](https://img.shields.io/github/license/intuit/bias-detector)](https://github.com/intuit/bias-detector/blob/main/LICENSE)
<!--[![PyPI version](https://badge.fury.io/py/bias-detector.svg)](https://badge.fury.io/py/bias-detector)-->

# <img src="https://github.com/intuit/bias-detector/blob/main/bias_detector/static/libra.svg" height="50" width="50"/> Bias Detector
[//]: # (description)
Bias Detector is a python package for detecting gender/race bias in binary classification models.

Based on first and last name/zip code the package analyzes the probability of the user belonging to different genders/races. Then, the model predictions per gender/race are compared using various bias metrics.

Using this package you would be able to get insight on whether your model is biased or not and how much.

The Bias Detector is based on statistical data from the US and therefore should be used only with US originated data. We hope to support more countries in the future.

We can be contacted on Stack Overflow using the bias-detector tag. 
We would appreciate your feedback!

### Supported Metrics
There are many metrics which can possibly be used to detect Bias, we currently support the following three:
1. Statistical Parity - tests whether the probability of 2 groups to be classified as belonging to the positive class by the model is equal.
2. Equal Opportunity - tests whether the True Positive Rates of 2 groups are equal (how likely is the model to predict correctly the positive class for each group).
2. Predictive Equality - tests whether there False Positive Rates of 2 groups are equal (how likely is the model to predict incorrectly the positive class for each group).

### Usage

**Install the package**

```
!pip install bias-detector
```

**Calculate bias metrics based on users data, y_true and y_pred:** 

```
from bias_detector.BiasDetector import BiasDetector
bias_report = BiasDetector(country='US').get_bias_report(first_names=first_names, last_names=last_names, zip_codes=zip_codes, y_true=y_true, y_pred=y_pred)
bias_report.plot_summary()
```

**Example for the report output:** 

**bias_report.plot_summary()**

<p float="left" width="100%">
    <img src="https://github.com/intuit/bias-detector/blob/main/bias_detector/static/bias_report_summary_plot_statistical_parity.png" width="30%" />
    <img src="https://github.com/intuit/bias-detector/blob/main/bias_detector/static/bias_report_summary_plot_equal_opportunity.png" width="30%" />
    <img src="https://github.com/intuit/bias-detector/blob/main/bias_detector/static/bias_report_summary_plot_preditive_equality.png" width="30%" />
</p>

**bias_report.print_summary()**

<ul><li>Statistical Parity:</li>We observed the following statistically significant differences:<ul><li>P(pred=1|Male)-P(pred=1|Female)=0.55-0.49=0.053±0.026 (𝛼=0.01,p-value=1e-07)</li></ul><li>Equal Opportunity:</li>We observed the following statistically significant differences:<ul><li>TPR<sub>Male</sub>-TPR<sub>Female</sub>=0.56-0.51=0.047±0.036 (𝛼=0.01,p-value=0.00097)</li></ul><li>Predictive Equality:</li>We observed the following statistically significant differences:<ul><li>FPR<sub>Male</sub>-FPR<sub>Female</sub>=0.54-0.48=0.06±0.036 (𝛼=0.01,p-value=2e-05)</li></ul></ul>

**bias_report.plot_groups()**

<p float="left" width="100%">
  <img src="https://github.com/intuit/bias-detector/blob/main/bias_detector/static/bias_report_gender_pie.png" width="30%" />
  <img src="https://github.com/intuit/bias-detector/blob/main/bias_detector/static/bias_report_race_pie.png" width="30%" />
</p>

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

### References 
1. NINAREH MEHRABI, FRED MORSTATTER, NRIPSUTA SAXENA, KRISTINA LERMAN, and ARAM GALSTYAN, 2019. A Survey on Bias and Fairness in Machine Learning.
2. Moritz Hardt, Eric Price, Nathan Srebro, 2016. Equality of Opportunity in Supervised Learning.
3. Ioan Voicu (2018) Using First Name Information to Improve Race and Ethnicity Classification, Statistics and Public Policy, 5:1, 1-13, DOI: 10.1080/2330443X.2018.1427012

