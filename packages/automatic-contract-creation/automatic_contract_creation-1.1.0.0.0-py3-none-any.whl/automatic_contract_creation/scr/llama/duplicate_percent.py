from automatic_contract_creation.scr.llama.llama_model import LlamaModel
from automatic_contract_creation.scr.llama.checks import Checks
import polars as pl
import ast
import regex





class DuplicatePercent(Checks, LlamaModel):
    def determine_quality_checks(self, profiler: pl.DataFrame=None):
        prompt =[{
            "role":"system",
            "content":"""You are an assistant who get a polars dataframe object with the columns and metrics. 
            You're main goal determinate suitable check "duplicate_percent" for the column when it acceptable
            and return the answer in a dictionary format.
            Use context below for that.
            
            Context:
            You'll get a polars dataframe object what consist name of columns in the table and 
            metrics that will present as an array. Every value in array it's calculated metric during some period.
            Description columns of the table:
            - "column" - the name of column
            - "percent_dup" - this is main metrics for determinate check "duplicate_percent"
            here calculated percent duplicate during period. Usually check 
            suitable if here is really low percent. But remember that you have to analyze 
            normal picture for the column. This mean that if in array you have 3 values in a array
            and 2 from 3 have low percent and, on the contrary 1 have is very high the check "duplicate_percent"
            will acceptable for that column.
            - "null_count" - here is the percentage of null value in the column. This metric have some 
            correlation with the "percent_dup" metric. For example if "percent_dup" is 0.01% and 
            "null_count" is 99% that's means that column can have duplicates because only 1% of the table is filled
            and check "duplicate_percent" unacceptable.
            - "cat_dist" if you have some value in this column the check "duplicate_percent" never 
            will acceptable for that column.
            
            If column have something in the name what have connection with the money
            for example name of column contain 'price' or 'payment' then this will  
            the check "duplicate_percent"!
            
            If the column name indicates that it contains a categorical variable, 
            for example, there is a '_type' in the name column, then the check "duplicate_percent" 
            unacceptable!
            
            You should determinate what percent should be in the check "duplicate_percent",based on a 
            all value in an array. Give answer in a dictionary format.
            If check is not acceptable for the column just 
            pass it and don't add in a dictionary. 
            If you met column 'all' don't include it in a dictionary.
            If you don't identify any checks just return False.
            If you get empty polars DataFrame just return False.
            
            Here is an example how it will looks like:
            request from user(input): <polars_dataframe_profiler>
            The answer what you have to back: {'<name_column1>':<acceptable_percentage>,
            '<name_column2>':<acceptable_percentage>}
            
            
            Don't add any comments just back dictionary!
            """
        },
        {
            "role":"user",
            "content":f"{profiler}"
        }]

        match = regex.search(r'\{(?:[^{}]|(?R))*\}', self.get_response(prompt))
        response = match.group(0) if match else False

        return ast.literal_eval(response) if response else False
