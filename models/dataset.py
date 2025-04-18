"""
This python file is responsible for the dataset class
"""

import pandas as pd
from pathlib import Path
from typing import Optional, List, Union

class Dataset:
    def __init__(self, file_path: str, delimiter: str = ",", has_header: bool = True):
        """
        Initializes the Dataset class and loads the dataset.
        
        :param file_path: Path to the dataset file (CSV, Parquet, etc.).
        :param delimiter: Delimiter used in the file (default is comma for CSV files).
        :param has_header: Whether the CSV file has a header.
        """
        self._file_path = file_path
        self._delimiter = delimiter
        self._has_header = has_header
        self.data = self._load_dataset()
        self.column = self.columns()
        self.missing_val_columns = self.check_missing_value_columns()
        self.target = ""

    def get_shape(self) -> tuple:
        """
        Returns the shape of the dataset as a tuple (number of rows, number of columns).
        
        :return: Tuple containing the number of rows and columns.
        """
        print(f"Rows: {self.data.shape[0]}")
        print(f"Columns: {self.data.shape[1]}")
        return self.data.shape
    

    def head(self, n: int = 5) -> pd.DataFrame:
        """
        Returns the first n rows of the dataset.
        
        :param n: Number of rows to return. By default set to 5
        :return: Pandas DataFrame containing the first n rows.
        """
        return self.data.head(n)
    

    def tail(self, n: int = 5) -> pd.DataFrame:
        """
        Returns the last n rows of the dataset.
        
        :param n: Number of rows to return. By default set to 5
        :return: Pandas DataFrame containing the last n rows.
        """
        return self.data.tail(n)
    

    def _load_dataset(self) -> pd.DataFrame:
        """
        Loads the dataset using Pandas.
        
        :return: Pandas DataFrame containing the dataset.
        """
        try:
            if self.get_file_path().endswith(".csv"):
                return pd.read_csv(self.get_file_path(), delimiter=self.get_delimiter(), header=0 if self.get_has_header() else None)
            elif self.get_file_path().endswith(".parquet"):
                return pd.read_parquet(self.get_file_path())
            else:
                raise ValueError("Unsupported file format. Use CSV or Parquet.")
        except Exception as e:
            raise ValueError(f"Error loading dataset: {e}")
    
    
    def validate_columns(self, required_columns: List[str]) -> bool:
        """
        Validates if the dataset contains the required columns.
        
        :param required_columns: List of column names to check.
        :return: True if all columns exist, False otherwise.
        """
        return all(col in self.data.columns for col in required_columns)
    
    
    def get_summary(self) -> pd.DataFrame:
        """
        Returns a summary of the dataset including column statistics.
        
        :return: Pandas DataFrame with summary statistics.
        """
        return self.data.describe()


    def filter_rows(self, column: str, value: Union[str, int, float]) -> pd.DataFrame:
        """
        Filters rows based on a specific column value.
        
        :param column: Column name to filter on.
        :param value: Value to filter by.
        :return: Filtered Pandas DataFrame.
        """
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found in dataset.")
        return self.data[self.data[column] == value]
    

    def drop_missing(self) -> None:
        """
        Drops rows with missing values in the dataset.
        """
        null_counts = self.data.isnull().sum().sum()

        if null_counts == 0:  # If no missing values
            print("No null values found in the dataset.")
        else:
            self.data = self.data.dropna()

    

    def check_missing_value_columns(self) -> List[str]:
        """
        Checks for missing values in the dataset and returns a list of columns that have missing values.
        
        :return: List of column names with missing values.
        """
        missing_columns = [col for col in self.data.columns if self.data[col].isnull().any()]
        return missing_columns
    

    def save_dataset(self, output_path: str) -> None:
        """
        Saves the dataset to a specified path.
        
        :param output_path: File path to save the dataset (CSV or Parquet).
        """
        try:
            if output_path.endswith(".csv"):
                self.data.to_csv(output_path, index=False)
            elif output_path.endswith(".parquet"):
                self.data.to_parquet(output_path, index=False)
            else:
                raise ValueError("Unsupported file format. Use CSV or Parquet.")
        except Exception as e:
            raise ValueError(f"Error saving dataset: {e}")


    def replace_with_null(self, mark: str) -> None:
        """
        Replaces all occurrences of a given str in string columns with null values.
        """
        for col in self.data.select_dtypes(include=['object']).columns:
            self.data[col] = self.data[col].replace(mark, pd.NA)


    def dtypes(self) -> pd.DataFrame:
        """
        Returns the data types of all columns in the dataset as a Pandas DataFrame.
        
        :return: Pandas DataFrame with column names and their data types.
        """
        return pd.DataFrame({
            "column": self.data.columns,
            "dtype": self.data.dtypes
        })


    def set_dtype(self, column: str, dtype: str) -> None:
        """
        Sets the data type of a specific column.
        
        :param column: Column name to change the data type.
        :param dtype: New data type to set.
        """
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found in dataset.")
        self.data[column] = self.data[column].astype(dtype)


    def set_target(self, target_column: str = None) -> None:
        """
        Sets the target column for the Machine Learning Problem.

        :param target_column: Column name that would be used as the y to predict.
        """
        if target_column is None:
            target_column = self.data.columns[-1]

        if self.validate_columns([target_column]):
            self.target = target_column
        else:
            print(f"The column {target_column} does not exist!")


    def unique_values(self) -> dict:
        """
        Returns the unique values of columns that do not have a numeric dtype.
        
        :return: Dictionary with column names as keys and unique values as lists.
        """
        unique_values_dict = {}

        for col in self.data.select_dtypes(exclude=['number']).columns:
            unique_values_dict[col] = self.data[col].unique().tolist()

        return unique_values_dict

                

    # Getters
    def get_file_path(self):
        return self._file_path

    def get_delimiter(self):
        return self._delimiter

    def get_has_header(self):
        return self._has_header

    def get_data(self):
        return self.data
    
    def columns(self) -> List[str]:
        """
        Returns the column names of the dataset.
        
        :return: List of column names.
        """
        return self.data.columns.tolist()
    
    def get_target(self):
        return self.target

    # Setters
    def set_file_path(self, file_path: str):
        self._file_path = file_path
        self.data = self._load_dataset()  # Reload dataset if path changes

    def set_delimiter(self, delimiter: str):
        self._delimiter = delimiter
        self.data = self._load_dataset()  # Reload dataset if delimiter changes


    def set_has_header(self, has_header: bool):
        self._has_header = has_header
        self.data = self._load_dataset()  # Reload dataset if header setting changes
