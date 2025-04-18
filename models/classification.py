import os
import h2o
from h2o.automl import H2OAutoML
from h2o.frame import H2OFrame

class Classifier:
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
        self.df[self.target] = self.df[self.target].asfactor()
        exclude = self.exclude + [self.target]
        self.features = [col for col in self.df.col_names if col not in exclude]
        self.train, self.test = self.df.split_frame(ratios=[1 - self.test_ratio], seed=self.seed)

    def train_model(self):
        self.aml = H2OAutoML(max_models=self.max_models, seed=self.seed)
        self.aml.train(x=self.features, y=self.target, training_frame=self.train)
        self.trained = True
        print("✅ Training complete.")
        print("🏆 Best model ID:", self.aml.leader.model_id)

    def save_best_model(self, path: str = "saved_models", model_name: str = None) -> str:
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
        model_id = leader.model_id
        algo = leader.algo
        perf = leader.model_performance(self.test)

        summary = {
            "model_id": model_id,
            "algorithm": algo,
            "logloss": perf.logloss() if hasattr(perf, "logloss") else None,
            "auc": perf.auc() if hasattr(perf, "auc") else None,
            "accuracy": perf.accuracy()[0][1] if hasattr(perf, "accuracy") else None,
        }

        print("📊 Leader Model Summary:")
        for k, v in summary.items():
            print(f"  {k}: {v}")

        return summary

    def show_leaderboard(self):
        if not self.trained:
            raise RuntimeError("⚠️ Train the model first!")
        print("📈 Leaderboard:")
        print(self.aml.leaderboard.head(rows=self.aml.leaderboard.nrows))

    def predict(self):
        if not self.trained:
            raise RuntimeError("⚠️ Model not trained yet!")

        preds = self.aml.leader.predict(self.test)
        print("🔮 Predictions on test set:")
        print(preds.head())