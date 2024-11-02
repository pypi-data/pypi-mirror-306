from automatic_contract_creation.scr.profilers.profiler import Profiler
import polars as pl
import polars.selectors as cs


class ContractVariable(Profiler):
    def __init__(self, connection_name: str, **creds):
        super().__init__(connection_name, **creds)


    def get_data(self, query, parameters=None):
        lf = self.connector.read_data(query, parameters)
        lf = lf.cast({pl.Decimal: pl.Float64})
        profiling_data = self.compute_metrics(lf)
        dtypes = self.connector.origin_dtypes

        return lf, profiling_data, dtypes


    def get_checks_config(self, query, parameters=None):
        lf, profiling_data, dtypes = self.get_data(query, parameters)
        unique_columns = profiling_data.filter(pl.col('percent_dup') == 0)['column'].to_list()
        not_null_columns = profiling_data.filter(pl.col('null_count') == 0)['column'].to_list()
        regex_columns = self.define_regex_columns(query, self.connector)

        min_max_columns = profiling_data.filter(pl.col('minimum').is_not_null() |
                                                 pl.col('maximum').is_not_null())['column'].to_list()

        min_max_columns = [x for x in min_max_columns if x not in lf.select(cs.temporal()).columns]

        invalid_count_dict = {}
        for col in min_max_columns:
            min_value = profiling_data.filter(pl.col('column') == col)['minimum'].to_list()[0]
            max_value = profiling_data.filter(pl.col('column') == col)['maximum'].to_list()[0]
            invalid_count_dict[col] = {'valid_min': min_value, 'valid_max': max_value}


        for col, reg in regex_columns.items():
            if col in invalid_count_dict:
                invalid_count_dict[col]['valid_regex'] = reg
            else:
                invalid_count_dict[col] = {'valid_regex':reg}


        categorical_columns = profiling_data.filter(pl.col('cat_dist').is_not_null())['column'].to_list() if 'cat_dist' in profiling_data.columns else None
        for col in categorical_columns:
            values = pl.Series(lf.select(pl.col(col).unique()).drop_nulls().collect()).drop_nans().to_list()
            if col in invalid_count_dict:
                invalid_count_dict[col]['valid_values'] = values
            else:
                invalid_count_dict[col] = {'valid_values': values}



        contracts_checks = {'duplicate_count': {'columns':unique_columns},
                            'missing_count': {'columns': not_null_columns},
                            'invalid_count': {'columns': set(
                                min_max_columns+list(regex_columns.keys())+categorical_columns
                            ),
                                                      'valid_format_dict': invalid_count_dict}

                            }
        set_columns_checks = set(categorical_columns+unique_columns+not_null_columns+min_max_columns+list(regex_columns.keys()))

        return contracts_checks, dtypes, set_columns_checks

