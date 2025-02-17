from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import json
import os
import numpy as np
import joblib
import tempfile
import datetime

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "mydatabase"),
    "user": os.getenv("DB_USER", "myuser"),
    "password": os.getenv("DB_PASSWORD", "mypassword"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", 5432)
}

# Ensure predictions directory exists
PREDICTIONS_DIR = "output_predictions"
os.makedirs(PREDICTIONS_DIR, exist_ok=True)

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/api/data', methods=['GET'])
def get_data():
    """Fetches stored training data results from the database."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM "trainning_data_results";')
        rows = cur.fetchall()
        
        data = [{
            "model": row[0],
            "calculations": json.loads(row[1]) if isinstance(row[1], str) else row[1],
            "predictions": json.loads(row[2]) if isinstance(row[2], str) else row[2]
        } for row in rows]
        
        cur.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": "Failed to fetch data", "details": str(e)}), 500

@app.route('/api/rul', methods=['POST'])
def predict_rul():
    """Handles file uploads and makes predictions using a selected ML model."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    model_name = request.form.get('model_name')
    
    if not model_name:
        return jsonify({"error": "Model name is required"}), 400
    
    model_paths = {
        "XGBoost (RUL)": "./notebooks/models/xgboost_rul.pkl",
        "Random Forest (RUL)": "./notebooks/models/random_forest_rul.pkl",
        "SVR (RUL)": "./notebooks/models/svr_rul.pkl",
        "LightGBM (RUL)": "./notebooks/models/lightgbm_rul.pkl"
    }
    
    model_path = model_paths.get(model_name)
    if not model_path:
        return jsonify({"error": "Invalid model name"}), 400
    
    try:
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name
        
        # Read data from file
        try:
            input_data = np.loadtxt(temp_file_path)
        except Exception:
            return jsonify({"error": "Invalid file format: must contain only numeric values"}), 400

        # Ensure input is a NumPy array
        if not isinstance(input_data, np.ndarray):
            return jsonify({"error": "Error processing file: Data is not in the correct format"}), 400
        
        # Load model
        if not os.path.exists(model_path):
            return jsonify({"error": "Model not found"}), 500
        
        model = joblib.load(model_path)
        
        # Check expected feature size
        expected_features = model.n_features_in_
        if input_data.ndim == 1:
            input_data = input_data.reshape(1, -1)  # Convert 1D array to 2D
        
        if input_data.shape[1] != expected_features:
            return jsonify({
                "error": "Feature count mismatch",
                "details": f"Input has {input_data.shape[1]} features, but model expects {expected_features}."
            }), 400
        
        # Make prediction
        predictions = model.predict(input_data).tolist()
        
        # Generate a unique timestamped output filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{PREDICTIONS_DIR}/{model_name.replace(' ', '_').lower()}_prediction_{timestamp}.json"
        
        # Save predictions to the file
        with open(output_filename, "w") as f:
            json.dump({"predictions": predictions}, f)
        
        # Cleanup temp file
        os.remove(temp_file_path)
        
        return jsonify({"prediction": predictions, "output_file_path": output_filename})
    
    except Exception as e:
        return jsonify({"error": "Error processing the file", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
