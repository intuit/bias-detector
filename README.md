

[![codecov](https://codecov.io/gh/intuit/bias-detector/branch/main/graph/badge.svg)](https://codecov.io/gh/intuit/bias-detector)
[![CircleCI](https://circleci.com/gh/intuit/bias-detector.svg?style=shield)](https://circleci.com/gh/intuit/bias-detector)
[![License](https://img.shields.io/github/license/intuit/bias-detector)](https://raw.githubusercontent.com/intuit/bias-detector/master/LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/bias-detector)](https://pypi.org/project/bias-detector)
<!--[![PiPi stats](https://img.shields.io/pypi/dm/bias-detector.svg)](https://pypistats.org/packages/bias-detector)-->
<!--[![GitHub release](https://img.shields.io/github/release/intuit/bias-detector.svg)](https://github.com/intuit/bias-detector/releases)-->

# <img src="https://raw.githubusercontent.com/intuit/bias-detector/master/bias_detector/static/libra.svg" height="50" width="50"/> Bias Detector
[//]: # (description)
Bias Detector is a python package for detecting gender/race bias in binary classification models.

Based on first and last name/zip code the package analyzes the probability of the user belonging to different genders/races. Then, the model predictions per gender/race are compared using various bias metrics.

Using this package you will be able to gain insight into whether your model is biased or not, and if so, how much bias was found.

The Bias Detector is based on statistical data from the US and therefore should be used only with US originated data. We hope to support more countries in the future.

If you have any questions please [let us know](https://github.com/intuit/bias-detector/discussions).

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

**Create a bias detector instance:**

```
from bias_detector.BiasDetector import BiasDetector
bias_detector = BiasDetector(country='US')
```

**Generate bias report:** 

```
bias_report = bias_detector.get_bias_report(first_names=first_names, last_names=last_names, zip_codes=zip_codes, y_true=y_true, y_pred=y_pred)
```

**Visualize the bias report:** 

```
bias_report.plot_summary()
```

<img src="https://raw.githubusercontent.com/intuit/bias-detector/master/bias_detector/static/bias_report_summary_plot_statistical_parity.png" width="66%"/>
<img src="https://raw.githubusercontent.com/intuit/bias-detector/master/bias_detector/static/bias_report_summary_plot_equal_opportunity.png" width="66%"/>
<img src="https://raw.githubusercontent.com/intuit/bias-detector/master/bias_detector/static/bias_report_summary_plot_preditive_equality.png" width="66%"/>

```
bias_report.print_summary()
```

<ul><li>Statistical Parity:</li>We observed the following statistically significant differences (𝛼=0.01):<ul><li>P(pred=1|Male)-P(pred=1|Female)=0.55-0.49=0.053±0.026 (p-value=1e-07)</li></ul><li>Equal Opportunity:</li>We observed the following statistically significant differences (𝛼=0.01):<ul><li>TPR<sub>Male</sub>-TPR<sub>Female</sub>=0.56-0.51=0.047±0.036 (p-value=0.00097)</li></ul><li>Predictive Equality:</li>We observed the following statistically significant differences (𝛼=0.01):<ul><li>FPR<sub>Male</sub>-FPR<sub>Female</sub>=0.54-0.48=0.06±0.036 (p-value=2e-05)</li></ul></ul>

```
bias_report.plot_groups()
```

<img src="https://raw.githubusercontent.com/intuit/bias-detector/master/bias_detector/static/bias_report_gender_pie.png" width="66%" />
<img src="https://raw.githubusercontent.com/intuit/bias-detector/master/bias_detector/static/bias_report_race_pie.png" width="66%" />

**Show gender/race correlation with model features:**

```
bias_detector.get_features_groups_correlation(first_names=first_names, last_names=last_names, zip_codes=zip_codes, features=features)
```
Sample output from the [Titanic demo](https://github.com/intuit/bias-detector/blob/main/demos/titanic/titanic-bias-detection.ipynb):
<table>
    <thead>
    <tr>
        <th></th>
        <th>male_correlation</th>
        <th>female_correlation</th>
        <th>white_correlation</th>
        <th>black_correlation</th>
        <th>api_correlation</th>
        <th>hispanic_correlation</th>
        <th>native_correlation</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <th>ticket_class</th>
        <td>-0.243730</td>
        <td>0.010038</td>
        <td>-0.122978</td>
        <td>-0.152287</td>
        <td>0.128161</td>
        <td>-0.003452</td>
        <td>-0.029846</td>
    </tr>
    <tr>
        <th>age</th>
        <td>0.234712</td>
        <td>-0.168692</td>
        <td>0.165937</td>
        <td>-0.059513</td>
        <td>-0.044503</td>
        <td>-0.058893</td>
        <td>0.036010</td>
    </tr>
    <tr>
        <th>num_of_siblings_or_spouses_aboard</th>
        <td>0.027651</td>
        <td>0.025737</td>
        <td>0.029292</td>
        <td>0.066896</td>
        <td>-0.061708</td>
        <td>-0.072092</td>
        <td>0.138135</td>
    </tr>
    <tr>
        <th>num_of_parents_or_children_aboard</th>
        <td>0.057575</td>
        <td>0.042770</td>
        <td>0.048623</td>
        <td>0.099354</td>
        <td>-0.064993</td>
        <td>-0.100496</td>
        <td>0.064185</td>
    </tr>
    <tr>
        <th>fare</th>
        <td>0.053703</td>
        <td>0.071300</td>
        <td>0.076330</td>
        <td>0.061158</td>
        <td>-0.001893</td>
        <td>-0.067631</td>
        <td>0.058121</td>
    </tr>
    <tr>
        <th>embarked_Cherbourg</th>
        <td>-0.073627</td>
        <td>-0.013599</td>
        <td>-0.093890</td>
        <td>-0.075407</td>
        <td>-0.007720</td>
        <td>0.124144</td>
        <td>-0.020478</td>
    </tr>
    <tr>
        <th>embarked_Queenstown</th>
        <td>-0.019206</td>
        <td>0.169752</td>
        <td>0.110737</td>
        <td>-0.049664</td>
        <td>-0.049379</td>
        <td>0.011407</td>
        <td>-0.054550</td>
    </tr>
    <tr>
        <th>embarked_Southampton</th>
        <td>0.082538</td>
        <td>-0.090631</td>
        <td>0.011149</td>
        <td>0.100265</td>
        <td>0.038108</td>
        <td>-0.116438</td>
        <td>0.050909</td>
    </tr>
    <tr>
        <th>sex_female</th>
        <td>-0.327044</td>
        <td>0.615262</td>
        <td>0.047330</td>
        <td>0.073640</td>
        <td>-0.051959</td>
        <td>0.074259</td>
        <td>0.011737</td>
    </tr>
    <tr>
        <th>sex_male</th>
        <td>0.327044</td>
        <td>-0.615262</td>
        <td>-0.047330</td>
        <td>-0.073640</td>
        <td>0.051959</td>
        <td>-0.074259</td>
        <td>-0.011737</td>
    </tr>
    </tbody>
</table>

**Fuzzy extraction of first/last names from emails:**

```
bias_detector.fuzzily_get_emails_full_names(emails)
```

This method will return a DataFrame with first_name and last_name columns fuzzily extracted from the users emails. Note that the accuracy of this method varies between emails and data sets.

Sample output for synthetic emails:

<table>
    <thead>
    <tr>
        <th>email</th>
        <th>first_name</th>
        <th>last_name</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <th>holleybeverly@gmail.com</th>
        <td>holley</td>
        <td>beverly</td>
    </tr>
    <tr>
        <th>breweradrienne@gmail.com</th>
        <td>adrienne</td>
        <td>brewer</td>
    </tr>
    <tr>
        <th>craigreed@gmail.com</th>
        <td>craig</td>
        <td>reed</td>
    </tr>
    <tr>
        <th>battagliahenry@gmail.com</th>
        <td>henry</td>
        <td>battaglia</td>
    </tr>
    <tr>
        <th>apaget@gmail.com</th>
        <td></td>
        <td>paget</td>
    </tr>
    <tr>
        <th>briana@gmail.com</th>
        <td>briana</td>
        <td></td>
    </tr>
    <tr>
        <th>apena@gmail.com</th>
        <td></td>
        <td>pena</td>
    </tr>
    <tr>
        <th>jacka@gmail.com</th>
        <td></td>
        <td>jacka</td>
    </tr>
    <tr>
        <th>mattiea@gmail.com</th>
        <td>mattie</td>
        <td></td>
    </tr>
    <tr>
        <th>patricia_calder@gmail.com</th>
        <td>patricia</td>
        <td>calder</td>
    </tr>
    </tbody>
</table>


### Contributing

See [CONTRIBUTING.md](https://github.com/intuit/bias-detector/blob/main/CONTRIBUTING.md).

### References 
1. NINAREH MEHRABI, FRED MORSTATTER, NRIPSUTA SAXENA, KRISTINA LERMAN, and ARAM GALSTYAN, 2019. A Survey on Bias and Fairness in Machine Learning.
2. Moritz Hardt, Eric Price, Nathan Srebro, 2016. Equality of Opportunity in Supervised Learning.
3. Ioan Voicu (2018) Using First Name Information to Improve Race and Ethnicity Classification, Statistics and Public Policy, 5:1, 1-13, DOI: 10.1080/2330443X.2018.1427012

