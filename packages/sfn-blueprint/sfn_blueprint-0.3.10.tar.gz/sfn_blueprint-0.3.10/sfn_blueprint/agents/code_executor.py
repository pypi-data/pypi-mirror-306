import pandas as pd
from .base_agent import SFNAgent
import numpy as np
import textblob 
import sklearn
import nltk
import spacy


class SFNCodeExecutorAgent(SFNAgent):
    def __init__(self):
        super().__init__(name="Code Executor", role="Python Code Executor")

    def execute_task(self, task) -> pd.DataFrame:
        local_env = {'pd': pd, 'np': np, 'textblob': textblob, 'sklearn': sklearn, 'nltk': nltk, 'spacy': spacy, 'df': task.data}
        exec(task.code, local_env)
        return local_env['df']