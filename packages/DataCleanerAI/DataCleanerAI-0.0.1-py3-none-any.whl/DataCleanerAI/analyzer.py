
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def analyze_data(df):
    issues = {
        'missing_values': df.isnull().sum().to_dict(),
        'duplicates': df.duplicated().sum(),
        'type_inconsistencies': {},
        'outliers': detect_outliers(df)
    }
    return issues

def detect_outliers(df):
    outliers = {}
    for col in df.select_dtypes(include=[np.number]):
        model = IsolationForest(contamination=0.05)
        df['outliers'] = model.fit_predict(df[[col]])
        outliers[col] = df[df['outliers'] == -1][col].values.tolist()
    return outliers
    