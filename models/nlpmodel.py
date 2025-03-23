import h2o
from h2o.automl import H2OAutoML
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Union


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
        """
        NLP model using TF-IDF Bag-of-Words + H2O AutoML.

        :param dataset: Instance of your Dataset class.
        :param text_columns: List of text columns to combine as input.
        :param target_column: The column to predict.
        :param max_models: Number of models to train.
        :param max_runtime_secs: Time budget (in seconds) for AutoML.
        :param max_features: Max TF-IDF features.
        :param seed: Random seed for reproducibility.
        """
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
        """
        Prepares dataset: combines text, vectorizes with TF-IDF, creates H2O frame.
        """
        df = self.dataset.get_data().copy()
        df = df.dropna(subset=[self.target_column])

        for col in self.text_columns:
            df[col] = df[col].fillna("")

        df["__combined_text__"] = df[self.text_columns].agg(" ".join, axis=1)

        # TF-IDF vectorization
        self.vectorizer = TfidfVectorizer(max_features=self.max_features)
        tfidf_matrix = self.vectorizer.fit_transform(df["__combined_text__"])

        # Convert sparse matrix to DataFrame
        tfidf_df = pd.DataFrame(
            tfidf_matrix.toarray(),
            columns=self.vectorizer.get_feature_names_out()
        )
        self.feature_names = tfidf_df.columns.tolist()

        # Combine with target
        tfidf_df[self.target_column] = df[self.target_column].values

        # Init H2O
        h2o.init()
        self.h2o_df = h2o.H2OFrame(tfidf_df)

        # Set correct target type
        if self._is_classification(df):
    # 👇 Cast to string BEFORE H2O conversion
            self.h2o_df[self.target_column] = self.h2o_df[self.target_column].ascharacter()
            self.h2o_df[self.target_column] = self.h2o_df[self.target_column].asfactor()
        else:
            self.h2o_df[self.target_column] = self.h2o_df[self.target_column].asnumeric()

    def _is_classification(self, df) -> bool:
        """
        Determines if the target is categorical.
        """
        dtype = df[self.target_column].dtype
        return dtype == "object" or str(dtype).startswith("category")

    def train(self):
        """
        Trains H2O AutoML model.
        """
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

    def leaderboard(self):
        """
        Returns leaderboard of models.
        """
        if not self.trained:
            raise RuntimeError("⚠️ Train the model first!")
        return self.aml.leaderboard

    def predict(self, text_list: List[str]) -> List[Union[str, float]]:
        """
        Predicts outcomes from raw text input.

        :param text_list: List of raw input strings.
        :return: List of predicted values.
        """
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