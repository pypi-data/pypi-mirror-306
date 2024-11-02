from automatic_contract_creation.scr.connectors.connection_manager import ConnectionManager
from automatic_contract_creation.scr.connectors.connectors import Connector
import polars as pl
import polars.selectors as cs
import re
from typing import Optional, Dict


class Profiler(ConnectionManager):
    def define_categorical(self, lf: pl.LazyFrame)->list:
        """

        Test for categorical columns.
        https://jeffreymorgan.io/articles/identifying-categorical-data/
        The algorithm provides a useful test for identifying categorical data:

        Calculate the number of unique values in the data set.
        Calculate the difference between the number of unique values in the data set and the total number of values in the data set.
        Calculate the difference as a percentage of the total number of values in the data set.
        If the percentage difference is 95% or more, then the data set is composed of categorical values.

        """
        len_df= lf.select(pl.len()).collect().row(0)[0]
        cat_columns = pl.Series(
            lf.select(
                cs.by_dtype(pl.String, cs.INTEGER_DTYPES).unique().count()
            ).select(
                pl.all().map_elements(
                    lambda x: (len_df- x) / len_df, return_dtype=float)
        ).melt().filter(
                pl.col('value') > 0.9
            ).select('variable').collect()
        ).to_list()

        return cat_columns


    def compute_metrics(self, lazyframe: pl.LazyFrame, dt: str=None)->pl.DataFrame:
        """
        Colculate metrics ant return report profiling that consist:
        - 'columns' - is the name of the column.
        The first value is always 'all', which means that the metric is applied to the entire dataset.
        - 'rows' - the number of rows.
        - 'percent_dup' - percentage of duplicates
        - 'quantile_05_morning' - percentile of 5% of the number of rows per hour from 9:00:00 am to 23:59:59.
        - 'quantile_95_morning' - percentile of 95% of the number of rows per hour from 9:00:00 am to 23:59:59.
        - 'quantile_05_night' - percentile of 5% of the number of rows per hour from 00:00:00 am to 8:59:59.
        - 'quantile_95_night' - the percentile, which is 95% of the number of rows per hour from 00:00:00 am to 8:59:59.
        - 'null_percent' - the percentage is equal to Null values.
        - 'percent_zeros' - percentage 0 (for numeric units whose type is numeric or string, but inside which there is a number).
        - 'percent_empty_strings' - is the percentage of empty strings. " If there are spaces in the line, they will not be taken into account.
        - 'percent_strings_with_spaces' - percentage with spaces only ' '.
        - 'minimum' - the minimum for numbers and dates (which have a numeric or string type, but are inside a number or date).
        - 'maximum' - maximum for numbers and dates (which have a numeric or string type, but are inside a number or date)
        - 'cat_dist' - percentage of distribution (for categorical values less than 20). It has the structure: ['distribution name':
        percentage]
        """
        lf = lazyframe.cast({pl.Decimal: pl.Float64, pl.Object: pl.Utf8})
        if dt:
            try: lf = lf.cast({dt: pl.Datetime})
            except: lf = lf.with_columns([
            pl.col(dt).str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S", strict=False)
        ])

        categorical_columns = lf.select(cs.categorical()).columns
        if len(categorical_columns) == 0: categorical_columns.extend(self.define_categorical(lf))
        numeric_columns = lf.select(cs.numeric()).columns
        temporal_columns = lf.select(cs.temporal()).columns
        string_columns = lf.select(cs.string()).columns
        bool_columns = lf.select(cs.boolean()).columns
        others = lf.select(~cs.by_name(numeric_columns,
                                            temporal_columns,
                                            categorical_columns,
                                            string_columns,
                                            bool_columns)).columns
        datetime_columns = lf.select(cs.datetime()).columns
        dt =dt or (datetime_columns[0] if datetime_columns else None)


        df_info = lf.select(
                    column = pl.lit('all'),
                    rows = pl.len(),
                    percent_dup =(
                            (pl.len() - lf.unique().with_row_index(offset=1).last().select(
                                pl.col('index')
                            ).collect())
                            /pl.len()
                    )
                ).collect()

        if dt is not None:
            df_info.hstack(
                pl.concat([
                    lf.filter(
                    pl.col(dt).dt.hour().is_between(9, 23)
                ).group_by(
                    pl.col(dt).dt.hour()
                ).agg(
                    pl.len()
                ).select(
                    quantile_05_morning=pl.col('len').quantile(0.05),
                    quantile_95_morning=pl.col('len').quantile(0.95)
                ),
                lf.filter(
                    ~pl.col(dt).dt.hour().is_between(9, 23)
                ).group_by(
                    pl.col(dt).dt.hour()
                ).agg(
                    pl.len()
                ).select(
                    quantile_05_night=pl.col('len').quantile(0.05),
                    quantile_95_night=pl.col('len').quantile(0.95)
            )], how='horizontal').collect(), in_place=True)

        else:
            df_info = pl.concat([
                df_info,
                pl.DataFrame({
                    'quantile_05_morning': [None],
                    'quantile_95_morning': [None],
                    'quantile_05_night': [None],
                    'quantile_95_night': [None]
                })
            ], how='diagonal_relaxed')

        total_rows = df_info.select(pl.col('rows'))[0, 0]

        df_describe = pl.concat([
            lf.null_count().melt(variable_name='column',
                   value_name='null_percent'),

            lf.select(
                pl.all().n_unique()
            ).melt(variable_name='column',
                   value_name='percent_dup'),

            lf.select(pl.all().map_elements(
                lambda s: (s == 0) | (s == "0") | (s == "0.0")
                , return_dtype=bool).sum()
                      ).melt(variable_name='column',
                             value_name='percent_zeros'),

            lf.select(pl.all().map_elements(
                lambda s: s == "", return_dtype=bool).sum()
                      ).melt(variable_name='column',
                             value_name='percent_empty_strings'),

            lf.select(
                pl.exclude(categorical_columns).str.contains(r'^\s+$')
            ).sum().melt(
                variable_name='column',
                value_name='percent_strings_with_spaces'
            )
        ], how='align').with_columns(
            pl.exclude('column').map_elements(
                lambda x: round(x/ total_rows, 3),
                return_dtype=float
            )).collect()

        if numeric_columns + temporal_columns:
            df_describe.join(
                pl.concat([
                    lf.select(
                        pl.col(numeric_columns + temporal_columns).min()
                    ).cast(
                        {cs.numeric(): pl.String, cs.temporal(): pl.String}
                    ).melt(variable_name='column',
                           value_name='minimum'),

                    lf.select(
                        pl.col(numeric_columns + temporal_columns).max()
                    ).cast(
                        {cs.numeric(): pl.String, cs.temporal(): pl.String}
                    ).melt(variable_name='column',
                           value_name='maximum')
                ], how='align').collect(),
                on='column'
            ).with_columns(
                pl.exclude(['column', 'minimum', 'maximum']
                           ).map_elements(
                    lambda x: round(x/ total_rows, 3),
                    return_dtype=float
                )
            )

        if dt:
            df_describe= pl.concat([df_describe,
                pl.concat([
                    lf.filter(
                        pl.col(dt).dt.hour().is_between(9, 23)
                    ).group_by(
                        pl.col(dt).dt.hour()
                    ).agg(
                        pl.all().drop_nulls().drop_nans().len()
                    ).quantile(0.05).melt(variable_name='column',
                                          value_name='quantile_05_morning'),

                    lf.filter(
                        pl.col(dt).dt.hour().is_between(9, 23)
                    ).group_by(
                        pl.col(dt).dt.hour()
                    ).agg(
                        pl.all().drop_nulls().drop_nans().len()
                    ).quantile(0.95).melt(variable_name='column',
                                          value_name='quantile_95_morning'),

                    lf.filter(
                        ~pl.col(dt).dt.hour().is_between(9, 23)
                    ).group_by(
                        pl.col(dt).dt.hour()
                    ).agg(
                        pl.all().drop_nulls().drop_nans().len()
                    ).quantile(0.05).melt(variable_name='column',
                                          value_name='quantile_05_night'),

                    lf.filter(
                        ~pl.col(dt).dt.hour().is_between(9, 23)
                    ).group_by(
                        pl.col(dt).dt.hour()
                    ).agg(
                        pl.all().drop_nulls().drop_nans().len()
                    ).quantile(0.95).melt(variable_name='column',
                                          value_name='quantile_95_night')
                ], how='align').collect()
                                    ],how='align')

        distribution_percentage = pl.DataFrame({'cat_dist':[None]})

        if len(categorical_columns) > 0:
            for clm in lf.select(
                    pl.col(categorical_columns).unique().count()
            ).melt().filter(
                pl.col('value') < 20
            ).collect()['variable']:
                count_perc = (
                    lf.select(
                        pl.col(clm).drop_nulls().drop_nans().value_counts(sort=True)
                    )
                    .unnest(clm)
                    .with_columns(
                        column=pl.lit(clm),
                        cat_dist=pl.col(clm),
                        percent_of_total=(pl.col('count') / total_rows).round(3)

                ).collect()
                )

                combined_list = [
                    f"{row['cat_dist']}: {row['percent_of_total']}"
                    for row in count_perc.to_dicts()
                ]


                distribution_percentage = pl.concat([
                    distribution_percentage,
                    pl.DataFrame({'column': clm, 'cat_dist': [combined_list]})
                ], how='diagonal_relaxed')

        how_concat = 'align' if distribution_percentage.height > 1 else 'diagonal_relaxed'
        final_df = pl.concat(
            [pl.concat(
                [
                    df_info,
                    df_describe
                ], how='diagonal_relaxed'),
                distribution_percentage
            ], how=how_concat)


        return final_df.filter(~pl.all_horizontal(pl.all().is_null()))

    def save_to_csv(self, lazyframe: pl.LazyFrame, dt: str=None):
        dt = dt if dt else None
        self.compute_metrics(lazyframe, dt).with_columns(
            pl.col('cat_dist').map_elements(
                lambda col: str(col.to_list()), return_dtype=pl.String)
        ).write_csv('report.csv')

        print(f'Report saved!')

    def define_regex_columns(self, query:str, connector: Connector)-> Optional[Dict[str, str]]:
        """
        This function runs through all columns except dates, and if 60% of the filled values
        satisfy a regular mask, then the column contains a regular expression.
        Return the dictionary {<column_name>: <regex_mask>}>
        """
        regexes = {
            'email_regex': r'^[\w\.-]+@[\w\.-]+\.\w+$',
            'card_regex': r'^(2200|2204)|^5[1-5]\d{2}\d{12}$|^4\d{15}$|^3[47]\d{13}$|^6\d{15,17}$|^6\d{15}$|^9860\d{12}$|^(8600|5614)\d{12}$|^94\d{14}$|^30[0-5]\d{11}$|^36\d{12}$|^38\d{12}$|^39\d{12}$',
            'uuid': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
            'phone_number': r'^(?:\+?(?:7|8|996|995|994|998|374|375|972))\d{9,10}$',
            'ip_address': r'([0-9]{1,3}[\.]){3}[0-9]{1,3}',
            'web_site': r'^(https?://)?(www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,63}([/\?#][a-zA-Z0-9-_=#%&.+]+)*$',
            'date': r'^(19\d{2}|20\d{2})$|^(19\d{2}|20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$|^(19\d{2}|20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\s([01]\d|2[0-3]):([0-5]\d):([0-5]\d)(\.\d{2,3})?$|^(19\d{2}|20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\s([01]\d|2[0-3]):([0-5]\d):([0-5]\d)(\.\d{2,3})?\s\+([01]\d|2[0-3]):([0-5]\d)$|^(19\d{2}|20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])T([01]\d|2[0-3]):([0-5]\d):([0-5]\d)(\.\d{2,3})?$',
            'int': r'^-?\d+$',
            'float': r'\s*-?\d+[,.]\d+\s*$'
        }

        priority = [
            'email_regex', 'uuid', 'card_regex', 'phone_number',
            'ip_address', 'web_site', 'int', 'float'
        ]

        lf = connector.read_data(query)
        result = {}

        for column in lf.select(~cs.temporal()).columns:
            col_full_rows = \
                lf.select(pl.col(column).drop_nans()).drop_nulls(subset=column).select(pl.len()).collect().row(0)[0]
            for regex_name in priority:
                regex = regexes[regex_name]
                matching_rows = lf.select(pl.col(column).map_elements(
                    lambda x: len(re.findall(regex, str(x))),
                    return_dtype=pl.Int64,
                    skip_nulls=True
                )).sum().collect().row(0)[0]
                if matching_rows != 0 and (matching_rows * 100) / col_full_rows >= 60:
                    result[column] = regex
                    break

        return result if result else None
