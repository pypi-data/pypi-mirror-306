import json
import pkg_resources
from scipy.stats import randint, uniform
from sklearn.linear_model import LogisticRegression, LinearRegression, Lasso, Ridge
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier
from xgboost import XGBClassifier as ExtremeGradientBoosting
from xgboost import XGBRegressor as ExtremeGradientBoostingRegressor
from lightgbm import LGBMClassifier as LightGradientBoosting
from lightgbm import LGBMRegressor as LightGradientBoostingRegressor
from catboost import CatBoostClassifier as CategoricalBoosting
from catboost import CatBoostRegressor as CategoricalBoostingRegressor
import warnings
warnings.filterwarnings('ignore')

class HyperparameterConfigParser:
    def __init__(self, file_name):
        self.file_path = pkg_resources.resource_filename(__name__, file_name)
        self.classification_mapping = {
            'LogisticRegression': LogisticRegression,
            'GaussianNB': GaussianNB,
            'SVC': SVC,
            'KNeighborsClassifier': KNeighborsClassifier,
            'DecisionTreeClassifier': DecisionTreeClassifier,
            'RandomForestClassifier': RandomForestClassifier,
            'GradientBoostingClassifier': GradientBoostingClassifier,
            'ExtremeGradientBoosting': ExtremeGradientBoosting,
            'LightGradientBoosting': LightGradientBoosting,
            'CategoricalBoosting': CategoricalBoosting
        }
        self.regression_mapping = {
            'LinearRegression': LinearRegression,
            'Lasso': Lasso,
            'Ridge': Ridge,
            'DecisionTree': DecisionTreeRegressor,
            'RandomForest': RandomForestRegressor,
            'ExtremeGradientBoosting': ExtremeGradientBoostingRegressor,
            'LightGradientBoosting': LightGradientBoostingRegressor,
            'CategoricalBoosting': CategoricalBoostingRegressor
        }
        self.classification_config = {}
        self.regression_config = {}

    @staticmethod
    def is_numeric_string(s):
        try:
            float(s.strip())
            return True
        except ValueError:
            return False

    @staticmethod
    def convert_number_type(value):
        if isinstance(value, (int, float)):
            return int(value) if value.is_integer() else value
        return value

    def create_distribution(self, param_value):
        if isinstance(param_value, str) and param_value.startswith('[') and param_value.endswith(']'):
            param_value = param_value[1:-1].strip()

        if isinstance(param_value, str):
            if ',' in param_value:
                values = [
                    float(x.strip()) if self.is_numeric_string(x) else x.strip()
                    for x in param_value.split(',')
                ]
                return [int(val) if isinstance(val, float) and val.is_integer() else val for val in values]

            if param_value.lower() == 'true': return [True]
            if param_value.lower() == 'false': return [False]
            try:
                num = float(param_value)
                return [int(num) if num.is_integer() else num]
            except ValueError:
                return [param_value]

        elif isinstance(param_value, (int, float)):
            return [self.convert_number_type(param_value)]
        
        elif isinstance(param_value, list):
            return [self.convert_number_type(x) if isinstance(x, (int, float)) else x for x in param_value]

        return [param_value]

    def parse_config_file(self):
        try:
            with open(self.file_path, 'r') as file:
                config_data = json.load(file)

            if 'classification' in config_data:
                for model_name, options in config_data['classification'].items():
                    # Skip LightGradientBoosting for classification
                    if model_name == 'LightGradientBoosting':
                        continue
                    if model_name in self.classification_mapping and 'option 1' in options:
                        params = {k: self.create_distribution(v)
                                for k, v in options['option 1'].items()}
                        self.classification_config[model_name] = {
                            'model_class': self.classification_mapping[model_name],
                            'params': params
                        }

            if 'regression' in config_data:
                for model_name, options in config_data['regression'].items():
                    # Skip LightGradientBoosting for regression
                    if model_name == 'LightGradientBoosting':
                        continue
                    if model_name in self.regression_mapping and 'option 1' in options:
                        params = {k: self.create_distribution(v)
                                for k, v in options['option 1'].items()}
                        self.regression_config[model_name] = {
                            'model_class': self.regression_mapping[model_name],
                            'params': params
                        }

        except FileNotFoundError:
            print(f"Error: Configuration file not found at {self.file_path}")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in configuration file")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def print_configurations(self):
        print("\n" + "="*50)
        print("CLASSIFICATION MODELS CONFIGURATION")
        print("="*50)
        
        for model_name, config in self.classification_config.items():
            print(f"\n{model_name}:")
            print("-" * (len(model_name) + 1))
            for param_name, param_values in config['params'].items():
                print(f"{param_name}:")
                for value in param_values:
                    print(f"  - {value} (Type: {type(value).__name__})")

        print("\n" + "="*50)
        print("REGRESSION MODELS CONFIGURATION")
        print("="*50)
        
        for model_name, config in self.regression_config.items():
            print(f"\n{model_name}:")
            print("-" * (len(model_name) + 1))
            for param_name, param_values in config['params'].items():
                print(f"{param_name}:")
                for value in param_values:
                    print(f"  - {value} (Type: {type(value).__name__})")
