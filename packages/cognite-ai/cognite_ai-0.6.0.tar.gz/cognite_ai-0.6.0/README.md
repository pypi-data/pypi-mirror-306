# cognite-ai

A set of AI tools for working with CDF (Cognite Data Fusion) in Python, including vector stores and intelligent data manipulation features leveraging large language models (LLMs).

# Installation

This package is intended to be used in Cognite's Jupyter notebook and Streamlit. To get started, install the package using:

```bash
%pip install cognite-ai
```

## MemoryVectorStore

The `MemoryVectorStore` allows you to store and query vector embeddings created from text, enabling use cases where the number of vectors is relatively small.

### Example

You can create vectors from text (either as individual strings or as a list) and query them:

```python
from cognite.ai import MemoryVectorStore
from cognite.client import CogniteClient

client = CogniteClient()
# Create a MemoryVectorStore instance
vector_store = MemoryVectorStore(client)

# Store text as vectors
vector_store.store_text("The compressor in unit 7B requires maintenance next week.")
vector_store.store_text("Pump 5A has shown signs of decreased efficiency.")
vector_store.store_text("Unit 9 is operating at optimal capacity.")

# Query vector store
vector_store.query_text("Which units require maintenance?")
```

---

## Smart Data Tools

With `cognite-ai`, you can enhance your data workflows by integrating LLMs for intuitive querying and manipulation of data frames. The module is built on top of [PandasAI](https://docs.pandas-ai.com/en/latest/) and adds Cognite-specific features.

The Smart Data Tools come in three components:

Pandas Smart DataFrame
Pandas Smart DataLake
Pandas AI Agent

### 1. Pandas Smart DataFrame

`SmartDataframe` enables you to chat with individual data frames, using LLMs to query, summarize, and analyze your data conversationally.

#### Example

```python
from cognite.ai import load_pandasai
from cognite.client import CogniteClient
import pandas as pd

# Load the necessary classes
client = CogniteClient()
SmartDataframe, SmartDatalake, Agent = await load_pandasai()

# Create demo data
workorders_df = pd.DataFrame({
    "workorder_id": ["WO001", "WO002", "WO003", "WO004", "WO005"],
    "description": [
        "Replace filter in compressor unit 3A",
        "Inspect and lubricate pump 5B",
        "Check pressure valve in unit 7C",
        "Repair leak in pipeline 4D",
        "Test emergency shutdown system"
    ],
    "priority": ["High", "Medium", "High", "Low", "Medium"]
})

# Create a SmartDataframe object
s_workorders_df = SmartDataframe(workorders_df, cognite_client=client)

# Chat with the dataframe
s_workorders_df.chat('Which 5 work orders are the most critical based on priority?')
```

#### Customizing LLM Parameters

You can configure the LLM parameters to control aspects like model selection and temperature.

```python
params = {
    "model": "gpt-35-turbo",
    "temperature": 0.5
}

s_workorders_df = SmartDataframe(workorders_df, cognite_client=client, params=params)
```

### 2. Pandas Smart DataLake

`SmartDatalake` allows you to combine and query multiple data frames simultaneously, treating them as a unified data lake.

#### Example

```python
from cognite.ai import load_pandasai
from cognite.client import CogniteClient
import pandas as pd

# Load the necessary classes
client = CogniteClient()
SmartDataframe, SmartDatalake, Agent = await load_pandasai()

# Create demo data
workorders_df = pd.DataFrame({
    "workorder_id": ["WO001", "WO002", "WO003"],
    "asset_id": ["A1", "A2", "A3"],
    "description": ["Replace filter", "Inspect pump", "Check valve"]
})
workitems_df = pd.DataFrame({
    "workitem_id": ["WI001", "WI002", "WI003"],
    "workorder_id": ["WO001", "WO002", "WO003"],
    "task": ["Filter replacement", "Pump inspection", "Valve check"]
})
assets_df = pd.DataFrame({
    "asset_id": ["A1", "A2", "A3"],
    "name": ["Compressor 3A", "Pump 5B", "Valve 7C"]
})

# Combine them into a smart lake
smart_lake_df = SmartDatalake([workorders_df, workitems_df, assets_df], cognite_client=client)

# Chat with the unified data lake
smart_lake_df.chat("Which assets have the most work orders associated with them?")
```

### 3. Pandas AI Agent

The `Agent` provides conversational querying capabilities across a single data frame, allowing you to have follow up questions.

#### Example

```python
from cognite.ai import load_pandasai
from cognite.client import CogniteClient
import pandas as pd

# Load the necessary classes
client = CogniteClient()
SmartDataframe, SmartDatalake, Agent = await load_pandasai()

# Create example data
sensor_readings_df = pd.DataFrame({
    "sensor_id": ["A1", "A2", "A3", "A4", "A5"],
    "temperature": [75, 80, 72, 78, 69],
    "pressure": [30, 35, 33, 31, 29],
    "status": ["Normal", "Warning", "Normal", "Warning", "Normal"]
})

# Create an Agent for the dataframe
agent = Agent(sensor_readings_df, cognite_client=client)

# Ask a question
print(agent.chat("Which sensors are showing a warning status?"))
```

# Contributing

This package exists mainly to provide a in memory vector store
in addition to getting around the install problems
a user gets in Pyodide when installing `pandasai` due to
dependencies that are not pure Python 3 wheels.

The current development cycle is not great, but consists of copying the contents
of the source code in this package into e.g. a Jupyter notebook
in Fusion to verify that everything works there.
