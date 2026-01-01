/**
 * Main App Component
 *
 * This is the root component of our application.
 * It manages the overall state and renders the prediction form.
 */

import { useState } from "react";
import "./App.css";

function App() {
  // State to store form input values
  const [formData, setFormData] = useState({
    attendance: "",
    study_hours: "",
    assignments_completed: "",
    quiz_score: "",
    midterm_score: "",
    internet_access: "1", // Default to "Yes"
    past_failures: "",
  });

  // State to store prediction results
  const [results, setResults] = useState(null);

  // State to track if we're currently loading (waiting for API response)
  const [loading, setLoading] = useState(false);

  // State to store any error messages
  const [error, setError] = useState(null);

  /**
   * Handle input field changes
   * Updates the formData state when user types in any field
   */
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Clear error when user starts typing again
    setError(null);
  };

  /**
   * Handle form submission
   * Sends the student data to the backend API and displays results
   */
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent page refresh

    // Reset previous results and errors
    setResults(null);
    setError(null);
    setLoading(true);

    try {
      // Convert form data to the format expected by the backend
      const requestData = {
        attendance: parseFloat(formData.attendance),
        study_hours: parseFloat(formData.study_hours),
        assignments_completed: parseInt(formData.assignments_completed),
        quiz_score: parseFloat(formData.quiz_score),
        midterm_score: parseFloat(formData.midterm_score),
        internet_access: parseInt(formData.internet_access), // Convert to 0 or 1
        past_failures: parseInt(formData.past_failures),
      };

      // Validate that all fields are filled
      if (Object.values(requestData).some((val) => isNaN(val) || val === "")) {
        throw new Error("Please fill in all fields with valid numbers");
      }

      // Send POST request to the backend API
      const response = await fetch(
        "https://student-risk-api-mgui.onrender.com/predict",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestData),
        }
      );

      // Check if the request was successful
      if (!response.ok) {
        const errorData = await response
          .json()
          .catch(() => ({ detail: "Unknown error" }));
        throw new Error(errorData.detail || `Server error: ${response.status}`);
      }

      // Get the prediction results from the response
      const data = await response.json();
      setResults(data);
    } catch (err) {
      // Handle any errors (network errors, validation errors, etc.)
      setError(err.message || "Failed to get prediction. Please try again.");
      console.error("Prediction error:", err);
    } finally {
      // Always stop loading, whether success or error
      setLoading(false);
    }
  };

  /**
   * Helper function to get risk status label
   * Returns "At Risk" if prediction is 1, "Not At Risk" if 0
   */
  const getRiskLabel = (prediction) => {
    return prediction === 1 ? "At Risk" : "Not At Risk";
  };

  /**
   * Helper function to get risk status class for styling
   * Returns appropriate class based on prediction and probability
   */
  const getRiskClass = (prediction, probability = null) => {
    if (prediction === 1) {
      return "risk-at-risk";
    } else if (
      probability !== null &&
      probability >= 0.45 &&
      probability <= 0.55
    ) {
      // Yellow/orange for uncertain predictions (close to 50%)
      return "risk-uncertain";
    } else {
      return "risk-not-at-risk";
    }
  };

  /**
   * Helper function to format probability as percentage
   */
  const formatProbability = (probability) => {
    if (probability === null || probability === undefined) return "N/A";
    return `${Math.round(probability * 100)}%`;
  };

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>Student Academic Risk Prediction</h1>
          <p>
            Enter student data below to predict academic risk using ML models
          </p>
        </header>

        {/* Prediction Form */}
        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <label htmlFor="attendance">
              Attendance (%) <span className="required">*</span>
            </label>
            <input
              type="number"
              id="attendance"
              name="attendance"
              value={formData.attendance}
              onChange={handleChange}
              min="0"
              max="100"
              step="0.1"
              required
              placeholder="e.g., 85.5"
            />
          </div>

          <div className="form-group">
            <label htmlFor="study_hours">
              Study Hours (per week) <span className="required">*</span>
            </label>
            <input
              type="number"
              id="study_hours"
              name="study_hours"
              value={formData.study_hours}
              onChange={handleChange}
              min="0"
              step="0.1"
              required
              placeholder="e.g., 10.0"
            />
          </div>

          <div className="form-group">
            <label htmlFor="assignments_completed">
              Assignments Completed <span className="required">*</span>
            </label>
            <input
              type="number"
              id="assignments_completed"
              name="assignments_completed"
              value={formData.assignments_completed}
              onChange={handleChange}
              min="0"
              required
              placeholder="e.g., 8"
            />
          </div>

          <div className="form-group">
            <label htmlFor="quiz_score">
              Quiz Score (0-100) <span className="required">*</span>
            </label>
            <input
              type="number"
              id="quiz_score"
              name="quiz_score"
              value={formData.quiz_score}
              onChange={handleChange}
              min="0"
              max="100"
              step="0.1"
              required
              placeholder="e.g., 75.0"
            />
          </div>

          <div className="form-group">
            <label htmlFor="midterm_score">
              Midterm Score (0-100) <span className="required">*</span>
            </label>
            <input
              type="number"
              id="midterm_score"
              name="midterm_score"
              value={formData.midterm_score}
              onChange={handleChange}
              min="0"
              max="100"
              step="0.1"
              required
              placeholder="e.g., 80.0"
            />
          </div>

          <div className="form-group">
            <label htmlFor="internet_access">
              Internet Access <span className="required">*</span>
            </label>
            <select
              id="internet_access"
              name="internet_access"
              value={formData.internet_access}
              onChange={handleChange}
              required
            >
              <option value="1">Yes</option>
              <option value="0">No</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="past_failures">
              Past Failures <span className="required">*</span>
            </label>
            <input
              type="number"
              id="past_failures"
              name="past_failures"
              value={formData.past_failures}
              onChange={handleChange}
              min="0"
              required
              placeholder="e.g., 0"
            />
          </div>

          {/* Submit Button */}
          <button type="submit" className="submit-button" disabled={loading}>
            {loading ? "Predicting..." : "Get Prediction"}
          </button>
        </form>

        {/* Error Message Display */}
        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Results Display */}
        {results && (
          <div className="results">
            <h2>Prediction Results</h2>

            {/* Logistic Regression Results */}
            <div className="result-item">
              <h3>Logistic Regression (Trend-based model)</h3>
              <div
                className={`risk-status ${getRiskClass(
                  results.logistic_regression?.prediction ??
                    results.logistic_regression,
                  results.logistic_regression?.risk_probability
                )}`}
              >
                {getRiskLabel(
                  results.logistic_regression?.prediction ??
                    results.logistic_regression
                )}
                {results.logistic_regression?.risk_probability !==
                  undefined && (
                  <span className="probability-badge">
                    {formatProbability(
                      results.logistic_regression.risk_probability
                    )}{" "}
                    risk
                  </span>
                )}
              </div>

              {/* Explanation Section */}
              {results.logistic_regression?.explanation && (
                <div className="explanation-section">
                  <h4>Why this prediction?</h4>
                  <p className="explanation-text">
                    {results.logistic_regression.explanation}
                  </p>
                </div>
              )}
            </div>

            {/* Decision Tree Results */}
            <div className="result-item">
              <h3>Decision Tree (Rule-based model)</h3>
              <div
                className={`risk-status ${getRiskClass(
                  results.decision_tree?.prediction ?? results.decision_tree
                )}`}
              >
                {getRiskLabel(
                  results.decision_tree?.prediction ?? results.decision_tree
                )}
              </div>

              {/* Explanation Section */}
              {results.decision_tree?.explanation && (
                <div className="explanation-section">
                  <h4>Why this prediction?</h4>
                  <p className="explanation-text">
                    {results.decision_tree.explanation}
                  </p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
