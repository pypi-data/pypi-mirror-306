import numpy as np
import pandas as pd
from sklearn.model_selection import RandomizedSearchCV, cross_val_score
from scipy.stats import uniform, randint
import random
from sklearn.utils._testing import ignore_warnings
import sys
import os

import warnings
warnings.filterwarnings('ignore')

from sklearn.metrics import (
    # Classification metrics
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    # Regression metrics
    mean_squared_error, mean_absolute_error, r2_score,
    make_scorer
)

from .data_cleaner import DataCleaner
from .data_preprocessor import DataPreprocessor
from .config import HyperparameterConfigParser

DEFAULT_METRICS = {
    'classification': ['accuracy', 'precision', 'recall', 'f1'],
    'regression': ['r2', 'neg_mean_squared_error', 'neg_mean_absolute_error']
}

class EnhancedSequentialOptimizer:
    """Enhanced Sequential Optimizer with support for both classification and regression"""

    def __init__(
        self,
        task_type,  # 'classification' or 'regression'
        target_column=None,
        scoring_metrics=None,
        generations=5,
        cv_folds=5,
        random_state=42,
        n_jobs=-1,
        refit_metric=None,
        verbosity=0,
        categorical_threshold=10
    ):
        # Validate task type
        if task_type not in ['classification', 'regression']:
            raise ValueError("task_type must be either 'classification' or 'regression'")

        self.task_type = task_type

        print("Task Type is ", task_type)

        # Hardcode the configuration file path
        config_path = 'hyperparam_config.json'

        # Initialize hyperparameter config parser
        config_parser = HyperparameterConfigParser(config_path)
        config_parser.parse_config_file()

        # Get configurations based on task type
        if task_type == 'classification':
            self.model_configs = config_parser.classification_config
        else:
            self.model_configs = config_parser.regression_config

        # Print configurations if verbosity is enabled
        if verbosity >= 2:
            print("\nLoaded Model Configurations:")
            for model_name, config in self.model_configs.items():
                print(f"\n{model_name}:")
                print(f"Model Class: {config['model_class'].__name__}")
                print("Parameters:")
                for param, values in config['params'].items():
                    print(f"  {param}: {values}")

        self.target_column = target_column
        self.generations = generations
        self.cv_folds = cv_folds
        self.random_state = random_state
        self.n_jobs = n_jobs
        self.verbosity = verbosity
        self.categorical_threshold = categorical_threshold
        self.n_classes = None 

        # Initialize preprocessor
        self.preprocessor = DataPreprocessor(categorical_threshold=categorical_threshold)

        if scoring_metrics is None:
            scoring_metrics = DEFAULT_METRICS[task_type]

        # Ensure scoring_metrics is a list
        if isinstance(scoring_metrics, str):
            scoring_metrics = [scoring_metrics]

        self.scoring = scoring_metrics
        self.refit = refit_metric if refit_metric else scoring_metrics[0]

        random.seed(random_state)
        np.random.seed(random_state)

        # Initialize best models and scores dictionaries
        self.best_models = {metric: None for metric in scoring_metrics}
        self.best_params = {metric: None for metric in scoring_metrics}
        self.best_scores = {metric: -np.inf for metric in scoring_metrics}

        self.results_ = {}
        self.detailed_results_ = {}
    
    def _get_scorer(self, metric_name):
        """Get the appropriate scorer function based on metric name"""
        if self.task_type == 'classification':
            scorers = {
                'accuracy': accuracy_score,
                'precision': lambda y_true, y_pred: precision_score(y_true, y_pred, zero_division=1, average='macro'),
                'f1': lambda y_true, y_pred: f1_score(y_true, y_pred, average='macro'),
                'recall': lambda y_true, y_pred: recall_score(y_true, y_pred, average='macro')
            }
        else:
            # Updated regression scorers
            scorers = {
                'r2': r2_score,
                'neg_mean_squared_error': lambda y_true, y_pred: -mean_squared_error(y_true, y_pred),
                'neg_mean_absolute_error': lambda y_true, y_pred: -mean_absolute_error(y_true, y_pred)
            }
        
        scorer_func = scorers.get(metric_name)
        if scorer_func:
            if metric_name.startswith('neg_') or metric_name == 'r2':
                return make_scorer(scorer_func, greater_is_better=True)
            else:
                return make_scorer(scorer_func)
        return None
    
    def _convert_negative_metrics(self, score, metric):
        """Convert negative metrics to their positive counterparts for display"""
        if metric.startswith('neg_'):
            return -score
        return score

    def _get_metric_display_name(self, metric):
        """Convert metric name to display format"""
        if metric.startswith('neg_'):
            return metric.replace('neg_', '').replace('_', ' ').title()
        return metric.title()

    def _log_detailed_results(self, model_name, random_search):
        """Log detailed results for each fold and iteration"""
        detailed_results = pd.DataFrame(random_search.cv_results_)
        detailed_results['model'] = model_name

        param_cols = [col for col in detailed_results.columns if col.startswith('param_')]
        for col in param_cols:
            detailed_results[col] = detailed_results[col].astype(str)

        # Organize results by iteration
        iterations = []
        for idx in range(len(detailed_results)):
            iteration_data = {
                'iteration': idx + 1,
                'model': model_name,
                'params': dict(zip(
                    [col.replace('param_', '') for col in param_cols],
                    [detailed_results[col][idx] for col in param_cols]
                )),
                'mean_scores': {},
                'std_scores': {},
                'fold_scores': {}
            }

            # Get scores for each metric
            for metric in self.scoring:
                mean_score_key = f'mean_test_{metric}'
                std_score_key = f'std_test_{metric}'
                fold_scores_key = f'split_test_{metric}'

                iteration_data['mean_scores'][metric] = detailed_results[mean_score_key][idx]
                iteration_data['std_scores'][metric] = detailed_results[std_score_key][idx]
                iteration_data['fold_scores'][metric] = [
                    detailed_results[f'split{i}_test_{metric}'][idx]
                    for i in range(self.cv_folds)
                ]

            iterations.append(iteration_data)

        self.detailed_results_[model_name] = iterations

        if self.verbosity >= 2:
            self._print_detailed_iteration_results(model_name)

    def _print_detailed_iteration_results(self, model_name):
        """Print detailed results for each iteration"""
        print(f"\nDetailed Results for {model_name}")
        print("=" * 80)

        for iteration in self .detailed_results_[model_name]:
            print(f"\nIteration {iteration['iteration']}")
            print("-" * 40)
            print("Parameters:")
            for param, value in iteration['params'].items():
                print(f"  {param}: {value}")

            print("\nScores:")
            for metric in iteration['mean_scores'].keys():
                mean_score = iteration['mean_scores'][metric]
                std_score = iteration['std_scores'][metric]
                print(f"  {metric}:")
                print(f"    Mean: {mean_score:.4f} (±{std_score:.4f})")
                print("    Fold scores:", end=" ")
                print([f"{score:.4f}" for score in iteration['fold_scores'][metric]])

    def optimize_single_model(self, model_name, X, y):
        """Optimize a single model using RandomizedSearchCV with detailed output"""

        if not sys.warnoptions:
            warnings.simplefilter("ignore")
            os.environ["PYTHONWARNINGS"] = "ignore"

        if self.verbosity >= 1:
            print(f"\nOptimizing {model_name}...")

        model_config = self.model_configs[model_name]
        model_class = model_config['model_class']
        param_grid = model_config['params']

        best_params = {metric: {} for metric in self.scoring}
        best_scores = {metric: float('-inf') for metric in self.scoring}

        try:
            # Create scoring dictionary for all metrics
            scoring_dict = {}
            for metric in self.scoring:
                scorer = self._get_scorer(metric)
                if scorer is not None:
                    scoring_dict[metric] = scorer

            # If there is no parameter grid, perform simple cross-validation
            if not param_grid:
                model = model_class()
                cv_scores = cross_val_score(
                    model, X, y,
                    cv=self.cv_folds,
                    scoring=scoring_dict,
                    n_jobs=self.n_jobs
                )
                for metric in self.scoring:
                    best_scores[metric] = np.nanmean(cv_scores)  # Use nanmean to ignore NaNs
                return best_params, best_scores

            # Perform RandomizedSearchCV
            random_search = RandomizedSearchCV(
                estimator=model_class(),
                param_distributions=param_grid,
                n_iter=self.generations,
                cv=self.cv_folds,
                scoring=scoring_dict,
                refit=self.refit,
                random_state=self.random_state,
                n_jobs=self.n_jobs,
                verbose=max(0, self.verbosity - 1),
                return_train_score=True
            )

            random_search.fit(X, y)
            self._log_detailed_results(model_name, random_search)

            # Get best scores and parameters for each metric, ignoring NaN scores
            for metric in self.scoring:
                metric_scores = random_search.cv_results_[f'mean_test_{metric}']
                valid_scores = ~np.isnan(metric_scores)  # Filter out NaNs
                if valid_scores.any():
                    best_idx = np.argmax(metric_scores[valid_scores])
                    best_scores[metric] = metric_scores[valid_scores][best_idx]
                    best_params[metric] = {
                        param.replace('param_', ''): random_search.cv_results_[param][valid_scores][best_idx]
                        for param in random_search.cv_results_.keys()
                        if param.startswith('param_')
                    }

        except Exception as e:
            print(f"Error optimizing {model_name}: {str(e)}")
            # Return default values in case of error
            return best_params, best_scores

        return best_params, best_scores

    def fit(self, data):
        """Fit the optimizer to the data"""

        cleaner = DataCleaner()
        data = cleaner.clean(data)

        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame")

        # Extract features and target
        y = data[self.target_column]
        X = data.drop(columns=[self.target_column])

        # Preprocess features
        if self.verbosity >= 1:
            print("\nPreprocessing data...")
            print(f"Original features: {X.columns.tolist()}")

        # Determine number of classes for classification tasks
        if self.task_type == 'classification':
            self.n_classes = len(np.unique(y))
            if self.verbosity >= 1:
                print(f"\nDetected {self.n_classes} classes in target variable")

        X_processed = self.preprocessor.fit_transform(X)
        y_processed = self.preprocessor.fit_transform_target(y)

        if self.verbosity >= 1:
            print(f"Processed features: {X_processed.columns.tolist()}")
            print(f"Number of features after preprocessing: {X_processed.shape[1]}")
            if not pd.api.types.is_numeric_dtype(y):
                print(f"Target classes: {self.preprocessor.target_encoder.classes_}")

        for model_name in self.model_configs.keys():
            best_params, best_scores = self.optimize_single_model(model_name, X_processed, y_processed)

            # Store results for each metric
            self.results_[model_name] = {
                'params': best_params,
                'scores': best_scores
            }

            # Update best models for each metric
            for metric in self.scoring:
                if best_scores[metric] > self.best_scores[metric]:
                    self.best_scores[metric] = best_scores[metric]
                    self.best_params[metric] = best_params[metric]
                    self.best_models[metric] = model_name

        if self.verbosity >= 1:
            self._print_results()
        
        return self
    
    def best_model_params(self, test_df):
        """
        Select and evaluate the best model based on the optimizer's configuration.
        
        Parameters:
        -----------
        test_df : pandas.DataFrame
            Test dataset for final model evaluation
        
        Returns:
        --------
        dict
            A dictionary containing model evaluation metrics and details
        """
        
        best_model_name = self.best_models[self.refit]
        model_class = self.model_configs[best_model_name]['model_class']
        best_params = self.best_params[self.refit]
        
        target_column = self.target_column
        X_test = test_df.drop(columns=[target_column])
        y_test = test_df[target_column]
        
        X_test_processed = self.preprocessor.transform(X_test)
        y_test_processed = self.preprocessor.transform_target(y_test)
        
        best_model_instance = model_class(**best_params)
        best_model_instance.fit(
            self.preprocessor.transform(test_df.drop(columns=[target_column])), 
            self.preprocessor.transform_target(test_df[target_column])
        )
        
        predictions = best_model_instance.predict(X_test_processed)
        
        results = {}
        if self.task_type == 'classification':
            results = {
                'model_name': best_model_name,
                'accuracy': accuracy_score(y_test_processed, predictions),
                'precision': precision_score(y_test_processed, predictions, zero_division=1, average='macro'),
                'recall': recall_score(y_test_processed, predictions, average='macro'),
                'f1_score': f1_score(y_test_processed, predictions, average='macro'),
                'best_params': best_params
            }
            print("\nClassification Metrics Test Results:")
        else:
            mse = mean_squared_error(y_test_processed, predictions)
            mae = mean_absolute_error(y_test_processed, predictions)
            r2 = r2_score(y_test_processed, predictions)
            
            results = {
                'model_name': best_model_name,
                'r2_score': r2,
                'mean_squared_error': mse,
                'mean_absolute_error': mae,
                'best_params': best_params
            }
            print("\nRegression Metrics Test Results:")
            
        # Print results with consistent formatting
        for metric, value in results.items():
            if metric not in ['best_params', 'model_name']:
                if isinstance(value, (float, int)):
                    metric_display = self._get_metric_display_name(metric)
                    print(f"{metric_display}: {value:.4f}")
                else:
                    print(f"{metric.capitalize()}: {value}")
                    
        return results

    def predict(self, X):
        """Make predictions using the best model"""
        if self.best_models[self.refit] is None:
            raise ValueError("Optimizer hasn't been fitted yet.")

        # Preprocess features
        X_processed = self.preprocessor.transform(X)

        # Get predictions
        model = self.get_best_model()
        return model.predict(X_processed)

    def _print_results(self):
        """Print optimization results"""
        print("\nFinal Results Summary:")
        print("=" * 120)
        print(f"{'Model':<20} {'Metric':<10} {'Best Score':<12} {'Parameters'}")
        print("-" * 120)
        
        for model_name, results in self.results_.items():
            for metric in self.scoring:
                score = results['scores'][metric]
                display_score = self._convert_negative_metrics(score, metric)
                params = results['params'][metric]
                params_str = str(params)
                metric_display = self._get_metric_display_name(metric)
                print(f"{model_name:<20} {metric_display:<25} {display_score:<12.4f} {params_str}")

        print("\nBest Model for Each Metric:")
        print("=" * 80)

        for metric in self.scoring:
            print(f"\nMetric: {self._get_metric_display_name(metric)}")
            print(f"Best Model: {self.best_models[metric]}")
            score = self.best_scores[metric]
            display_score = self._convert_negative_metrics(score, metric)
            print(f"Best Score: {display_score:.4f}")
            print(f"Best Parameters: {self.best_params[metric]}")

    def get_best_model(self, metric=None):
        """Return the best model instance with optimal parameters for a specific metric"""
        if metric is None:
            metric = self.refit

        if self.best_models[metric] is None:
            raise ValueError("Optimizer hasn't been fitted yet.")

        model_class = self.model_configs[self.best_models[metric]]['model_class']
        return model_class(**self.best_params[metric])

    def get_detailed_results(self, as_dataframe=False):
        """Get detailed results for all models"""
        if not as_dataframe:
            return self.detailed_results_

        # Convert to DataFrame
        rows = []
        for model_name, iterations in self.detailed_results_.items():
            for iteration in iterations:
                row = {
                    'model': model_name,
                    'iteration': iteration['iteration'],
                    **iteration['params']
                }
                for metric, score in iteration['mean_scores'].items():
                    row[f'mean_{metric}'] = score
                    row[f'std_{metric}'] = iteration['std_scores'][metric]
                    for fold_idx, fold_score in enumerate(iteration['fold_scores'][metric]):
                        row[f'{metric}_fold_{fold_idx+1}'] = fold_score
                rows.append(row)

        return pd.DataFrame(rows)