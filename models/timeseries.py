import pandas as pd
import h2o
from h2o.automl import H2OAutoML
from typing import List, Optional, Union
from datetime import timedelta
import os

class TimeSeriesModel:
    def __init__(
        self,
        dataset,
        date_column: str,
        target_column: str,
        lags: int = 5,
        max_models: int = 10,
        seed: int = 42
    ):
        """
        Initializes the TimeSeriesModel using H2O AutoML.

        :param dataset: Instance of the Dataset class.
        :param date_column: Name of the datetime column.
        :param target_column: Column to forecast.
        :param lags: Number of lag features to generate.
        :param max_models: Max models for H2O AutoML.
        :param seed: Random seed for reproducibility.
        """
        self.dataset = dataset
        self.date_column = date_column
        self.target_column = target_column
        self.lags = lags
        self.max_models = max_models
        self.seed = seed
        self.aml = None
        self.trained = False
        self._prepare_data()

    def _prepare_data(self):
        """
        Converts dataset into a supervised learning format with lag features.
        """
        df = self.dataset.get_data().copy()
        df[self.date_column] = pd.to_datetime(df[self.date_column])
        df = df.sort_values(self.date_column)

        # Generate lag features
        for i in range(1, self.lags + 1):
            df[f"lag_{i}"] = df[self.target_column].shift(i)

        df.dropna(inplace=True)
        self.supervised_df = df

        # H2O setup
        h2o.init()
        self.h2o_df = h2o.H2OFrame(df)
        self.features = [col for col in df.columns if col not in [self.target_column, self.date_column]]
        self.h2o_df[self.target_column] = self.h2o_df[self.target_column].asnumeric()

    def train(self):
        """
        Trains the H2O AutoML model.
        """
        self.aml = H2OAutoML(max_models=self.max_models, seed=self.seed)
        self.aml.train(x=self.features, y=self.target_column, training_frame=self.h2o_df)
        self.trained = True
        print("✅ Training complete.")
        print("🏆 Best model ID:", self.aml.leader.model_id)

    
    def save_best_model(self, path: str = "saved_models") -> str:
        """
        Saves the best H2O model (leader) to the given directory.

        :param path: Directory where the model will be saved.
        :return: Full path to saved model directory.
        """
        if not self.trained:
            raise RuntimeError("⚠️ Model not trained yet!")

        os.makedirs(path, exist_ok=True)
        model_path = h2o.save_model(model=self.aml.leader, path=path, force=True)
        print(f"📦 Model saved at: {model_path}")
        return model_path
    
    def get_leader_summary(self) -> dict:
        """
        Returns summary stats of the best (leader) model.

        :return: Dictionary with model ID, type, and training metrics.
        """
        if not self.trained:
            raise RuntimeError("⚠️ Model not trained yet!")

        leader = self.aml.leader
        model_type = leader.algo
        model_id = leader.model_id
        training_metrics = leader.model_performance()

        summary = {
            "model_id": model_id,
            "algorithm": model_type,
            "r2": training_metrics.r2(),
            "mse": training_metrics.mse(),
            "rmse": training_metrics.rmse(),
            "mae": training_metrics.mae(),
        }

        print("📊 Leader Model Summary:")
        for k, v in summary.items():
            print(f"  {k}: {v}")

        return summary

    def forecast(self, steps: int = 1) -> List[float]:
        """
        Forecasts future time steps using recursive predictions.

        :param steps: Number of future steps to predict.
        :return: List of predicted values.
        """
        if not self.trained:
            raise RuntimeError("Model not trained yet!")

        recent_df = self.supervised_df.sort_values(self.date_column).tail(self.lags).copy()
        predictions = []

        for _ in range(steps):
            input_data = {}

            for i in range(1, self.lags + 1):
                input_data[f"lag_{i}"] = recent_df[self.target_column].iloc[-i]

            row_df = pd.DataFrame([input_data])
            row_h2o = h2o.H2OFrame(row_df)
            pred = self.aml.leader.predict(row_h2o).as_data_frame().iloc[0, 0]
            predictions.append(pred)

            # Update recent_df for recursive prediction
            new_row = {self.target_column: pred}
            for i in range(1, self.lags):
                new_row[f"lag_{i}"] = input_data.get(f"lag_{i+1}", pred)
            new_row[f"lag_{self.lags}"] = pred
            recent_df = pd.concat([recent_df, pd.DataFrame([new_row])], ignore_index=True)


        return predictions

    def leaderboard(self):
        """
        Returns the leaderboard of H2O AutoML models.
        """
        if self.trained:
            return self.aml.leaderboard
        else:
            print("⚠️ Model not trained yet.")
            return None
