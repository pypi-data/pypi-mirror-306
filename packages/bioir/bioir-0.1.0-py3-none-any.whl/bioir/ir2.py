print("""import pandas as pd
import numpy as np
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination

# Load data
columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach',
           'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']
data = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data", 
                   names=columns)

# Basic preprocessing
data = data.replace('?', np.nan).dropna()
numeric_cols = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
for col in numeric_cols:
    data[col] = pd.to_numeric(data[col])

# Simple binary features
data['age_high'] = (data['age'] > 60).astype(int)
data['bp_high'] = (data['trestbps'] > 140).astype(int)
data['chol_high'] = (data['chol'] > 240).astype(int)
data['target'] = (data['target'] > 0).astype(int)

# Select final features
features = ['age_high', 'bp_high', 'chol_high', 'cp', 'exang', 'target']
data = data[features].astype(int)

# Create and train model
model = BayesianNetwork([
    ('age_high', 'target'),
    ('bp_high', 'target'),
    ('chol_high', 'target'),
    ('cp', 'target'),
    ('exang', 'target')
])

model.fit(data, estimator=MaximumLikelihoodEstimator)
inference = VariableElimination(model)

# Make prediction
evidence = {
    'age_high': 0,    # age > 60
    'bp_high': 1,     # blood pressure > 140
    'chol_high': 1,   # cholesterol > 240
    'cp': 1 ,          # chest pain type
    'exang': 0       # exercise induced angina
}

result = inference.query(variables=['target'], evidence=evidence)
print(f"Probability of Heart Disease: {result.values[1]:.2%}")

# Print data distribution
print("\nData Distribution:")
for col in features:
    print(f"\n{col}:")
    print(data[col].value_counts().sort_index())""")