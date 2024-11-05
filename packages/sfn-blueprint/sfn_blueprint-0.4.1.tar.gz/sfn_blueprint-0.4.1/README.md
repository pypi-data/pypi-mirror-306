```md
# sfn_blueprint Framework

sfn_blueprint is a modular framework for rapid building of intelligent agents
to handle various data-related tasks, such as category identification,
code execution, feature suggestion generation, data analysis, and more.
These agents integrate with OpenAI to perform 
their tasks and can be extended with custom logic.

## Features

- **Base Agent**: A base class for all agents to extend.
- **Category Identification**: Automatically categorize datasets based on column names.
- **Data Cleaning Suggestions**: Generate suggestions for cleaning datasets.
- **Code Execution**: Dynamically execute code on data frames.
- **Feature Suggestion**: Get feature engineering suggestions based on your dataset.
- **Data Analysis**: Analyze datasets and return detailed statistics.

## Installation

You can install the sfn_blueprint framework via pip:

```bash
pip install sfn_blueprint
```

## Usage

### 1. Environment Setup

To use the agents, you need an API key from OpenAI. Store the key in a `.env` file in your project root directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

Ensure the `python-dotenv` package is installed to load environment variables.

### 2. Using Agents

### Example : Loading Data with `SFNDataLoader`

```python
from sfn_blueprint import SFNDataLoader, Task

task = Task(description="Load CSV data", data=open("data.csv", "rb"))

data_loader = SFNDataLoader()

# Load data into a pandas DataFrame
dataframe = data_loader.execute_task(task)
print(dataframe.head())  # Display the first few rows
```

## Contact

For any queries or issues, please contact the maintainer at `rajesh@stepfunction.ai`.
```