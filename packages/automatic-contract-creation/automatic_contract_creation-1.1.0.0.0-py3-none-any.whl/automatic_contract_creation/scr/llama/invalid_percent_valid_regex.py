from automatic_contract_creation.scr.llama.llama_model import LlamaModel
from automatic_contract_creation.scr.llama.checks import Checks
import polars as pl
import ast
from typing import Union, Dict, Optional
import regex

class InvalidPercentValidRegex(Checks, LlamaModel):
    def determine_quality_checks(self, regex_dict: Optional[dict], sample: pl.DataFrame)-> Union[Dict[str, str], bool]:
        prompt = [{
            "role": "system",
            "content": r"""
            You are an assistant re an assistant whose main task is determinate suitable check 'valid_regex'
            for the column when it acceptable.
            Use context below for that.

            Context:
            At first you'll get a dictionary what consist name of columns in the table and 
            regex mask that suitable for the column. The dictionary has a structure {'<name_column>':'<regex_mask>',
            '<name_column2>':'<regex_mask>}
            Secondly you'll get example table in polars DataFrame object. This is pristine data
            without any transformations.
            When you'll get 2 objects you have to analyze pristine data use the rules:
            1. if the picture from the sample logically reflects the regular expression, then 
            the check is valid.
            2. if the column name reflects the business logic of the regular schedule, then the check is valid
            
            Pay your attention than you should analyze only columns what dictionary have.
            
            Here all regex mask what you can meet:
            'email_regex':'^[\w\.-]+@[\w\.-]+\.\w+$'
            'card_regex': '^(2200|2204)|^5[1-5]\d{2}\d{12}$|^4\d{15}$|^3[47]\d{13}$|^6\d{15,17}$|^6\d{15}$|^9860\d{12}$|^(8600|5614)\d{12}$|^94\d{14}$|^30[0-5]\d{11}$|^36\d{12}$|^38\d{12}$|^39\d{12}$'
            'uuid': '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
            'phone_number': '^(?:\+?(?:7|8|996|995|994|998|374|375|972))\d{9,10}$'
            'ip_address': '([0-9]{1,3}[\.]){3}[0-9]{1,3}'
            'web_site': '^(https?://)?(www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,63}([/\?#][a-zA-Z0-9-_=#%&.+]+)*$'
            'date': '^(19\d{2}|20\d{2})$|^(19\d{2}|20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$|^(19\d{2}|20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\s([01]\d|2[0-3]):([0-5]\d):([0-5]\d)(\.\d{2,3})?$|^(19\d{2}|20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\s([01]\d|2[0-3]):([0-5]\d):([0-5]\d)(\.\d{2,3})?\s\+([01]\d|2[0-3]):([0-5]\d)$|^(19\d{2}|20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])T([01]\d|2[0-3]):([0-5]\d):([0-5]\d)(\.\d{2,3})?$'
            'int': '^-?\d+$'
            'float': '\s*-?\d+[,.]\d+\s*$'

            Give answer in a dictionary format.
            If check is not acceptable for the column just 
            pass it and don't add in a dictionary. 
            If you don't identify any checks just return False.
            If you get empty polars DataFrame just return False.

            Here is an example how it will looks like:
            request from user(input): <dictionary_with_regex_columns_and_masks>
            The answer what you have to back: 
            {'<name_column1>':<regex_mask_from_the_input_dictionary>,
            '<name_column2>':<regex_mask_from_the_input_dictionary>}

            Don't add any comments just back dictionary!
            """
        },
            {
                "role": "user",
                "content": f"{regex_dict}, {sample}"
            }]

        match = regex.search(r'\{(?:[^{}]|(?R))*\}', self.get_response(prompt))
        response = match.group(0) if match else False


        return ast.literal_eval(response) if response else False
