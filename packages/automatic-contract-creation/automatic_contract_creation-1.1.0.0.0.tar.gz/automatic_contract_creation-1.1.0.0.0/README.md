# Automatic Contract Creation

**Automatic Contract Creation** is a Python library that is designed to auto-generate various types of contracts based on the soda syntax using LLM.

### Features

In the current version, connection to DB such as Clickhouse and Trino is configured.
By connecting to the database, you can generate and/or upload a statistical report, as well as generate a soda contract.

## Get Started

### Requirements
trino==0.327.0  
clickhouse-connect==0.6.22  
pandas==2.2.3  
polars==0.20.21  
openai==1.37.0  
regex==2024.9.11  
load-dotenv==0.1.0  
python=3.11.5  
pyarrow==17.0.0  
The rule based approach uses soda version 3.3.5 (SODAGenerateContract).  
The LLM approach uses soda versions 3.1.5(LlamaGeneratorSODAContract).


### Install and run

You can install the library using pip:
```
pip install automatic-contract-creation
```
Import the necessary objects. To use all the functionality, you can contact SODAGenerator
```
from automatic_contract_creation import SODAGenerator
from automatic_contract_creation import LlamaGenerateSuite
from automatic_contract_creation import LlamaGeneratorSODAContract
```

##### To rule based approach:
Create a connection object by passing the connector type and credits in dictionary format.
Use the methods to auto-generate a contract or generate a statistical report.

##### To LLM approach:
Create a file in the virtual environment ".env" with its credits
example

```
connection_name='clickhouse or trino'
host='hostname'
port=port
user='username'
password='password'
llama_api_url='your api url for llm'



token='token_omd'
```

use your method
```
print(LlamaGenerateSuite('db_name.table_name').get_suite())# prints the tests (the path is specified by the click example)
LlamaGenerateSuite('catalog.schema.table').generate_suite()# upload a yaml file with tests (the path is specified following the example of trino)
LlamaGenerateSuite('catalog.schema.table').save_profiling()# will save the profiling
print(LlamaGeneratorSODAContract('catalog.schema.table').generate_schema_contract())# will print the contract
LlamaGeneratorSODAContract('catalog.schema.table').get_soda_contracts()# will download the yaml file with the contract
```


