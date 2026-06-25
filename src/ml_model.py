"""
ml_model.py — IPL Intelligence Hub
Win Probability prediction model with evaluation metrics, feature importance,
and confidence scoring.
"""

import logging
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, classification_report,
)

from src.constants import MODEL_FEATURES, MODEL_TEST_YEAR_CUTOFF

logger = logging.getLogger(__name__)


class WinProbabilityModel:
    """
    Logistic Regression model predicting 2nd-innings chase outcomes.
    Provides evaluation metrics, feature importance, and confidence intervals.
    """

    def __init__(self):
        self.model = LogisticRegression(max_iter=1000, class_weight="balanced", C=1.0)
        self.is_fitted = False
        self.metrics = {}
        self.feature_names = MODEL_FEATURES

    def _prepare_data(self, df: pd.DataFrame):
        """Prepare chase data for training/testing."""
        chase = df[df["innings"] == 2].copy()
        chase = chase.dropna(subset=["runs_target", "balls_remaining", "match_won_by", "batting_team"])
        chase["chase_won"] = (chase["batting_team"] == chase["match_won_by"]).astype(int)

        # Ensure features exist
        balls_bowled = 120 - chase["balls_remaining"]
        chase["runs_needed"] = (chase["runs_target"] - chase["cumulative_runs"]).clip(lower=0)
        chase["required_run_rate"] = np.where(
            chase["balls_remaining"] > 0,
            (chase["runs_needed"] * 6) / chase["balls_remaining"],
            0,
        )
        chase["current_run_rate"] = np.where(
            balls_bowled > 0,
            (chase["cumulative_runs"] * 6) / balls_bowled,
            0,
        )
        chase["wickets_lost"] = chase["cumulative_wickets"]
        return chase

    def train(self, df: pd.DataFrame):
        """Train the model on pre-cutoff data, evaluate on post-cutoff data."""
        chase = self._prepare_data(df)

        X = chase[self.feature_names]
        y = chase["chase_won"]
        years = chase["year"]

        # Chronological split
        train_mask = years < MODEL_TEST_YEAR_CUTOFF
        X_train, X_test = X[train_mask], X[~train_mask]
        y_train, y_test = y[train_mask], y[~train_mask]

        logger.info(f"Training on {len(X_train):,} samples, testing on {len(X_test):,} samples")

        self.model.fit(X_train, y_train)
        self.is_fitted = True

        # Predictions
        y_pred = self.model.predict(X_test)
        y_prob = self.model.predict_proba(X_test)[:, 1]

        # Store metrics
        self.metrics = {
            "accuracy": round(accuracy_score(y_test, y_pred) * 100, 1),
            "precision": round(precision_score(y_test, y_pred, zero_division=0) * 100, 1),
            "recall": round(recall_score(y_test, y_pred, zero_division=0) * 100, 1),
            "f1": round(f1_score(y_test, y_pred, zero_division=0) * 100, 1),
            "roc_auc": round(roc_auc_score(y_test, y_prob), 4) if len(set(y_test)) > 1 else 0.0,
            "train_size": len(X_train),
            "test_size": len(X_test),
        }

        # ROC curve data
        if len(set(y_test)) > 1:
            fpr, tpr, _ = roc_curve(y_test, y_prob)
            self.roc_data = {"fpr": fpr.tolist(), "tpr": tpr.tolist()}
        else:
            self.roc_data = {"fpr": [0, 1], "tpr": [0, 1]}

        # Confusion matrix
        self.conf_matrix = confusion_matrix(y_test, y_pred).tolist()

        logger.info(f"Model trained. ROC-AUC: {self.metrics['roc_auc']}")

    def predict_live(self, runs_needed: float, balls_remaining: int,
                     wickets_lost: int, rrr: float, crr: float) -> dict:
        """
        Predict win probability with confidence assessment.
        Returns probability, confidence level, and match situation label.
        """
        if not self.is_fitted:
            return {"probability": 0.5, "confidence": "Low", "situation": "Model not trained"}

        features = np.array([[runs_needed, balls_remaining, wickets_lost, rrr, crr]])
        prob = self.model.predict_proba(features)[:, 1][0]

        # Confidence based on distance from 0.5
        distance = abs(prob - 0.5)
        if distance >= 0.3:
            confidence = "High"
        elif distance >= 0.15:
            confidence = "Medium"
        else:
            confidence = "Low"

        # Situation label
        if prob >= 0.75:
            situation = "Strongly Favoring Chasing Team"
        elif prob >= 0.60:
            situation = "Chasing Team Slightly Ahead"
        elif prob >= 0.40:
            situation = "Evenly Balanced Contest"
        elif prob >= 0.25:
            situation = "Defending Team Slightly Ahead"
        else:
            situation = "Strongly Favoring Defending Team"

        return {
            "probability": round(prob, 4),
            "confidence": confidence,
            "situation": situation,
        }

    def get_feature_importance(self) -> pd.DataFrame:
        """Return feature importance based on model coefficients."""
        if not self.is_fitted:
            return pd.DataFrame()
        coefs = self.model.coef_[0]
        importance = pd.DataFrame({
            "Feature": self.feature_names,
            "Coefficient": coefs,
            "Abs_Importance": np.abs(coefs),
        }).sort_values("Abs_Importance", ascending=True)

        # Readable labels
        label_map = {
            "runs_needed": "Runs Needed",
            "balls_remaining": "Balls Remaining",
            "wickets_lost": "Wickets Lost",
            "required_run_rate": "Required Run Rate",
            "current_run_rate": "Current Run Rate",
        }
        importance["Label"] = importance["Feature"].map(label_map)
        return importance


@st.cache_resource(show_spinner="Training ML model…")
def get_trained_model(df: pd.DataFrame) -> WinProbabilityModel:
    """Train and cache the win probability model."""
    model = WinProbabilityModel()
    model.train(df)
    return model
