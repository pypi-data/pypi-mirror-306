import itertools
import json
import os

import matplotlib.pyplot as plt
import seaborn as sns
from common.common import prepare_directory


class FoldValidationReportGenerator:
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.reports_validation_directory = f'{self.root_directory}/reports/validation'
        self.reports_screens_directory = f'{self.root_directory}/reports/screens'
        prepare_directory(self.reports_screens_directory)
        self.validation_data = []

    def _load_validation_results(self):
        """Load validation results from JSON files."""
        for filename in os.listdir(self.reports_validation_directory):
            if filename.endswith('.json'):
                file_path = os.path.join(self.reports_validation_directory, filename)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    self.validation_data.append(data)

    def plot_all_runs(self, min_score=0.0, save_path=None):
        """Plot accumulated scores for all runs with a score above min_score."""
        sns.set_style('white')
        plt.figure(figsize=(14, 8))

        for entry in self.validation_data:
            if entry['score'] < min_score:
                continue

            validation_results = entry['validation_results']
            scores = []
            indices = []

            score = 0

            for idx, result in enumerate(validation_results):
                score += 1 if result['is_correct'] else -1
                scores.append(score)
                indices.append(idx)

            sns.lineplot(
                x=indices,
                y=scores,
                linewidth=0.5,
                marker=None,
                label=f"Run: {entry['run_id']} (Score: {entry['score']:.2f})"
            )

        plt.title(f'Validation Results (Score >= {min_score})', fontsize=16)
        plt.xlabel('Index', fontsize=14)
        plt.ylabel('Accumulated Score', fontsize=14)
        plt.legend(loc='best', fontsize='small')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300)
        plt.close()

    def plot_each_param_combination(self):
        """Plot scatter plots for each combination of parameters with color scale and size variation."""
        sns.set_style('white')
        all_params = self.get_all_params()
        param_combinations = list(itertools.combinations(all_params, 2))

        for x_param, y_param in param_combinations:
            x_values, y_values, scores = self.get_values_for_plot(x_param, y_param)

            if not x_values or not y_values:
                continue  # Skip if no data for this parameter combination

            # Create a figure and axes
            fig, ax = plt.subplots(figsize=(10, 6))

            scatter = ax.scatter(
                x_values,
                y_values,
                c=scores,
                cmap='coolwarm',
                s=[(abs(score) + 1) * 50 for score in scores],  # Размер меняется в зависимости от score
                alpha=0.8
            )
            ax.set_title(f'{x_param} vs {y_param}', fontsize=16)
            ax.set_xlabel(x_param, fontsize=14)
            ax.set_ylabel(y_param, fontsize=14)

            cbar = plt.colorbar(scatter, ax=ax)
            cbar.set_label('Score', fontsize=12)

            plt.tight_layout()

            save_path = os.path.join(self.reports_screens_directory, f'{x_param}_vs_{y_param}.png')
            plt.savefig(save_path, dpi=300)
            plt.close()

    def get_all_params(self):
        """Get a list of all unique parameter names."""
        params_set = set()
        for entry in self.validation_data:
            params = entry['params']
            params_set.update(params.keys())
        return list(params_set)

    def get_values_for_plot(self, x_param, y_param):
        """Extract values for plotting based on parameter names."""
        x_values = []
        y_values = []
        scores = []

        for entry in self.validation_data:
            params = entry['params']

            x_value = self.extract_param_value(params, x_param)
            y_value = self.extract_param_value(params, y_param)

            if x_value is not None and y_value is not None:
                x_values.append(x_value)
                y_values.append(y_value)
                scores.append(entry['score'])

        return x_values, y_values, scores

    def extract_param_value(self, params, param_name):
        """Extract a parameter value from params."""
        if param_name in params:
            value = params[param_name]
            if isinstance(value, list) and len(value) > 0:
                return ', '.join(map(str, value))
            if isinstance(value, (int, float, str)):
                return value
        return None

    def generate_all_reports(self, min_score=0.0):
        self._load_validation_results()
        all_runs_path = os.path.join(self.reports_screens_directory, 'all_runs.png')
        self.plot_all_runs(save_path=all_runs_path, min_score=min_score)
        self.plot_each_param_combination()
