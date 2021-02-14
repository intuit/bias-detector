
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from bias_detector.BiasConfidence import BiasConfidence
from bias_detector.BiasMetric import get_bias_metric_description, get_bias_metric, get_bias_metric_short_description
from bias_detector.common import get_p_others, get_other_groups_names, races


class BiasReport:

    def __init__(self,
                 bias_metrics_results: pd.DataFrame,
                 estimated_groups_sizes: pd.Series,
                 y_true: pd.Series,
                 y_pred: pd.Series,
                 y_scores: pd.Series,
                 privileged_race: str,
                 p_groups: pd.DataFrame,
                 detect_gender_bias: bool,
                 detect_race_bias: bool) -> None:
        self.bias_metrics_results = bias_metrics_results
        self.estimated_groups_sizes = estimated_groups_sizes
        self.y_true = y_true
        self.y_pred = y_pred
        self.y_scores = y_scores
        self.privileged_race = privileged_race
        self.p_groups = p_groups
        self.detect_gender_bias = detect_gender_bias
        self.detect_race_bias = detect_race_bias

    def plot_groups(self) -> None:
        if self.detect_race_bias:
            race_group_sizes = self.estimated_groups_sizes[races + ['race_unknown']]
            race_group_percentages = pd.Series(race_group_sizes.values / race_group_sizes.sum()).apply(lambda fraction: '{fraction:.2%}'.format(fraction=fraction))
            if len(race_group_sizes) > 0:
                plt.title('Race estimated groups sizes')
                plt.pie(race_group_sizes.values)
                plt.legend(labels=race_group_sizes.index.values + ' - ' + race_group_percentages)
                plt.show()
        if self.detect_gender_bias:
            gender_group_sizes = self.estimated_groups_sizes[['male', 'female', 'gender_unknown']]
            gender_group_percentages = pd.Series(gender_group_sizes.values / gender_group_sizes.sum()).apply(lambda fraction: '{fraction:.2%}'.format(fraction=fraction))
            if len(gender_group_sizes) > 0:
                plt.title('Gender estimated groups sizes')
                plt.pie(gender_group_sizes.values)
                plt.legend(labels=gender_group_sizes.index.values + ' - ' + gender_group_percentages)
                plt.show()

    def plot_y_pred(self) -> None:
        for group_name in self.bias_metrics_results.columns:
            if group_name == 'female':
                continue
            group = self.p_groups[group_name]
            others = get_p_others(self.p_groups, group_name, self.privileged_race)
            group_title, others_title = self.get_titles(group_name)
            if self.y_pred is not None:
                plt.title('y_pred distribution by {group_title}/{others_title} classes'.format(
                    group_title=group_title, others_title=others_title))
                pos_pred_group_size = (self.y_pred == 1).multiply(group).sum()
                pos_pred_others_size = (self.y_pred == 1).multiply(others).sum()
                neg_pred_group_size = (self.y_pred == 0).multiply(group).sum()
                neg_pred_others_size = (self.y_pred == 0).multiply(others).sum()
                plt.bar(x=[0, 1], height=[neg_pred_group_size/group.sum(), pos_pred_group_size/group.sum()], label=group_title, alpha=0.5, width=0.1)
                plt.bar(x=[0, 1], height=[neg_pred_others_size/others.sum(), pos_pred_others_size/others.sum()], label=others_title, alpha=0.5, width=0.1)
                plt.legend()
                plt.xlabel('y_pred')
                plt.ylabel('density')
                plt.show()

    def plot_y_scores(self) -> None:
        for group_name in self.bias_metrics_results.columns:
            if group_name == 'female':
                continue
            group = self.p_groups[group_name]
            others = get_p_others(self.p_groups, group_name, self.privileged_race)
            group_title, others_title = self.get_titles(group_name)
            if self.y_scores is not None:
                plt.title('y_scores distribution by {group_label}/{others_label} classes'.format(
                    group_label=group_title, others_label=others_title))
                bucket_count = 20
                bucket_size = 1 / bucket_count
                buckets = [i * bucket_size for i in range(0, bucket_count)]
                normalized_group_sizes = []
                normalized_others_sizes = []
                for bucket in buckets:
                    bucket_scores = ((self.y_scores >= bucket) & (self.y_scores < bucket + bucket_size))
                    normalized_group_sizes.append(bucket_scores.multiply(group).sum()/group.sum())
                    normalized_others_sizes.append(bucket_scores.multiply(others).sum()/others.sum())
                plt.bar(x=np.array(buckets) + bucket_size / 2, height=normalized_group_sizes, label=group_title, alpha=0.5, width=bucket_size)
                plt.bar(x=np.array(buckets) + bucket_size / 2, height=normalized_others_sizes, label=others_title, alpha=0.5, width=bucket_size)
                plt.legend()
                plt.xlabel('y_score')
                plt.ylabel('density')
                plt.show()

    def get_titles(self, group_name):
        group_title = group_name.replace('_', ' ').title()
        other_groups_names = get_other_groups_names(group_name, self.privileged_race)
        others_title = other_groups_names[0].replace('_', ' ').title() if len(other_groups_names) == 1 else 'Others'
        group_title = group_title if group_title != 'Api' else 'API'
        others_title = others_title if others_title != 'Api' else 'API'
        return group_title, others_title

    def plot_summary(self) -> dict:
        for bias_metric in self.bias_metrics_results.index:
            bias_metric_title = bias_metric.replace('_', ' ').title()
            results = self.bias_metrics_results.loc[bias_metric]
            x_labels = []
            bar_results = []
            for group_name in results.index:
                if group_name == 'female':
                    continue
                group_title, others_title = self.get_titles(group_name)
                x_labels.append(group_title + '\n' + others_title)
                bar_results.append(results[group_name])

            fig, ax = plt.subplots()
            bar_width = 0.2
            index = np.arange(len(bar_results))
            group_colors = []
            others_colors = []
            for i, r in enumerate(bar_results):
                confidence = r.bias_confidence
                if confidence is None or confidence.p_value > BiasConfidence.alpha:
                    group_colors.append('lightsteelblue')
                    others_colors.append('bisque')
                else:
                    group_colors.append('tab:blue')
                    others_colors.append('tab:orange')
            group_bar = ax.bar(x=index, height=[r.group_p for r in bar_results], width=bar_width, color=group_colors)
            others_bar = ax.bar(x=index+bar_width, height=[r.others_p for r in bar_results], width=bar_width, color=others_colors)
            ax.set_xticks(index + bar_width / 2)
            ax.set_xticklabels(x_labels)
            ax.set_ylabel(get_bias_metric_short_description(get_bias_metric(bias_metric)))
            biased = np.any([r.bias_confidence is not None and r.bias_confidence.p_value <= BiasConfidence.alpha for r in bar_results])
            for i, r in enumerate(bar_results):
                confidence = r.bias_confidence
                if confidence is None or confidence.p_value > BiasConfidence.alpha:
                    continue
                interval = confidence.get_interval()
                plt.plot((i+(bar_width/2), i+(bar_width/2)), (min(r.group_p, r.others_p) + interval/2, max(r.group_p, r.others_p) - interval/2), 'r_-', color='black')
            if biased:
                percents = int((1 - BiasConfidence.alpha) * 100)
                plt.title(bias_metric_title + '\n\n' + 'Intervals represents the {percents}% confidence min difference'.format(percents=percents))
            else:
                plt.title(bias_metric_title + '\n\n' + 'No bias detected')
            plt.xticks(rotation=90)
            plt.show()

    def get_summary(self) -> dict:
        summary = {}
        for bias_metric in self.bias_metrics_results.index:
            groups_alerts = []
            bias_metric_formatted = bias_metric.replace('_', ' ').title()
            summary[bias_metric_formatted] = groups_alerts
            results = self.bias_metrics_results.loc[bias_metric]
            for group_name in results.index:
                if group_name == 'female':
                    continue
                result = results[group_name]
                confidence = result.bias_confidence
                if result is not None and confidence is not None and type(confidence) == BiasConfidence and confidence.p_value <= BiasConfidence.alpha:
                    group_title, others_title = self.get_titles(group_name)
                    group_metric_description = get_bias_metric_description(get_bias_metric(bias_metric), group_title)
                    others_metric_description = get_bias_metric_description(get_bias_metric(bias_metric), others_title)
                    group_alert = '{group_metric_description}-{others_metric_description}={group_p:.2}-{others_p:.2}={diff:.2}±{ci:.2} (p-value={p_value:.2})'.format(
                        group_metric_description=group_metric_description,
                        others_metric_description=others_metric_description,
                        diff=result.get_diff(),
                        ci=confidence.get_interval(),
                        group_p=result.group_p,
                        others_p=result.others_p,
                        p_value=confidence.p_value)
                    groups_alerts.append(group_alert)
        return summary

    def print_summary(self):
        from IPython.core.display import display, HTML
        display(HTML(self.get_summary_html()))

    def get_summary_html(self):
        summary = self.get_summary()
        formatted_summary = '''<b>Report Summary:</b>'''
        formatted_summary += '''<ul>'''
        for bias_metric_title, groups_alerts in summary.items():
            formatted_summary += '''<li>{bias_metric_title}:</li>'''.format(bias_metric_title=bias_metric_title)
            if len(groups_alerts) == 0:
                formatted_summary += '''No bias detected.'''
            else:
                formatted_summary += 'We observed the following statistically significant differences (𝛼={alpha:.2}):'\
                    .format(alpha=BiasConfidence.alpha)
                formatted_summary += '''<ul>'''
                for group_alert in groups_alerts:
                    formatted_summary += '''<li>{group_alert}</li>'''.format(group_alert=group_alert)
                formatted_summary += '''</ul>'''
        formatted_summary += '''</ul>'''
        return formatted_summary

    def get_bias_metrics_results(self):
        return self.bias_metrics_results

    def get_estimated_groups_sizes(self):
        return self.estimated_groups_sizes

    def get_p_groups(self):
        return self.p_groups
