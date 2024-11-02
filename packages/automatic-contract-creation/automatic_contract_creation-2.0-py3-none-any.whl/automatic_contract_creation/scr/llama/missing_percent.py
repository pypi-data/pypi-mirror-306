from automatic_contract_creation.scr.llama.llama_model import LlamaModel
from automatic_contract_creation.scr.llama.checks import Checks
import polars as pl
import ast
import regex

class MissingPercent(Checks, LlamaModel):
    def determine_quality_checks(self, profiler: pl.DataFrame, sample: pl.DataFrame):
        prompt = [{
            "role": "system",
            "content": """
            You are an assistant whose main task is determinate suitable check 'missing_percent' for the column 
            when it acceptable.
            Use context below for that.

            Context:
            At first you'll get a polars dataframe object what consist name of columns in the table and 
            metrics that will present as an array. Every value in array it's calculated metric during some period.
            Description columns of the table:
            - 'column' - the name of column
            - 'null_count' - it contains the percentage of missing values. This is one of the main metrics 
            for determining check 'missing_percent', if the percentage is low here, then verification is acceptable.
            But remember that you have to analyze normal picture for the column. This mean that 
            if in array you have 3 values in a array and 2 from 3 have low percent and, 
            on the contrary 1 have is very high the check 'missing_percent'
            will acceptable for that column.
            - 'quantile_95_morning' - the 95% percentile is the number of rows per hour from 9:00:00 am to 23:59:59.
            - 'quantile_95_night' - The 95% percentile is the number of rows per hour from 00:00:00  am to 8:59:59.
            Secondly you'll get example table in polars DataFrame object. This is pristine data
            without any transformations.
            
            When you'll get 2 objects you have to determinate check 'missing_percent' is acceptable or not
            for that column. If it acceptable you have to determinate acceptable percentage for the check
            'missing_percent'. To determine the check, use the rules:
            1. if the percentage of missing values (null_count) is low, then the check is applicable.
            2. it's necessary to take into account all periods, i.e. if the rule from point 1 is applicable 
            for 2 of the 3 periods, then the check is acceptable
            4. it is necessary to analyze a sample of 100 thousand lines, 
            if the picture from the sample shows that there should be no missing values 
            with a certain filtration (maximum when filtering by 1 column), then checking is acceptable with a filter.
            For example you have columns 'blob__delivery__p_id' (type delivery) and 'blob__delivery__sm_id' (id
            delivery) you recognize that if the type of delivery is 7, 
            then the ID of the pick-up point must be indicated. Then the filter 
            will looks like: blob__delivery__sm_id = '6'
            5. if the check is valid, it is necessary to determine the acceptable percentage based 
            on the quantiles - take the average value from the quantiles for 3 periods and 
            convert it to a 100% scale, i.e. the maximum allowable value is 1, there will never be more 
            than 1. Usually the percentage of acceptable values does not exceed 0.05 and most often it is 0.

            Give answer in a dictionary format.
            If check accaptable with the filter full filter with the 
            filter value, if check accaptable without filter full filter 'without filter'
            If check is not acceptable for the column just 
            pass it and don't add in a dictionary. 
            If you met column 'all' don't include it in a dictionary.
            If you don't identify any checks just return False.
            If you get empty polars DataFrame just return False.

            Here is an example how it will looks like:
            request from user(input): <polars_dataframe_profiler>
            The answer what you have to back: 
            {'<name_column1>':
                            {'percantage':<acceptable_percentage>,
                            'ftlter_val': 'without filter'},
            {'<name_column2>':
                            {'percantage':<acceptable_percentage>,
                            ftlter_val': <recognized_filter>}
            }

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
