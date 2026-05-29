import matplotlib.pyplot as plt
from utils import validate_column


class VisualizationTool:
    def __init__(self, df):
        self.df = df

    # -------------------------------
    # MAIN VIS FUNCTION
    # -------------------------------
    def visualize(self, query):
        query = query.lower()

        try:
            column = self._find_column(query)

            if column is None:
                return None, "❌ Could not find relevant column."
            
            valid, error = validate_column(self.df, column)
            if not valid:
             return None, f"❌ {error}"

            # -------------------------------
            # HISTOGRAM
            # -------------------------------
            if "histogram" in query or "distribution" in query:
                fig, ax = plt.subplots()
                ax.hist(self.df[column].dropna())
                ax.set_title(f"Distribution of {column}")
                return fig, None

            # -------------------------------
            # BAR CHART
            # -------------------------------
            elif "bar" in query:
                fig, ax = plt.subplots()
                self.df[column].value_counts().plot(kind="bar", ax=ax)
                ax.set_title(f"Bar Chart of {column}")
                return fig, None

            # -------------------------------
            # LINE CHART
            # -------------------------------
            elif "line" in query:
                fig, ax = plt.subplots()
                self.df[column].plot(kind="line", ax=ax)
                ax.set_title(f"Line Chart of {column}")
                return fig, None

            else:
                return None, "❌ Visualization type not supported."

        except Exception as e:
            return None, f"Visualization Error: {str(e)}"

    # -------------------------------
    # COLUMN DETECTION
    # -------------------------------
    def _find_column(self, query):
        for col in self.df.columns:
            if col.lower() in query:
                return col
        return None