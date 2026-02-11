
import pickle
import os
import numpy as np
from sklearn.ensemble import IsolationForest

MODEL_PATH = "backend/ai_engine/model.pkl"

class AnomalyDetector:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                with open(MODEL_PATH, "rb") as f:
                    self.model = pickle.load(f)
                print("ML Model loaded successfully.")
            except Exception as e:
                print(f"Error loading ML model: {e}")
                self.model = None
        else:
            print("ML Model not found. Please train the model first.")
            self.model = None

    def predict(self, features):
        """
        Returns:
            1 if normal
            -1 if anomaly
        """
        if not self.model:
            return 1 # Default to normal if no model

        # Features expected: [attempts_last_1min, attempts_last_10min, total_attempts]
        feature_vector = np.array([[
            features.get("attempts_last_1min", 0),
            features.get("attempts_last_10min", 0),
            features.get("total_attempts", 0)
        ]])
        
        try:
            prediction = self.model.predict(feature_vector)[0]
            return prediction
        except Exception as e:
            print(f"Error during ML prediction: {e}")
            return 1

# Singleton
anomaly_detector = AnomalyDetector()
