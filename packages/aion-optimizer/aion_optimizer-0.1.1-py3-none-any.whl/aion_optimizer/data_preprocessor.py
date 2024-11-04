import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer

class DataPreprocessor:
    """Handle data preprocessing for both numerical and categorical features"""

    def __init__(self, categorical_threshold=10):
        self.categorical_threshold = categorical_threshold
        self.num_features = None
        self.cat_features = None
        self.preprocessor = None
        self.target_encoder = LabelEncoder()

    def _identify_features(self, X):
        """Identify numerical and categorical features"""
        numeric_features = []
        categorical_features = []

        for column in X.columns:
            if pd.api.types.is_numeric_dtype(X[column]):
                if X[column].nunique() > self.categorical_threshold:
                    numeric_features.append(column)
                else:
                    categorical_features.append(column)
            else:
                categorical_features.append(column)

        return numeric_features, categorical_features

    def fit(self, X, y=None):
        """Fit the preprocessor to the data"""
        self.num_features, self.cat_features = self._identify_features(X)

        numeric_transformer = StandardScaler()
        categorical_transformer = OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore')

        transformers = []
        if self.num_features:
            transformers.append(('num', numeric_transformer, self.num_features))
        if self.cat_features:
            transformers.append(('cat', categorical_transformer, self.cat_features))

        self.preprocessor = ColumnTransformer(
            transformers=transformers,
            remainder='passthrough'
        )

        self.preprocessor.fit(X)

        return self

    def transform(self, X):
        """Transform the data"""
        if self.preprocessor is None:
            raise ValueError("Preprocessor not fitted yet!")

        X_transformed = self.preprocessor.transform(X)
        feature_names = self._get_feature_names()
        return pd.DataFrame(X_transformed, columns=feature_names, index=X.index)

    def fit_transform(self, X, y=None):
        """Fit and transform the data"""
        return self.fit(X, y).transform(X)

    def _get_feature_names(self):
        """Get feature names after transformation"""
        feature_names = []

        for name, transformer, features in self.preprocessor.transformers_:
            if name == 'num':
                feature_names.extend(features)
            elif name == 'cat':
                for feature in features:
                    categories = transformer.categories_[features.index(feature)][1:]
                    feature_names.extend([f"{feature}_{cat}" for cat in categories])

        return feature_names

    def fit_transform_target(self, y):
        """Fit and transform the target variable if it's categorical"""
        if not pd.api.types.is_numeric_dtype(y):
            return self.target_encoder.fit_transform(y)
        return y

    def transform_target(self, y):
        """Transform the target variable if it's categorical"""
        if not pd.api.types.is_numeric_dtype(y):
            return self.target_encoder.transform(y)
        return y