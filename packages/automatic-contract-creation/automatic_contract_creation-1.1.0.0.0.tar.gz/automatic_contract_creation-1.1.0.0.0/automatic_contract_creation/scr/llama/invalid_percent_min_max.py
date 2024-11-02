from automatic_contract_creation.scr.llama.llama_model import LlamaModel
from automatic_contract_creation.scr.llama.checks import Checks
import polars as pl
import regex
import ast


class InvalidPercentMinMax(Checks, LlamaModel):
    def determine_quality_checks(self, profiler: pl.DataFrame, sample: pl.DataFrame):
        prompt = [{
            "role": "system",
            "content": """
            You are an assistant who receives a polars dataframe object with columns and metrics. 
            Your main goal is to determine the appropriate 'valid_min/valid_max' check for the column when it is acceptable and return the answer in dictionary format.
            Use the context given below to do this.

            Context:
            First you will get a polars dataframe object, which contains the names of columns in 
            the table and metrics, which will be presented as an array. Each value in the array is a 
            calculated metric for a certain period.
            Description of the table columns:
            - 'column' - column name
            - 'minimum' - contains the minimum for numbers and dates.
            - 'maximum' - contains the maximum for numbers and dates.
            Secondly, you will get an example table in the polars DataFrame object. This is the 
            initial data without any transformations.
            When you get 2 objects, you have to determine whether the 'invalid_percent' check for 
            'valid_min/valid_max' is acceptable or not
            for this column. To determine whether a check is acceptable or not, use the rules:
            1. if the minimum and maximum are filled in the column in the profiling, then this can be 
            a check, but only if you find some logic from paragraph 2!
            2. if paragraph 1 is fulfilled, then you need to analyze the column name, and this
            the essence of the business, for example, if the name is price, then it cannot be negative,
            then the minimum value should be >=0, or the column name is discount, then discount 
            it cannot be more than 100%, and then the maximum value will be = 1.
            3. If paragraph 1 is fulfilled, and the column name does not contain any business logic,
            then verification is not applicable, for example, the name of the currency_id column 
            does not contain any business logic for verification, and it is impossible to determine 
            with certainty which currency identifier will be the maximum or minimum.
            4. if the 'invalid_percent' check is correct, then the maximum AND/OR minimum value 
            falls into an explicit outlier (for example, 100000000000 for the price), then it is 
            better not to include such values, but you can determine the maximum / minimum by the sample 
            that you received at the entrance.
            5. If the minimum and maximum contain a date, then this will never be a check and 
            it will never be applicable. 
            6. If there is an '_id' in the column name, then this is unlikely will be applicable and never 
            will have maximum. Maximum in this type of columns always False and minimum almost always 0.
            7. Remember that this check is used very rarely, so it is necessary to strictly follow the 
            rules from paragraphs 1-5. 
            
            If the check is applicable, you should determine what minimum or maximum should be 
            in the 'valid_min/valid_max' check based on the business logic of the rules and all 
            the values in the array. Also remember about rule from point 6! 
            If there is an '_id' in the column name,  then this is unlikely will be applicable and never 
            will have maximum. Maximum in this type of columns always False and minimum almost always 0.
            The verification may include at least
            either the maximum, or both (minimum and maximum). 
            
            Give the answer in dictionary format.
            If the check is invalid for a column, just 
            pass it on and don't add it to the dictionary. 
            If you encounter the 'all' column, do not include it in the dictionary.
            If you haven't defined any checks, just return False.
            If you get an empty polars data frame, just return False.
            If the reconciliation is applicable only for the minimum, 
            then set the value to False for the maximum.
            If the reconciliation is applicable only for the maximum, 
            then set the value to False for the minimum.

            Here is an example how it will looks like:
            request from user(input): <polars_dataframe_profiler>, <sample>
            The answer what you have to back: 
            '{
            '<name_column1>':{
                                'minimum':<acceptable_value_min>,
                                'maximum' <acceptable_value_max>},
            '<name_column2>':{
                                'minimum':<acceptable_value_min>,
                                'maximum': False}
            }'

            Don't add any comments just back dictionary!
            """
        },
            {
                "role": "user",
                "content": f"{profiler}, {sample}"
            }]

        match = regex.search(r'\{(?:[^{}]|(?R))*\}', self.get_response(prompt))
        response = match.group(0) if match else False

        return ast.literal_eval(response) if response else False
