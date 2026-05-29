import pandas as pd


class DataTool:
    def __init__(self, file):
        """
        Initialize with uploaded file
        """
        self.df = self.load_data(file)

    # -------------------------------
    # LOAD DATA
    # -------------------------------
    def load_data(self, file):
        try:
            df = pd.read_csv(file)
            return df
        except Exception as e:
            raise Exception(f"Error loading data: {e}")

    # -------------------------------
    # BASIC INFO
    # -------------------------------
    def get_shape(self):
        return self.df.shape

    def get_columns(self):
        return list(self.df.columns)

    def get_dtypes(self):
        return self.df.dtypes.astype(str).to_dict()

    # -------------------------------
    # DATA PREVIEW
    # -------------------------------
    def preview(self, n=5):
        return self.df.head(n)

    # -------------------------------
    # STATISTICS
    # -------------------------------
    def summary(self):
        return self.df.describe().to_dict()

    # -------------------------------
    # MISSING VALUES
    # -------------------------------
    def missing_values(self):
        return self.df.isnull().sum().to_dict()

    # -------------------------------
    # UNIQUE VALUES
    # -------------------------------
    def unique_values(self):
        return {col: self.df[col].nunique() for col in self.df.columns}