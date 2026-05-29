from utils import validate_column
class AnalysisTool:
    def __init__(self, df):
        self.df = df

    # -------------------------------
    # MAIN ANALYSIS FUNCTION
    # -------------------------------
    def analyze(self, query):
        query = query.lower()

        try:
            column = self._find_column(query)

            if column is None:
                return "❌ Could not find relevant column in dataset."
            
            # Validate column
            valid, error = validate_column(self.df, column)
            if not valid:
             return f"❌ {error}"
            


            # -------------------------------
            # OPERATIONS
            # -------------------------------

            if "average" in query or "mean" in query:
                result = self.df[column].mean()
                return f"📊 Average of '{column}' is {result}"

            elif "sum" in query or "total" in query:
                result = self.df[column].sum()
                return f"📊 Sum of '{column}' is {result}"

            elif "max" in query or "maximum" in query:
                result = self.df[column].max()
                return f"📊 Maximum of '{column}' is {result}"

            elif "min" in query or "minimum" in query:
                result = self.df[column].min()
                return f"📊 Minimum of '{column}' is {result}"

            elif "count" in query:
                result = self.df[column].count()
                return f"📊 Count of '{column}' is {result}"

            else:
                return "❌ Query not supported yet."

        except Exception as e:
            return f"Analysis Error: {str(e)}"

    # -------------------------------
    # COLUMN DETECTION
    # -------------------------------
    def _find_column(self, query):
        for col in self.df.columns:
            if col.lower() in query:
                return col
        return None