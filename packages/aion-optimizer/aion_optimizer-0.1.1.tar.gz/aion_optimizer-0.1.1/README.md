# Aion Optimizer

A Python package for automated machine learning optimization.

## Installation

```bash
pip install aion_optimizer
```

## Usage

```python
from aion_optimizer import EnhancedSequentialOptimizer
import pandas as pd
from sklearn.model_selection import train_test_split

dataset_path = "..."

df = pd.read_csv(dataset_path)

optimizer = EnhancedSequentialOptimizer(
        task_type='classification',
        target_column='class', 
        generations=5,
        cv_folds=5,
        random_state=42,
        n_jobs=-1,
        verbosity=0,
        categorical_threshold=10
    )

train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Fit the optimizer
optimizer.fit(train_df)

# Get the best model parameters and print them
results = optimizer.best_model_params(test_df)
print(results)

## Features
- Automatic model selection
- Hyperparameter optimization
- Support for:
  - Binary classification
  - Multiclass classification
  - Regression
- Simplified metrics reporting
- Cross-validation support
- Detailed results logging

## Requirements
- Python >=3.7
- NumPy >=1.19.0
- Pandas >=1.2.0
- Scikit-learn >=0.24.0
- SciPy >=1.6.0