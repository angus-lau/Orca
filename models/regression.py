import os
import h2o
from h2o.automl import H2OAutoML
from h2o.frame import H2OFrame

class Regressor:
    def __init__(self, dataset, target, max_models=20, seed=42, test=0.2, exclude=None):
        h2o.init()
        self.dataset = dataset
        self.target = target
        self.max_models = max_models
        self.seed = seed
        self.test_ratio = test
        self.exclude = exclude if exclude else []
        self.aml = None
        self.trained = False
        self._load_data()

    def _load_data(self):
        self.df = H2OFrame(self.dataset)
        self.features = [col for col in self.df.col_names if col not in self.exclude and col != self.target]
        self.train, self.test = self.df.split_frame(ratios=[1 - self.test_ratio], seed=self.seed)

    def train_model(self):
        self.aml = H2OAutoML(max_models=self.max_models, seed=self.seed)
        self.aml.train(x=self.features, y=self.target, training_frame=self.train)
        self.trained = True
        print("✅ Training complete.")
        print("🏆 Best model ID:", self.aml.leader.model_id)

    def save_best_model(self, path: str = "saved_models") -> str:
        """
        Saves the best H2O model (leader) to the given directory.
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
        """
        if not self.trained:
            raise RuntimeError("⚠️ Model not trained yet!")

        leader = self.aml.leader
        model_type = leader.algo
        model_id = leader.model_id
        training_metrics = leader.model_performance(self.train)
        test_metrics = leader.model_performance(self.test)

        summary = {
            "model_id": model_id,
            "algorithm": model_type,
            "train_r2": training_metrics.r2(),
            "train_mse": training_metrics.mse(),
            "train_rmse": training_metrics.rmse(),
            "train_mae": training_metrics.mae(),
            "test_r2": test_metrics.r2(),
            "test_mse": test_metrics.mse(),
            "test_rmse": test_metrics.rmse(),
            "test_mae": test_metrics.mae()
        }

        print("📊 Leader Model Summary:")
        for k, v in summary.items():
            print(f"  {k}: {v}")

        return summary

    def predict(self):
        """
        Predict on the test set and print first few predictions.
        """
        if not self.trained:
            raise RuntimeError("⚠️ Model not trained.")

        preds = self.aml.leader.predict(self.test)
        print("🔮 Predictions on test set:")
        print(preds.head())

    def show_leaderboard(self):
        """
        Display H2O AutoML leaderboard.
        """
        if not self.trained:
            raise RuntimeError("⚠️ Train the model first!")

        print("📈 Leaderboard:")
        print(self.aml.leaderboard.head(rows=self.aml.leaderboard.nrows))
