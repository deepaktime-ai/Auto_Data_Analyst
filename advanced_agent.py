from llm import OllamaLLM  # Fixed "rom" typo
from data_tool import DataTool
from analysis_tool import AnalysisTool
from viz_tool import VisualizationTool
from memory import Memory
from utils import safe_execute, format_error

class AdvancedDataAgent:
    def __init__(self, file):
        self.data_tool = DataTool(file)
        self.analysis_tool = AnalysisTool(self.data_tool.df)
        self.viz_tool = VisualizationTool(self.data_tool.df)
        self.llm = OllamaLLM()
        self.memory = Memory()

    # -------------------------------
    # MAIN ENTRY
    # -------------------------------
    def run(self, query):
        try:
            # Step 1: Create plan
            plan = self._create_plan(query)

            # Step 2: Execute plan
            result = self._execute_plan(plan, query)

            # Step 3: Save memory (Ensures we don't try to save a Plotly object as text)
            mem_val = result if isinstance(result, str) else "Visualization generated"
            self.memory.add(query, mem_val)

            return result

        except Exception as e:
            # Use your utility to format errors nicely
            return format_error(e) if 'format_error' in globals() else f"Advanced Agent Error: {str(e)}"

    # -------------------------------
    # STEP 1: PLAN CREATION (LLM)
    # -------------------------------
    def _create_plan(self, query):
        prompt = f"""
        You are an AI data analyst.
        Available tools:
        - data_tool (dataset info like shape, columns, dtypes)
        - analysis_tool (mean, sum, max, min, count, statistics)
        - viz_tool (charts, plots, graphs)

        Dataset columns: {self.data_tool.get_columns()}
        Conversation history: {self.memory.get_context()}
        User query: {query}

        Create a simple plan. Identify if the user wants info, analysis, or a visualization.
        """
        plan = self.llm.generate(prompt)
        return plan.lower()

    # -------------------------------
    # STEP 2: PLAN EXECUTION
    # -------------------------------
    def _execute_plan(self, plan, query):
        
        # 1. Visualization (Unpack Safely)
        if any(word in plan for word in ["chart", "plot", "graph", "histogram", "bar", "line"]):
            res = self.viz_tool.visualize(query)
            # Fix for "too many values to unpack"
            fig, error = res if (isinstance(res, tuple) and len(res) == 2) else (res, None)
            return error if error else fig

        # 2. Analysis (Unpack Safely)
        elif any(word in plan for word in ["average", "mean", "sum", "max", "min", "count", "statistics"]):
            res = self.analysis_tool.analyze(query)
            # Fix for "too many values to unpack"
            result, error = res if (isinstance(res, tuple) and len(res) == 2) else (res, None)
            return error if error else f"Analysis result: {result}"

        # 3. Data Info
        elif "columns" in plan or "names" in plan:
            return f"Columns: {self.data_tool.get_columns()}"

        elif "shape" in plan or "size" in plan or "rows" in plan:
            shape = self.data_tool.get_shape()
            return f"Dataset has {shape[0]} rows and {shape[1]} columns."

        # 4. Fallback to LLM
        else:
            context = f"Execute this plan based on the data: {plan}. Query: {query}"
            return self.llm.generate(context)