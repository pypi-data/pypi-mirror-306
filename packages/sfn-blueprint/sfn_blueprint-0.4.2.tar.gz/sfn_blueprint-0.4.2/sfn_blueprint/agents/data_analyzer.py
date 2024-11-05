from .base_agent import SFNAgent

class SFNDataAnalyzerAgent(SFNAgent):
    """
    This agent analyzes the data and returns a summary of the data.
    """
    def __init__(self):
        super().__init__(name="Data Analyzer", role="Data Analysis Specialist")

    def execute_task(self, task):
        df = task.data
        return {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "duplicates": df.duplicated().sum(),
            "numeric_summary": df.describe().to_dict(),
            "categorical_summary": df.select_dtypes(include=['object']).describe().to_dict()
        }