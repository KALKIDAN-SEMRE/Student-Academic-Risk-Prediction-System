"""
FastAPI Main Application

This is the main FastAPI application that serves machine learning predictions.
It provides a REST API endpoint for predicting student academic risk using
pre-trained Logistic Regression and Decision Tree models.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from model_loader import load_models, get_logistic_model, get_decision_tree_model, get_scaler
from schemas import StudentData

# Create FastAPI application instance
app = FastAPI(
    title="Student Academic Risk Prediction API",
    description="API for predicting student academic risk using ML models",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests
# This is useful if you want to call the API from a frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Startup event handler.
    
    This function runs once when the application starts.
    It loads all the pre-trained models into memory.
    """
    load_models()


@app.get("/")
async def root():
    """
    Root endpoint - provides basic API information.
    
    Returns:
        dict: Welcome message and API information
    """
    return {
        "message": "Student Academic Risk Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict (POST)",
            "docs": "/docs",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status of the API
    """
    return {"status": "healthy", "message": "API is running"}


@app.post("/predict")
async def predict(student_data: StudentData):
    """
    Prediction endpoint.
    
    This endpoint accepts student data and returns predictions from both
    Logistic Regression and Decision Tree models.
    
    Args:
        student_data: StudentData object containing student information
        
    Returns:
        dict: Predictions from both models (0 = Low Risk, 1 = High Risk)
        
    Raises:
        HTTPException: If models are not loaded or prediction fails
    """
    try:
        # Get the loaded models and scaler
        logistic_model = get_logistic_model()
        decision_tree_model = get_decision_tree_model()
        scaler = get_scaler()
        
        # Check if models are loaded
        if logistic_model is None or decision_tree_model is None or scaler is None:
            raise HTTPException(
                status_code=500,
                detail="Models not loaded. Please restart the application."
            )
        
        # Convert input data to a list in the correct order
        # Order: attendance, study_hours, assignments_completed, quiz_score, 
        #        midterm_score, internet_access, past_failures
        input_data = [
            student_data.attendance,
            student_data.study_hours,
            student_data.assignments_completed,
            student_data.quiz_score,
            student_data.midterm_score,
            student_data.internet_access,
            student_data.past_failures
        ]
        
        # Convert to NumPy array and reshape for model input
        # Reshape to (1, 7) because models expect 2D array with one sample
        input_array = np.array(input_data).reshape(1, -1)
        
        # Logistic Regression prediction (requires scaling)
        # Scale the input data using the pre-fitted scaler
        scaled_input = scaler.transform(input_array)
        logistic_prediction = logistic_model.predict(scaled_input)[0]
        
        # Get probability of being "At Risk" (class 1) using predict_proba
        # predict_proba returns probabilities for [class 0, class 1]
        logistic_proba = logistic_model.predict_proba(scaled_input)[0]
        # Get probability of class 1 (At Risk) and round to 2 decimal places
        risk_probability = round(float(logistic_proba[1]), 2)
        
        # Generate human-readable explanation for Logistic Regression
        # Based on input values: exam scores, study hours, attendance
        explanation_parts = []
        if student_data.midterm_score < 70:
            explanation_parts.append("low midterm score")
        if student_data.quiz_score < 70:
            explanation_parts.append("low quiz score")
        if student_data.study_hours < 10:
            explanation_parts.append("low study hours")
        if student_data.attendance < 75:
            explanation_parts.append("low attendance")
        
        # Build the explanation sentence
        if explanation_parts:
            if len(explanation_parts) == 1:
                explanation_text = f"The model predicted the student is {'at risk' if logistic_prediction == 1 else 'not at risk'} because of {explanation_parts[0]}."
            else:
                explanation_text = f"The model predicted the student is {'at risk' if logistic_prediction == 1 else 'not at risk'} because of {', '.join(explanation_parts[:-1])}, and {explanation_parts[-1]}."
        else:
            # If no risk factors, provide a positive explanation
            explanation_text = f"The model predicted the student is {'at risk' if logistic_prediction == 1 else 'not at risk'} based on overall academic performance indicators."
        
        # Decision Tree prediction (uses raw input, no scaling needed)
        decision_tree_prediction = decision_tree_model.predict(input_array)[0]
        
        # Generate human-readable explanation for Decision Tree
        # Based on: past failures and internet access
        dt_explanation_parts = []
        if student_data.past_failures > 0:
            dt_explanation_parts.append(f"{student_data.past_failures} past failure(s)")
        else:
            dt_explanation_parts.append("no past failures")
        
        if student_data.internet_access == 1:
            dt_explanation_parts.append("internet access available")
        else:
            dt_explanation_parts.append("no internet access")
        
        # Build Decision Tree explanation
        dt_explanation_text = f"The model predicted the student is {'at risk' if decision_tree_prediction == 1 else 'not at risk'} because of {', '.join(dt_explanation_parts)}."
        
        # Return the response in the new format with explanations
        return {
            "logistic_regression": {
                "prediction": int(logistic_prediction),
                "risk_probability": risk_probability,
                "explanation": explanation_text
            },
            "decision_tree": {
                "prediction": int(decision_tree_prediction),
                "explanation": dt_explanation_text
            }
        }
        
    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

