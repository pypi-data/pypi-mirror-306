import pandas as pd

class ContractStructure:
    def make_structure(self, table_name:str, dtypes: pd.DataFrame)-> str:
        contract_structure = f"""dataset: {table_name}
        
columns:"""

        for nm_col in dtypes['column_name']:
            column_info = f"""
- name: {nm_col}
  data_type: {dtypes[dtypes['column_name'] == nm_col]['data_type'].values[0]}"""
            column_info += "\n"
            contract_structure += column_info

        return contract_structure
        
