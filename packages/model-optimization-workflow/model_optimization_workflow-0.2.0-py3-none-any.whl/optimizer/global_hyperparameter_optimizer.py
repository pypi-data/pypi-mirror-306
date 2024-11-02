import itertools

import optuna


class GlobalHyperparameterOptimizer:
    def __init__(self, config):
        self.config = config
        optimizer_config = self.config['hyperparameter_optimizer']
        self.patience = optimizer_config['patience']
        self.tolerance = optimizer_config['tolerance']
        self.storage_url = optimizer_config['storage_url']
        self.study_name = optimizer_config['study_name']
        self.direction = optimizer_config['direction']
        self.best_metric = None
        self.no_improvement_count = 0

        self.study = optuna.create_study(
            study_name=self.study_name,
            storage=self.storage_url,
            direction=self.direction,
            load_if_exists=True
        )

    def suggest_parameters(self):
        if self.no_improvement_count >= self.patience:
            return None, None

        trial = self.study.ask()
        params = {
            'instruments': self._suggest_instruments(trial),
            'aggregation_window': trial.suggest_categorical(
                'aggregation_window',
                self.config['assembler']['aggregation_window']),
            'training_window_length': trial.suggest_categorical(
                'training_window_length',
                self.config['assembler']['dataset_labeler']['parameters']['training_window_length']),
            'prediction_window_length': trial.suggest_categorical(
                'prediction_window_length',
                self.config['assembler']['dataset_labeler']['parameters']['prediction_window_length']),
            'indicators': self._suggest_indicator_params(trial),
            'containers_params': self._suggest_model_container_params(trial),
            'total_folds': trial.suggest_categorical(
                'total_folds',
                self.config['workflow']['total_folds'])
        }
        return params, trial

    def _suggest_model_container_params(self, trial):
        model_containers = self.config['workflow']['model_containers']
        model_params = {}
        for container in model_containers:
            container_name = container['name']
            parameters = container.get('parameters', {}).copy()
            parameters.pop('class', None)
            parameters.pop('fold_from', None)
            parameters.pop('fold_to', None)
            for param_name, param_values in parameters.items():
                suggestion_name = f"container_{container_name}_{param_name}"
                model_params[suggestion_name] = trial.suggest_categorical(
                        suggestion_name, param_values)
        return model_params

    def _suggest_instruments(self, trial):
        assembler_config = self.config['assembler']
        available_instruments = assembler_config['instruments']
        instruments = []
        for instrument in available_instruments:
            include = trial.suggest_categorical(f"include_{instrument}", [True, False])
            if include:
                instruments.append(instrument)
        return instruments

    def _suggest_indicator_params(self, trial):
        indicators_config = self.config['assembler']['indicators']
        indicators_params = {}
        for indicator_config in indicators_config:
            indicator_name = 'indicator_' + indicator_config['class'].__name__
            indicators_params[indicator_name] = trial.suggest_categorical(
                indicator_name, indicator_config['parameters']['window_length'])
        return indicators_params

    def report_result(self, trial, metric):
        self.study.tell(trial, metric)

        if self.best_metric is None or metric > self.best_metric + self.tolerance:
            self.best_metric = metric
            self.no_improvement_count = 0
        else:
            self.no_improvement_count += 1

    def passed(self,trial):
        self.study.tell(trial,  float('-inf'))

    def print_final_results(self):
        trial_count = len(self.study.trials)
        best_trial = self.study.best_trial

        indicators_params = {}
        for key, value in best_trial.params.items():
            if key.startswith("indicator_"):
                parts = key.split('_')
                indicator_class_name = parts[1]
                param_name = '_'.join(parts[2:])
                if indicator_class_name not in indicators_params:
                    indicators_params[indicator_class_name] = {}
                indicators_params[indicator_class_name][param_name] = value

        model_params = {}
        for key, value in best_trial.params.items():
            if key.startswith("container_"):
                parts = key.split('_')
                container_name = parts[1]
                param_name = '_'.join(parts[2:])
                if container_name not in model_params:
                    model_params[container_name] = {}
                model_params[container_name][param_name] = value

        instruments = [
            instrument
            for instrument in self.config['assembler']['instruments']
            if best_trial.params.get(f"include_{instrument}", False)
        ]

        formatted_params = {
            'instruments': instruments,
            'aggregation_window': best_trial.params['aggregation_window'],
            'training_window_length': best_trial.params['training_window_length'],
            'prediction_window_length': best_trial.params['prediction_window_length'],
            'indicators': indicators_params,
            'containers_params': model_params,
            'total_folds': best_trial.params['total_folds']
        }

        print(f"Optimization complete!")
        print(f"Total trials: {trial_count}")
        print(f"Best trial value (metric): {best_trial.value}")
        print(f"Best trial parameters:")
        print(formatted_params)
