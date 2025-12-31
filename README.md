# Student Academic Risk Prediction System

A comprehensive full-stack machine learning application that predicts student academic risk using Logistic Regression and Decision Tree algorithms. The system provides an intuitive web interface for educators and administrators to assess student performance and identify at-risk students early.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Machine Learning Models](#machine-learning-models)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Overview

The Student Academic Risk Prediction System is designed to help educational institutions identify students who may be at risk of academic failure. By analyzing key performance indicators such as attendance, study hours, assignment completion, exam scores, and historical data, the system provides actionable insights through two complementary machine learning models.

### Key Capabilities

- **Dual Model Prediction**: Utilizes both Logistic Regression (trend-based) and Decision Tree (rule-based) models for comprehensive risk assessment
- **Probability Scoring**: Provides risk probability scores for more nuanced predictions
- **Explainable AI**: Generates human-readable explanations for each prediction
- **Real-time Predictions**: Fast API responses for immediate risk assessment
- **User-Friendly Interface**: Clean, intuitive web interface for easy data input and result visualization

## Features

### Machine Learning
- **Logistic Regression Model**: Provides probability-based predictions with trend analysis
- **Decision Tree Model**: Offers rule-based predictions with clear decision paths
- **Feature Scaling**: Automatic normalization for optimal model performance
- **Pre-trained Models**: Ready-to-use models for immediate deployment

### Backend (FastAPI)
- RESTful API with comprehensive endpoint documentation
- Input validation using Pydantic schemas
- CORS support for frontend integration
- Error handling and health check endpoints
- Probability calculation using `predict_proba`
- Human-readable explanation generation

### Frontend (React)
- Responsive, modern UI design
- Real-time form validation
- Loading states and error handling
- Color-coded risk indicators (Red: At Risk, Green: Not At Risk, Yellow: Uncertain)
- Probability display as percentage
- Explanation sections for model transparency
- Model type labels (Trend-based vs Rule-based)

## System Architecture

```
┌─────────────────┐
│   React Frontend │
│   (Port 3000)    │
└────────┬────────┘
         │ HTTP POST
         ▼
┌─────────────────┐
│  FastAPI Backend │
│   (Port 8001)    │
└────────┬────────┘
         │
         ├──► Logistic Regression Model
         │    └──► Probability + Explanation
         │
         └──► Decision Tree Model
              └──► Prediction + Explanation
```

### Data Flow

1. User inputs student data through the React frontend
2. Frontend validates and sends data to FastAPI backend
3. Backend validates input using Pydantic schemas
4. Data is preprocessed (scaled for Logistic Regression)
5. Both models generate predictions
6. Explanations are generated based on input features
7. Results are returned to frontend with probabilities and explanations
8. Frontend displays results with visual indicators

## Technology Stack

### Machine Learning
- **scikit-learn**: Model training and prediction
- **joblib**: Model serialization and loading
- **numpy**: Numerical computations

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **Pydantic**: Data validation using Python type annotations
- **Python 3.8+**: Programming language

### Frontend
- **React 18**: UI library for building user interfaces
- **Vite**: Fast build tool and development server
- **CSS3**: Styling and responsive design

## Installation

### Prerequisites

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Node.js 16+** and npm ([Download](https://nodejs.org/))
- **Git** (optional, for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Student-Academic-Risk-Prediction-ML-Project
```

### Step 2: Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd Student-Academic-Risk-Prediction-System/backend
   ```

2. Install Python dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

   This installs:
   - `fastapi`
   - `uvicorn`
   - `joblib`
   - `scikit-learn`
   - `numpy`

3. Verify models are present:
   Ensure the `models/` directory contains:
   - `logistic_model.joblib`
   - `decision_tree_model.joblib`
   - `scaler.joblib`

### Step 3: Frontend Setup

1. Navigate to the frontend directory (in a new terminal):
   ```bash
   cd Student-Academic-Risk-Prediction-System/frontend
   ```

2. Install Node.js dependencies:
```bash
npm install
```

   This installs:
   - `react`
   - `react-dom`
   - `vite`
   - `@vitejs/plugin-react`

## Usage

### Starting the Application

#### Terminal 1: Start Backend Server

```bash
cd Student-Academic-Risk-Prediction-System/backend
python -m uvicorn main:app --host 127.0.0.1 --port 8001
```

Expected output:
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
All models loaded successfully!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
```

#### Terminal 2: Start Frontend Server

```bash
cd Student-Academic-Risk-Prediction-System/frontend
npm run dev
```

Expected output:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
```

### Using the Web Interface

1. Open your browser and navigate to `http://localhost:3000`
2. Fill in the student data form:
   - **Attendance (%)**: 0-100
   - **Study Hours (per week)**: Number of hours
   - **Assignments Completed**: Count of completed assignments
   - **Quiz Score**: 0-100
   - **Midterm Score**: 0-100
   - **Internet Access**: Yes/No dropdown
   - **Past Failures**: Number of previous course failures
3. Click **"Get Prediction"**
4. View the results:
   - Risk predictions from both models
   - Probability percentage (Logistic Regression)
   - Explanations for each prediction

### API Usage (Direct)

You can also interact with the API directly using curl, Postman, or any HTTP client:

```bash
curl -X POST "http://127.0.0.1:8001/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "attendance": 85.5,
    "study_hours": 10.0,
    "assignments_completed": 8,
    "quiz_score": 75.0,
    "midterm_score": 80.0,
    "internet_access": 1,
    "past_failures": 0
  }'
```

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8001
```

### Interactive API Documentation

FastAPI provides automatic interactive documentation:
- **Swagger UI**: `http://127.0.0.1:8001/docs`
- **ReDoc**: `http://127.0.0.1:8001/redoc`

### Endpoints

#### `GET /`
Returns API information and available endpoints.

**Response:**
```json
{
  "message": "Student Academic Risk Prediction API",
  "version": "1.0.0",
  "endpoints": {
    "predict": "/predict (POST)",
    "docs": "/docs",
    "health": "/health"
  }
}
```

#### `GET /health`
Health check endpoint to verify API status.

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

#### `POST /predict`
Main prediction endpoint. Accepts student data and returns predictions from both models.

**Request Body:**
```json
{
  "attendance": 85.5,
  "study_hours": 10.0,
  "assignments_completed": 8,
  "quiz_score": 75.0,
  "midterm_score": 80.0,
  "internet_access": 1,
  "past_failures": 0
}
```

**Response:**
```json
{
  "logistic_regression": {
    "prediction": 0,
    "risk_probability": 0.23,
    "explanation": "The model predicted the student is not at risk based on overall academic performance indicators."
  },
  "decision_tree": {
    "prediction": 0,
    "explanation": "The model predicted the student is not at risk because of no past failures, and internet access available."
  }
}
```

**Field Descriptions:**

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `attendance` | float | 0-100 | Student's attendance percentage |
| `study_hours` | float | ≥0 | Number of hours studied per week |
| `assignments_completed` | int | ≥0 | Number of assignments completed |
| `quiz_score` | float | 0-100 | Average quiz score |
| `midterm_score` | float | 0-100 | Midterm exam score |
| `internet_access` | int | 0 or 1 | Internet access (0=No, 1=Yes) |
| `past_failures` | int | ≥0 | Number of past course failures |

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `prediction` | int | 0 = Not At Risk, 1 = At Risk |
| `risk_probability` | float | Probability of being at risk (0.0-1.0), only for Logistic Regression |
| `explanation` | string | Human-readable explanation of the prediction |

## Project Structure

```
Student-Academic-Risk-Prediction-ML-Project/
│
├── README.md                          # This file
│
└── Student-Academic-Risk-Prediction-System/
    │
    ├── backend/                       # FastAPI Backend
    │   ├── main.py                    # Main FastAPI application and endpoints
    │   ├── model_loader.py            # Model loading and management
    │   ├── schemas.py                 # Pydantic data validation schemas
    │   ├── test_backend.py            # Backend testing script
    │   ├── requirements.txt           # Python dependencies
    │   │
    │   └── models/                    # Pre-trained ML models
    │       ├── logistic_model.joblib  # Logistic Regression model
    │       ├── decision_tree_model.joblib  # Decision Tree model
    │       └── scaler.joblib          # Feature scaler
    │
    ├── frontend/                      # React Frontend
    │   ├── src/
    │   │   ├── App.jsx                # Main React component
    │   │   ├── App.css                # Component styles
    │   │   ├── main.jsx               # React entry point
    │   │   └── index.css              # Global styles
    │   ├── index.html                 # HTML template
    │   ├── package.json               # Node.js dependencies
    │   └── vite.config.js             # Vite configuration
    │
    ├── student_data.csv               # Training dataset (if available)
    ├── QUICK_START.md                 # Quick setup guide
    └── SETUP_COMMANDS.md              # Detailed setup commands
```

## 🤖 Machine Learning Models

### Model Overview

The system employs two complementary machine learning models to provide comprehensive risk assessment:

#### 1. Logistic Regression (Trend-based Model)

- **Type**: Probabilistic classification model
- **Use Case**: Identifies risk based on continuous trends and patterns
- **Output**: 
  - Binary prediction (0 or 1)
  - Risk probability (0.0 to 1.0)
  - Explanation based on performance metrics

**Key Features:**
- Uses feature scaling for optimal performance
- Provides probability scores for nuanced risk assessment
- Explains predictions based on:
  - Low midterm scores (< 70)
  - Low quiz scores (< 70)
  - Low study hours (< 10 hours/week)
  - Low attendance (< 75%)

#### 2. Decision Tree (Rule-based Model)

- **Type**: Rule-based classification model
- **Use Case**: Makes decisions based on clear, interpretable rules
- **Output**:
  - Binary prediction (0 or 1)
  - Explanation based on decision rules

**Key Features:**
- No feature scaling required
- Provides clear, rule-based explanations
- Explains predictions based on:
  - Past failures (presence or absence)
  - Internet access availability

### Model Training

The models were pre-trained on student academic data and are saved in the `backend/models/` directory. The models are loaded into memory when the backend server starts, ensuring fast prediction times.

**Model Files:**
- `logistic_model.joblib`: Trained Logistic Regression classifier
- `decision_tree_model.joblib`: Trained Decision Tree classifier
- `scaler.joblib`: StandardScaler fitted on training data

### Feature Engineering

The models use the following features:
1. **Attendance** (0-100%): Student attendance percentage
2. **Study Hours**: Weekly study hours
3. **Assignments Completed**: Number of completed assignments
4. **Quiz Score** (0-100): Average quiz performance
5. **Midterm Score** (0-100): Midterm exam performance
6. **Internet Access** (0/1): Binary indicator
7. **Past Failures**: Historical failure count

## 🔧 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError` when starting the server
- **Solution**: Ensure all dependencies are installed: `python -m pip install -r requirements.txt`

**Problem**: Models not loading
- **Solution**: Verify all three `.joblib` files exist in `backend/models/` directory

**Problem**: Port 8001 already in use
- **Solution**: Change the port: `python -m uvicorn main:app --host 127.0.0.1 --port 8002`
  - Update frontend API URL in `src/App.jsx` accordingly

**Problem**: CORS errors
- **Solution**: Backend has CORS enabled by default. Verify backend is running and accessible

### Frontend Issues

**Problem**: `npm` command not found
- **Solution**: Install Node.js from [nodejs.org](https://nodejs.org/)

**Problem**: Connection refused errors
- **Solution**: 
  1. Verify backend is running on port 8001
  2. Check the API URL in `src/App.jsx` matches your backend URL
  3. Ensure both servers are running simultaneously

**Problem**: Port 3000 already in use
- **Solution**: Vite will automatically use the next available port (3001, 3002, etc.)

### Testing the Connection

Test backend health:
```bash
curl http://127.0.0.1:8001/health
```

Expected response:
```json
{"status":"healthy","message":"API is running"}
```

## Contributing

This project is designed for educational and practical use. When contributing:

1. Maintain code quality and documentation
2. Follow existing code style and patterns
3. Test changes thoroughly
4. Update documentation as needed

### Code Style

- **Python**: Follow PEP 8 guidelines
- **JavaScript/React**: Use modern ES6+ syntax
- **Comments**: Include clear, descriptive comments

## License

This project is provided for educational and research purposes.

## Acknowledgments

- Built with FastAPI, React, and scikit-learn
- Designed for educational institutions and student support systems

---

**Version**: 1.0.0  
**Last Updated**: 2024

For detailed setup instructions, see `QUICK_START.md` or `SETUP_COMMANDS.md` in the project directory.
