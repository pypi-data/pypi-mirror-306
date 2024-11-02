from automatic_contract_creation.scr.llama.llama_model import LlamaModel
from automatic_contract_creation.scr.connectors.connection_manager import ConnectionManager
from automatic_contract_creation.scr.connectors.connectors import Connector
import os
import pandas as pd
from dotenv import load_dotenv
import re
from typing import Dict, Tuple




load_dotenv()

class DataContextProvider(LlamaModel):
    def __init__(self, context: str):
        super().__init__(context)
        self.creds, self.table = self.get_creds()
        self.con = self.create_connection()
        self.dtypes = self.get_dtypes()


    def get_creds(self)->Tuple[Dict[str, str], str]:
        connection_name = os.getenv('connection_name')

        if connection_name == 'trino':
            pattern = r'(?P<catalog>"?([\w\-_.]*)"?)\.(?P<schema>\w+)\.(?P<table>\w+_\w+|\w+)'
            match = re.match(pattern, self.context)
            catalog_schema_table = match.group('catalog'), match.group('schema'), match.group('table')

            creds ={
                'host' : os.getenv('host'),
                'port': os.getenv('port'),
                'user': os.getenv('user'),
                'password': os.getenv('password'),
                'catalog': catalog_schema_table[0].strip(),
                'schema': catalog_schema_table[1].strip(),
            }
            table = catalog_schema_table[2].strip()

        elif connection_name=='clickhouse':
            pattern = r'(?P<db_name>"?([\w\-_.]*)"?)\.(?P<table>\w+_\w+|\w+)'
            match = re.match(pattern, self.context)
            catalog_schema_table = match.group('db_name'), match.group('table')
            table = catalog_schema_table[1].strip()

            creds ={
                'host': os.getenv('host'),
                'port': os.getenv('port'),
                'user': os.getenv('user'),
                'password': os.getenv('password'),
                'db_name' : catalog_schema_table[0].strip()
            }



        return creds, table

    def create_connection(self)-> Connector:
        connection_name = os.getenv('connection_name')

        return ConnectionManager(connection_name, **self.creds)


    def get_dtypes(self)-> pd.DataFrame:
        if os.getenv('connection_name') == 'trino':
            dtypes = self.con.get_origin_dtypes(
                f'select * from {self.creds["catalog"]}.{self.creds["schema"]}.{self.table} limit 10'
            )
        elif os.getenv('connection_name') == 'clickhouse':
            dtypes = self.con.get_origin_dtypes(
                f'select * from {self.creds['db_name']}.{self.table} limit 10'
            )
        return dtypes


