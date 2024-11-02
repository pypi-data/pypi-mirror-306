from automatic_contract_creation.scr.llama.llama_model import LlamaModel
from automatic_contract_creation.scr.llama.checks import Checks
import polars as pl
import ast
import regex


class InvalidPercentValidValues(Checks, LlamaModel):
    def determine_quality_checks(self, profiler: pl.DataFrame):
        prompt = [{
            "role": "system",
            "content": """
            You are an assistant who get a polars dataframe object with the columns and metrics. 
            You're main goal create a list of valid values to check .
            Use context below for that.

            Context:
            You'll get a polars dataframe object what consist name of columns in the table and 
            categorical columns that will present as an array. Every value in array it's calculated metric 
            during some period.
            Description columns of the table:
            - 'column' - the name of column
            - 'cat_dist' - categorical columns that present in a structure '<categorical_value>':'<percentage_of_total>'.
            You need to make a list of acceptable values, usually these are all values <categorical_value> from the
            cat_dist column but sometimes there are incorrect values. Here are some cases:
            - the variation consists of numbers and symbolic expressions come across in it, 
            then such expressions must be excluded 
            (input locale ['ru', 'il', 'uz', 'by', 'az', 'am', 'kg', 'kz', 'ge', '1'] ->
            output ['ru', 'il', 'uz', 'by', 'az', 'am', 'kg', 'kz', 'ge'])
            - the variation consists of numbers, but the business logic of the column name says that there should 
            not be such values, for example, status_id id can hardly be negative and 
            if in all 3 periods the values are positive and 1-2 negative occur, then such variations
            must be excluded (status_id input [0, 1, 4, 12, 16, 20, 128, -1] ->
            output status_id [0, 1, 4, 12, 16, 20, 128])
            
            Don't forget that you need to include all the necessary values from the three periods, 
            i.e. if in one of the periods there is a value that is not included in the rest and this value 
            does not break out of logic, then it must be included
            
            Give answer in a dictionary format.
            You have to miss all 'None' and 'nan' values and don't include them.
            If column doesn't have values in cat_dist just 
            pass it and don't add in a dictionary. 
            If you get empty polars DataFrame just return False.
            If you get get only 'None' and 'nan' values just return False.

            Here is an example how it will looks like:
            request from user(input): <polars_dataframe_profiler>
            The answer what you have to back: 
            {'<name_column1>':[<all_valid_values>],
            '<name_column2>':[<all_valid_values>]}

            Don't add any comments just back dictionary!
            """
        },
            {
                "role": "user",
                "content": f"{profiler}"
            }]

        match = regex.search(r'\{(?:[^{}]|(?R))*\}', self.get_response(prompt))
        response = match.group(0) if match else False


        return ast.literal_eval(response) if response else False
