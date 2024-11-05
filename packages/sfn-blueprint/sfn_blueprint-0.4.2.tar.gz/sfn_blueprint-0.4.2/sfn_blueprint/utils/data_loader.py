import pandas as pd
from sfn_blueprint.agents.base_agent import SFNAgent

class SFNDataLoader(SFNAgent):
    def __init__(self):
        super().__init__(name="Data Loader", role="Data Loading Specialist")

    def execute_task(self, task) -> pd.DataFrame:
        file_obj = task.data
        if file_obj.name.endswith('.csv'):
            return pd.read_csv(file_obj, index_col=0,low_memory=False)
        elif file_obj.name.endswith('.xlsx'):
            return pd.read_excel(file_obj, index_col=0)
        elif file_obj.name.endswith('.json'):
            return pd.read_json(file_obj)
        elif file_obj.name.endswith('.parquet'):
            return pd.read_parquet(file_obj)
        else:
            raise ValueError("Unsupported file format. Please provide a CSV, Excel, JSON, Parquet file.")