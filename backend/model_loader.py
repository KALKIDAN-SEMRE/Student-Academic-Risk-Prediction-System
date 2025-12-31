"""
Model Loader Module

This module handles loading the pre-trained machine learning models and scaler.
The models are loaded once when the application starts to avoid reloading them
for every prediction request.
"""

import joblib
import os

# Define the path to the models directory
# Since this file is in the backend folder, models are in the models subdirectory
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")

# Global variables to store loaded models
logistic_model = None
decision_tree_model = None
scaler = None


def load_models():
    """
    Load all pre-trained models and the scaler from joblib files.
    
    This function should be called once when the application starts.
    It loads:
    - Logistic Regression model
    - Decision Tree model
    - Scaler (for feature normalization)
    """
    global logistic_model, decision_tree_model, scaler
    
    # Load Logistic Regression model
    logistic_model_path = os.path.join(MODELS_DIR, "logistic_model.joblib")
    logistic_model = joblib.load(logistic_model_path)
    
    # Load Decision Tree model
    decision_tree_model_path = os.path.join(MODELS_DIR, "decision_tree_model.joblib")
    decision_tree_model = joblib.load(decision_tree_model_path)
    
    # Load Scaler
    scaler_path = os.path.join(MODELS_DIR, "scaler.joblib")
    scaler = joblib.load(scaler_path)
    
    print("All models loaded successfully!")


def get_logistic_model():
    """Return the loaded Logistic Regression model."""
    return logistic_model


def get_decision_tree_model():
    """Return the loaded Decision Tree model."""
    return decision_tree_model


def get_scaler():
    """Return the loaded scaler."""
    return scaler

