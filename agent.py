from llm import OllamaLLM
from data_tool import DataTool
from analysis_tool import AnalysisTool
from viz_tool import VisualizationTool
from memory import Memory
from utils import safe_execute, format_error

class DataAgent:
    def __init__(self, file):
        self.data_tool = DataTool(file)
        self.memory = Memory()
        self.viz_tool = VisualizationTool(self.data_tool.df)
        self.analysis_tool = AnalysisTool(self.data_tool.df)
        self.llm = OllamaLLM()

    def run(self, query):
        query = query.lower()
        # Initial memory log (user intent)
        self.memory.add(query, None)

        try:
            # 1. BASIC METADATA CHECKS
            if "shape" in query or "rows" in query:
                shape = self.data_tool.get_shape()
                response = f"Dataset has {shape[0]} rows and {shape[1]} columns."
            
            elif "columns" in query:
                cols = self.data_tool.get_columns()
                response = f"Columns are: {cols}"

            elif "data types" in query or "dtype" in query:
                dtypes = self.data_tool.get_dtypes()
                response = f"Data types: {dtypes}"

            elif "summary" in query or "statistics" in query:
                summary = self.data_tool.summary()
                response = f"Summary statistics: {summary}"

            elif "missing" in query:
                missing = self.data_tool.missing_values()
                response = f"Missing values: {missing}"

            elif "unique" in query:
                unique = self.data_tool.unique_values()
                response = f"Unique values: {unique}"

            # 2. VISUALIZATION ENGINE (Chain continued)
            elif any(word in query for word in ["plot", "chart", "graph", "histogram", "bar", "line"]):
                # Unpack carefully to avoid "too many values to unpack"
                result = self.viz_tool.visualize(query)
                if isinstance(result, tuple) and len(result) == 2:
                    fig, error = result
                else:
                    fig, error = result, None # Fallback if only 1 value returned
                
                if error:
                    response = f"Visualization Error: {error}"
                else:
                    response = "Chart generated successfully."
                    # If using a UI like Streamlit, you'd render 'fig' here
                    return fig 

            # 3. ANALYSIS ENGINE (Chain continued)
            elif any(word in query for word in ["average", "mean", "sum", "max", "min", "count", "total"]):
                result, error = self.analysis_tool.analyze(query)
                response = error if error else f"Analysis result: {result}"

            # 4. LLM FALLBACK (Final link in the chain)
            else:
                context = f"""
                You are a data analyst AI.
                Dataset columns: {self.data_tool.get_columns()}
                Conversation history: {self.memory.get_context()}
                Current user question: {query}
                Answer clearly and helpfully.
                """
                response = self.llm.generate(context)

            # Final Memory Update & Return
            self.memory.add(query, response)
            return response

        except Exception as e:
            # Using your format_error utility if available
            return f"Advanced Agent Error: {str(e)}"