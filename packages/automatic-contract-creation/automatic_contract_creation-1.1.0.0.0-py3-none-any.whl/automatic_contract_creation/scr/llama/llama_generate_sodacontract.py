from automatic_contract_creation.scr.llama.llama_model import LlamaModel
from automatic_contract_creation.scr.profilers.profiler_helper_trino import ProfilerHelperTrino
from automatic_contract_creation.scr.utils.contract_structure import ContractStructure

class LlamaGeneratorSODAContract(LlamaModel):
    def __init__(self, context):
        super().__init__(context)
        self.profiler_helper = ProfilerHelperTrino(self.context)


    def get_structure(self):
        contract_structure = ContractStructure().make_structure(table_name=self.profiler_helper.table,
                                                                dtypes=self.profiler_helper.dtypes)

        return contract_structure
    def generate_soda_yaml(self):
        contract_structure = self.get_structure()
        profiling = self.profiler_helper.get_profiler()

        prompt = [{
        "role": "system",
        "content": """You are an assistant who generates a data validation contract in
        the soda yaml syntax using the context below.
        
Context:
You will get a table structure with column names and data types - this is a soda contract in yaml format. 
You don't need to anything change in this structure you only need to add checks to the columns.

You also will receive a polaris library DataFrame object as input,
which will contain statistics for 3 months. Each cell will contain an array of 3 objects with metrics for each month,
respectively. You have to analyze the normal picture for the table and generate
checks that match the rules.

The rules description:
- check for missing values "not_null" 
such a check is placed on those columns in which there should be no missing values, usually a
check is inserted if there are about 95% of missing values in the column
- checking for duplicates "unique" is a check for table keys,
checks the uniqueness of the column, is set at a threshold of 97%
- validation checks (valid_min/valid_max/valid_values):
  valid_min/valid_max - this check is performed for numeric columns.  If the numeric column 
  is full 'cat_dist' in profiling that valid_values check, not valid_min/valid_max!!
  valid_values - for categorical variables. Such checks are typical only for columns that have a 
  value in the 'cat_dist' column of <profiling>! The column cat_dist has a 
  structure <name_categorical>:<percent_of_total>. You have to include only 
  all possible <name_categorical> values, if list will have None, null you must exclude this value.
  
Keep in mind that the rules are justified for a normal picture, so you need to analyze the picture in 3 months

Here is an example how it will looks like:
request from user: "<contract_structure_in_variable>, <polars_dataframe_with_3months_profiling>"

the answer that the model should give is:
"
dataset: <table_name>

columns:
- name: <name_col1>
  data_type: varchar(255)
  not_null: true

- name: <name_col2>
  data_type: bigint
  valid_min: 124799
  valid_max: 146220895

- name: <name_col3>
  data_type: decimal(4,2)
  unique: true

- name: <name_col4>
  data_type: varchar

- name: <name_col5>
  data_type: date
  not_null: true

- name: <name_col6>
  data_type: varchar(4)
  not_null: true
  valid_values: ['RU', 'BY', 'AM', 'UZ', 'KZ']

- name: <name_col7>
  data_type: smallint
  not_null: 0
  valid_min: 0
  valid_max: 6
"
You only need to give that answer without any comments!
"""
        },
            {
                "role": "user",
                "content":f'''{contract_structure}, {profiling} '''
            }
        ]



        return self.get_response(prompt)

    def get_soda_contracts(self):
        contract = self.generate_soda_yaml()
        tablename = self.profiler_helper.table
        with open(f'{tablename}_contract.yml', "w", encoding='utf-8') as log_file:
            log_file.write(str(contract) + '\n')
            print(f'File {tablename}_contract.yml saved!')


    def generate_schema_contract(self):
        with open(f'{self.profiler_helper.table}_contract.yml', "w", encoding='utf-8') as log_file:
            log_file.write(str(self.get_structure()) + '\n')
            print(f'File {self.profiler_helper.table}_contract.yml saved!')


