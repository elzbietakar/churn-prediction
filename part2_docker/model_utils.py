import os
import pickle
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "models", "model.pkl")

ml_model = pickle.load(open(model_path, "rb"))

def predict(features):
    # Accept a dict (single sample), a list-of-dicts (multiple samples),
    # a pandas DataFrame, or other array-like that pandas can consume.
    if isinstance(features, pd.DataFrame):
        df = features
    elif isinstance(features, dict):
        df = pd.DataFrame([features])
    else:
        df = pd.DataFrame(features)

    predictions = ml_model.predict(df)
    probabilities = ml_model.predict_proba(df)[:, 1]
    
    return predictions.tolist(), probabilities.tolist()