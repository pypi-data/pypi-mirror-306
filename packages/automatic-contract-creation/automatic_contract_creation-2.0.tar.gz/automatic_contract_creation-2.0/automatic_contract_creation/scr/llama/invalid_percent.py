from automatic_contract_creation.scr.llama.llama_model import LlamaModel
from automatic_contract_creation.scr.llama.checks import Checks
import polars as pl
import ast
import regex


class InvalidPercent(Checks, LlamaModel):
    def determine_quality_checks(self, profiler: pl.DataFrame, sample: pl.DataFrame)->dict:
        prompt = [{
            "role": "system",
            "content": """
            You are an assistant re an assistant whose main task is determinate suitable check "invalid_percent". 
            for the column when it acceptable.
            Use context below for that.
                    
            At first you'll get a polars dataframe object what consist name of columns in the table and 
            metrics that will present as an array. Every value in array it's calculated metric during some period.
            Description columns of the table:
            - 'column' - the name of column
            - 'percent_empty_strings' - it contains the percentage of empty strings that has only ''
            - 'percent_strings_with_spaces' - it contains the percentage string with spaces
            Secondly you'll get example table in polars DataFrame object. This is pristine data
            without any transformations.
            When you'll get 2 objects you have to determinate check 'invalid_percent' for 
            is applicable or not for that column. To determine the check, use the rules:
            1. If the percent_empty_strings AND/OR the percent_strings_with_spaces is low and greater than 0, 
            then the check 'invalid_percent' is applicable 
            2. All periods must be taken into account, i.e. if the rule from point 1 is applicable 
            for 2 of the 3 periods means that the check is applicable. 
            3. If the upload shows that there should be no empty lines in the string field, 
            then the check is applicable
            
            Give answer in a dictionary format.
            If check is not acceptable for the column just 
            pass it and don't add in a dictionary. 
            If you met column 'all' don't include it in a dictionary.
            If you don't identify any checks just return False.
            If you get empty polars DataFrame just return False.
            
            Here is an example how it will looks like:
            request from user(input): <polars_dataframe_profiler>, <sample>
            The answer what you have to back:
            {'<name_column1': 'invalid_value'}
            
            Don't add any comments just back dictionary!
            
            """},
            {
                "role": "user",
                "content": f"{profiler}, {sample}"
        }]

        match = regex.search(r'\{(?:[^{}]|(?R))*\}', self.get_response(prompt))
        response = match.group(0) if match else False


        return ast.literal_eval(response) if response else False
