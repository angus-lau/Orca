import os
import h2o
import pandas as pd
from typing import List, Union, Optional
from h2o.automl import H2OAutoML
from sklearn.feature_extraction.text import TfidfVectorizer

class NLPModel:
    def __init__(
        self,
        dataset,
        text_columns: List[str],
        target_column: str,
        max_models: int = 10,
        max_runtime_secs: int = 60,
        max_features: int = 500,
        seed: int = 42
    ):
        self.dataset = dataset
        self.text_columns = text_columns
        self.target_column = target_column
        self.max_models = max_models
        self.max_runtime_secs = max_runtime_secs
        self.max_features = max_features
        self.seed = seed
        self.aml = None
        self.trained = False
        self.vectorizer = None
        self.feature_names = []
        self._prepare_data()

    def _prepare_data(self):
        df = self.dataset.get_data().copy()
        df = df.dropna(subset=[self.target_column])

        for col in self.text_columns:
            df[col] = df[col].fillna("")

        df["__combined_text__"] = df[self.text_columns].agg(" ".join, axis=1)

        self.vectorizer = TfidfVectorizer(max_features=self.max_features)
        tfidf_matrix = self.vectorizer.fit_transform(df["__combined_text__"])

        tfidf_df = pd.DataFrame(
            tfidf_matrix.toarray(),
            columns=self.vectorizer.get_feature_names_out()
        )
        self.feature_names = tfidf_df.columns.tolist()

        tfidf_df[self.target_column] = df[self.target_column].values

        h2o.init()
        self.h2o_df = h2o.H2OFrame(tfidf_df)

        if self._is_classification(df):
            self.h2o_df[self.target_column] = self.h2o_df[self.target_column].ascharacter()
            self.h2o_df[self.target_column] = self.h2o_df[self.target_column].asfactor()
        else:
            self.h2o_df[self.target_column] = self.h2o_df[self.target_column].asnumeric()

    def _is_classification(self, df) -> bool:
        dtype = df[self.target_column].dtype
        return dtype == "object" or str(dtype).startswith("category")

    def train(self):
        self.aml = H2OAutoML(
            max_models=self.max_models,
            max_runtime_secs=self.max_runtime_secs,
            seed=self.seed
        )
        self.aml.train(
            x=self.feature_names,
            y=self.target_column,
            training_frame=self.h2o_df
        )
        self.trained = True
        print("✅ Training complete.")
        print("🏆 Best model ID:", self.aml.leader.model_id)

    def save_best_model(self, path: str = "saved_models", model_name: Optional[str] = None) -> str:
        if not self.trained:
            raise RuntimeError("⚠️ Model not trained yet!")

        os.makedirs(path, exist_ok=True)
        model_path = h2o.save_model(model=self.aml.leader, path=path, force=True)

        if model_name:
            new_path = os.path.join(path, model_name)
            os.rename(model_path, new_path)
            print(f"📦 Model saved as: {new_path}")
            return new_path

        print(f"📦 Model saved at: {model_path}")
        return model_path

    def get_leader_summary(self) -> dict:
        if not self.trained:
            raise RuntimeError("⚠️ Model not trained yet!")

        leader = self.aml.leader
        model_type = leader.algo
        model_id = leader.model_id
        perf = leader.model_performance()

        summary = {
            "model_id": model_id,
            "algorithm": model_type,
            "r2": perf.r2() if hasattr(perf, "r2") else None,
            "mse": perf.mse(),
            "rmse": perf.rmse(),
            "mae": perf.mae(),
            "logloss": perf.logloss() if hasattr(perf, "logloss") else None,
        }

        print("📊 Leader Model Summary:")
        for k, v in summary.items():
            print(f"  {k}: {v}")

        return summary

    def leaderboard(self):
        if not self.trained:
            raise RuntimeError("⚠️ Train the model first!")
        return self.aml.leaderboard

    def predict(self, text_list: List[str]) -> List[Union[str, float]]:
        if not self.trained:
            raise RuntimeError("⚠️ Model not trained!")

        tfidf_matrix = self.vectorizer.transform(text_list)
        df = pd.DataFrame(
            tfidf_matrix.toarray(),
            columns=self.vectorizer.get_feature_names_out()
        )
        test_h2o = h2o.H2OFrame(df)
        preds = self.aml.leader.predict(test_h2o)
        return preds.as_data_frame().iloc[:, 0].tolist()
