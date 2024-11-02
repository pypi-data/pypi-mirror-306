from automatic_contract_creation.scr.profilers.profiler_helper_trino import ProfilerHelperTrino
from automatic_contract_creation.scr.profilers.profiler_helper_click import ProfilerHelperClick
from automatic_contract_creation.scr.llama.llama_model import LlamaModel
from automatic_contract_creation.scr.llama.duplicate_percent import DuplicatePercent
from automatic_contract_creation.scr.llama.missing_percent import MissingPercent
from automatic_contract_creation.scr.llama.invalid_percent_min_max import InvalidPercentMinMax
from automatic_contract_creation.scr.llama.invalid_percent_valid_values import InvalidPercentValidValues
from automatic_contract_creation.scr.llama.invalid_percent_valid_regex import InvalidPercentValidRegex
from automatic_contract_creation.scr.llama.invalid_percent import InvalidPercent
from automatic_contract_creation.scr.utils.omd_client import OMDClient
from automatic_contract_creation.scr.llama.llama_description import LlamaDescription




import polars as pl

from dotenv import load_dotenv
import os

load_dotenv()


class LlamaGenerateSuite(LlamaModel):
    def __init__(self, context):
        self.context = context
        self.helper= ProfilerHelperTrino(context) if os.getenv('connection_name')=='trino' else ProfilerHelperClick(context)
        self.profiler =self.helper.get_profiler()
        self.sample = self.helper.get_sample()
        self.regex =self.helper.get_regex_columns()



    def get_exist_cols(self, check: str=None):
        all_columns = self.profiler.columns
        if check=='duplicates_percentage':
            columns = [x for x in ['column', 'percent_dup', 'null_percent', 'cat_dist'] if x in all_columns]
        if check=='missing_percent':
            columns = [x for x in ['column', 'null_percent', 'quantile_95_morning', 'quantile_95_night'] if x in all_columns]
        if check=='invalid_percent_min_max':
            columns =[x for x in ['column', 'minimum', 'maximum'] if x in all_columns]
        if check=='invalid_percent_valid_values':
            columns =[x for x in ['column', 'cat_dist'] if x in all_columns]
        if check=='invalid_percent_invalid_values':
            columns =[x for x in ['column', 'percent_empty_strings','percent_strings_with_spaces'] if x in all_columns]

        return columns


    def get_percentage_duplicates_check(self):
        """
        Exclude columns where cat_dist exist to not disrupting a model
        """
        profiler =self.profiler.select(
                pl.col(self.get_exist_cols(check='duplicates_percentage')),
            )
        if 'cat_dist' in profiler.columns:
            profiler = profiler.with_columns(
                pl.col("cat_dist").list.eval(
                    pl.element().is_null())
            ).filter(
                pl.col('cat_dist')==[True, True, True]
            )
        duplicate_percent = DuplicatePercent(self.context).determine_quality_checks(
            profiler=profiler
        )

        return duplicate_percent


    def get_missing_percent_check(self):
        missing_percent = MissingPercent(self.context).determine_quality_checks(
            profiler = self.profiler.select(
            pl.col(self.get_exist_cols(check='missing_percent')),
            ),
            sample=self.sample
        )
        return missing_percent

    def get_invalid_percent_min_max_check(self):
        invalid_percent_min_max= InvalidPercentMinMax(self.context).determine_quality_checks(
            profiler = self.profiler.select(
                self.get_exist_cols(check='invalid_percent_min_max'),
            ),
            sample=self.sample
        )

        return invalid_percent_min_max


    def get_invalid_percent_valid_values_check(self):
        invalid_percent_valid_values= InvalidPercentValidValues(self.context).determine_quality_checks(
            self.profiler.select(pl.col(self.get_exist_cols(check='invalid_percent_valid_values'))),
        )

        return invalid_percent_valid_values

    def get_invalid_percent_valid_regex_check(self):
        invalid_regex = InvalidPercentValidRegex(self.context).determine_quality_checks(
            regex_dict=self.regex,
            sample=self.sample
        )

        return invalid_regex

    def get_invalid_percent_invalid_values_check(self):
        invalid_percent = InvalidPercent(self.context).determine_quality_checks(
            profiler=self.profiler.select(
                pl.col(self.get_exist_cols(check='invalid_percent_invalid_values')),
                       ),
            sample=self.sample
        )

        return invalid_percent


    def get_suite_dict(self):
        duplicate_percent = self.get_percentage_duplicates_check()
        missing_percent = self.get_missing_percent_check()
        invalid_percent_min_max = self.get_invalid_percent_min_max_check()
        invalid_percent_valid_values = self.get_invalid_percent_valid_values_check()
        invalid_percent_valid_regex = self.get_invalid_percent_valid_regex_check()
        invalid_percent_invalid_values = self.get_invalid_percent_invalid_values_check()

        suits_dict = {}

        if duplicate_percent:
            for key, val in duplicate_percent.items():
                suits_dict[key] ={'duplicate_percent':val}

        if missing_percent:
            for key, val in missing_percent.items():
                if key in suits_dict:
                    suits_dict[key]['missing_percent'] = val
                else:
                    suits_dict[key] = {'missing_percent': val}


        if invalid_percent_min_max:
            for key, val in invalid_percent_min_max.items():
                if key in suits_dict:
                    suits_dict[key]['invalid_percent_min_max'] = val
                else:
                    suits_dict[key] = {'invalid_percent_min_max': val}

        if invalid_percent_valid_values:
            for key, val in invalid_percent_valid_values.items():
                if key in suits_dict:
                    suits_dict[key]['invalid_percent_valid_values'] = val
                else:
                    suits_dict[key] = {'invalid_percent_valid_values': val}

        if invalid_percent_valid_regex:
            for key, val in invalid_percent_valid_regex.items():
                if key in suits_dict:
                    suits_dict[key]['invalid_percent_valid_regex'] = val
                else:
                    suits_dict[key] = {'invalid_percent_valid_regex': val}

        if invalid_percent_invalid_values:
            for key, val in invalid_percent_invalid_values.items():
                if key in suits_dict:
                    suits_dict[key]['invalid_percent_invalid_values'] = val
                else:
                    suits_dict[key] = {'invalid_percent_invalid_values': val}


        return suits_dict

    def get_description(self):
        columns_desc = OMDClient(base_url='https://metadata.wb.ru',
                             token=os.getenv('token')
                      ).get_table(f'HIVE.{self.helper.creds["catalog"]}.{self.helper.creds["schema"]}.{self.helper.table}').columns

        df_col_desc = pl.DataFrame(schema={'column_name': str, 'description': str})
        for col in columns_desc:
            if col.description!='' and col.description is not None:
                desc = LlamaDescription(self.context).get_business_description(col.name, col.description)
            else:
                desc = col.description
            df_col_desc.extend(pl.DataFrame({'column_name': col.name, 'description': desc}))

        return df_col_desc



    def get_suite(self)-> str:
        suite_dict = self.get_suite_dict()
        if os.getenv('connection_name')=='trino':
            check_names = self.get_description() if os.getenv('connection_name')=='trino' else None
        else:
            check_names=None

        yaml_suits=f"""
checks for {self.helper.table}:
  -row_count > 0
      name: Проверка на выявление аномалий в количестве событий за период.
            Должно приходить больше 0 событий за период.
      
  - duplicate_percent=0
      name: Не должно быть полных дублей в таблице.
        """


        if suite_dict:
            for col, checks in suite_dict.items():
                for check, val in checks.items():
                    if os.getenv('connection_name')=='trino':
                        business_desc = check_names.filter(pl.col('column_name') == col).select(pl.col('description')) if not check_names.is_empty() else None
                        business_desc = business_desc[0, 0] if business_desc.height > 0 else None
                    else:
                        business_desc = None
                    if 'duplicate_percent' in check:
                        duplicate_value = checks['duplicate_percent']
                        yaml_suits += f""" 
  - duplicate_percent({col}){'=0' if duplicate_value==0 else '<'+str(duplicate_value)}
      name: """

                        if business_desc is not None and business_desc!='':
                            yaml_suits+=f"""Не должно быть одинаковых значений по {business_desc}.\n"""
                        yaml_suits+=f"""Не должно быть одинаковых значений по {col}.\n"""

                    if 'missing_percent' in check:
                        missing_value = checks['missing_percent'].get('percentage', None)
                        filter_missing = checks['missing_percent'].get('ftlter_val', None)
                        if missing_value is not None:
                            yaml_suits += f"""  
  - missing_percent({col}){'=0' if missing_value==0 else '<'+str(missing_value)}
      name: """

                            if filter_missing!='without filter' and filter_missing is not None:
                                yaml_suits += f"""filter: {filter_missing}\n"""


                            if filter_missing=='without filter':
                                if business_desc is not None and business_desc != '':
                                    yaml_suits += f"""Не должно быть строк с пропущенным значением по {business_desc}.\n"""
                                yaml_suits += f"""{col} не должен быть равен null.\n"""


                            if filter_missing!='without filter':
                                if business_desc is not None and business_desc != '':
                                    yaml_suits+= f"Не должно быть строк с пропущенным значением по {business_desc} при условии {filter_missing}.\n"
                                yaml_suits += f"""{col} не должен быть равен null при условии {filter_missing}.\n"""

                    if 'invalid_percent_min_max' in check:
                        min_value = checks['invalid_percent_min_max'].get('minimum', False)
                        max_value = checks['invalid_percent_min_max'].get('maximum', False)
                        if min_value is not False or max_value is not False:
                            yaml_suits += f"""
  - invalid_percent({col})=0:"""

                            if min_value is not False and max_value is not False:
                                yaml_suits += f"""
      valid min: {min_value}
      valid max: {max_value}
         name: """
                                if business_desc is not None and business_desc!='':
                                    yaml_suits += f'Значение {business_desc} не должно быть меньше {min_value} и больше {max_value}.\n'
                                yaml_suits+=f"""Значение {col} не должно быть меньше {min_value} и больше {max_value}\n"""

                            elif max_value is False:
                                yaml_suits += f"""
      valid min: {min_value}
         name: """
                                if business_desc is not None and business_desc!='':
                                    yaml_suits += f'Значение {business_desc} не должно быть меньше {min_value}.\n'
                                yaml_suits+=f"""Значение {col} не должно быть меньше {min_value}\n"""

                            elif min_value is False:
                                yaml_suits += f"""
      valid max: {max_value}
         name: """
                                if business_desc is not None and business_desc != '':
                                    yaml_suits += f'Значение {business_desc} не должно быть больше {max_value}.\n'
                                yaml_suits += f"""Значение {col} не должно быть больше {max_value}\n"""



                    if 'invalid_percent_valid_values' in check:
                        valid_values = checks['invalid_percent_valid_values']
                        if valid_values is not None:
                            yaml_suits += f"""
  invalid_percent({col}):
      valid values: {valid_values}
         name: """
                            if business_desc is not None and business_desc != '':
                                yaml_suits += f'{business_desc}'
                            yaml_suits += f'{col} может принимать значения {valid_values}.\n'

                    if 'invalid_percent_valid_regex' in check:
                        valid_regex = checks['invalid_percent_valid_regex']
                        if valid_regex is not None:
                            yaml_suits += f"""
  - invalid_percent({col})=0: 
      valid regex: {valid_regex}
         name: """
                            if business_desc is not None and business_desc!='':
                                yaml_suits+=f' {business_desc} должно соответствовать форме.\n'
                            yaml_suits+=f'{col} соответствует форме {valid_regex}\n'

                    if 'invalid_percent_invalid_values' in check:
                        invalid_values = checks['invalid_percent_invalid_values']
                        if invalid_values is not None:
                            yaml_suits +=f"""
  - invalid_percent({col})=0: 
      invalid values: ['']
         name: """
                            if business_desc is not None and business_desc!='':
                                yaml_suits+=f'{business_desc} не может быть пустым.\n'
                            yaml_suits+=f'{col} не может принимать значение '' (пустая строка)\n'


        return yaml_suits


    def generate_suite(self):
        with open(f'{self.helper.table}_suite.yml', "w", encoding='utf-8') as log_file:
            log_file.write(str(self.get_suite()) + '\n')
            print(f'File {self.helper.table}_suite.yml saved!')


    def save_profiling(self):
        self.profiler.to_pandas().to_csv(f'{self.helper.table}_report.csv')

        print(f'{self.helper.table}_report saved!')
