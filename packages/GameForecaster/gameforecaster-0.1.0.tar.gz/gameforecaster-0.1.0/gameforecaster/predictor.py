import json
import joblib
import pandas as pd
from pathlib import Path
from typing import Dict

class GamePredictor:
    def __init__(self, model_dir='model_artifacts'):
        self.model_dir = Path(model_dir)
        self.load_model()
        
        # Features based on the training data
        self.categorical_features = ['Genre', 'Publisher', 'Developer', 'Rating']
        self.numerical_features = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 
                                   'Global_Sales', 'Critic_Score', 'Critic_Count',
                                   'User_Score', 'User_Count']
        self.features = self.categorical_features + self.numerical_features

    def load_model(self):
        """Load all necessary model artifacts."""
        try:
            self.model = joblib.load(self.model_dir / 'model.pkl')
            self.label_encoders = joblib.load(self.model_dir / 'label_encoders.pkl')
            self.scaler = joblib.load(self.model_dir / 'scaler.pkl')
            
            with open(self.model_dir / 'model_metadata.json', 'r') as f:
                self.metadata = json.load(f)
        except Exception as e:
            raise RuntimeError("Failed to load model artifacts: " + str(e))

    def preprocess_features(self, game_features: Dict) -> pd.DataFrame:
        """Preprocess input features."""
        try:
            df = pd.DataFrame([game_features])
            
            # Handle missing values
            for col in self.categorical_features:
                if col in df.columns and df[col].isnull().any():
                    df[col] = df[col].fillna('unknown')
                    
            for col in self.numerical_features:
                if col in df.columns and df[col].isnull().any():
                    df[col] = df[col].fillna(df[col].mean())
            
            # Scale numerical features
            df[self.numerical_features] = self.scaler.transform(df[self.numerical_features])
            
            # Encode categorical features
            for col in self.categorical_features:
                if col in df.columns:
                    df[col] = self.label_encoders[col].transform(df[col].astype(str))
            
            return df[self.features]
        except Exception as e:
            raise ValueError("Feature preprocessing failed: " + str(e))

    def predict(self, game_features: Dict) -> Dict:
        """Make a prediction for a single game."""
        processed_features = self.preprocess_features(game_features)
        prediction_prob = self.model.predict_proba(processed_features)[0]
        prediction = bool(prediction_prob[1] > 0.5)
        confidence = float(prediction_prob[1] if prediction else prediction_prob[0])
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'feature_importance': dict(zip(self.features, self.model.feature_importances_))
        }
