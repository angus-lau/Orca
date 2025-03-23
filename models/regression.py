import h2o
from models.dataset import Dataset
from h2o.automl import H2OAutoML
from h2o.frame import H2OFrame

class Regressor():
    def __init__(self, dataset, target, max_models=20, seed=42, test=0.2, exclude=None):
        h2o.init()
        self.dataset = dataset
        self.target = target
        self.max_models = max_models
        self.seed = seed
        self.test = test
        self.exclude = exclude
        self.aml = None
        self.load_data()

    def load_data(self):
        self.df = H2OFrame(self.dataset)
        exclude = self.exclude if self.exclude else []
        self.features = [col for col in self.df.col_names if col not in exclude and col != self.target]
        self.train, self.test = self.df.split_frame(ratios=[1 - self.test], seed=self.seed)

    def train_model(self, max_models=20, seed=1):
        self.aml = H2OAutoML(max_models=max_models, seed=seed)
        self.aml.train(x=self.features, y=self.target, training_frame=self.train)
        self.lb = self.aml.leaderboard

    def show_leaderboard(self):
        if self.lb is not None:
            print(self.lb.head(rows=self.lb.nrows))
        else:
            print('No available leaderboard.')

    def predict(self):
        if self.aml is not None:
            preds = self.aml.leader.predict(self.test)
            print(preds.head())
        else:
            print('Model not trained.')
