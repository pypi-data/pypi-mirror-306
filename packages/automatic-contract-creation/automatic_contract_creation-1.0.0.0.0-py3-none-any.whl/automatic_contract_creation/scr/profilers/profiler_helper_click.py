import random

from automatic_contract_creation.scr.utils.data_context_provider import DataContextProvider
from automatic_contract_creation.scr.profilers.profiler import Profiler
from typing import Dict, Any, List, Optional

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import re

import polars as pl
import pandas as pd


class ProfilerHelperClick(DataContextProvider,Profiler):
    def __init__(self, context):
        super().__init__(context)
        self.business_dt = self.define_business_date()
        self.group_dict = self.get_granularity()
        self.queries = self.make_query_for_profiler()

    def define_business_date(self) -> str:
        partition_query = f"""select partition_key, primary_key
                        from system.tables
                        where database ='{self.creds['db_name']}'
                        and table='{self.table}'"""

        partition = self.con.read_pandas_df(partition_query)['partition_key'][0]
        match = re.search(r'\(\s*([^()]+?)\s*\)', partition)
        if partition and match.group():
            business_dt = match.group()
        elif not self.dtypes[self.dtypes['data_type'].str.contains('DateTime')].empty:
            business_dt = self.dtypes[self.dtypes['data_type'].str.contains('DateTime')].iloc[0, 0]
        else:
            business_dt = None

        return business_dt

    def get_group_dt(self) -> dict:
        """
        Classify group of business date.
        Group 1 - with business date
        Group 2 - doesn't have business date
        """
        group_dict = {'query_dt': self.business_dt, 'num_group': []}
        if self.business_dt is not None:
            group_dict['num_group']=1
        else:
            group_dict['num_group']=2

        return group_dict


    def generate_dates(self, count: int=3)-> Dict[str, date]:
        """
        The function generates dates by quantity with a delta of minus 1 month, the countdown
        starts from yesterday
        """
        dt_yesterday = date.today() - timedelta(days=1)
        dates = {'dt_yesterday':dt_yesterday}

        for i in range(1, count):
            name = f'dt_{i}_months_ago'
            dates[name] = dt_yesterday - relativedelta(months=i)


        return dates

    def get_granularity(self)-> Dict[str, Any]:
        """
        The function determines the granularity of new sources.
        To determine a new source, we take the interval
        yesterday + 3 months ago and yesterday + 4 months ago
        and count the unique days in this period, if there are at least 20 unique days,
        the source is old, otherwise new

        Granularity 1 - old source that have statistics more than 3 months
        Granularity 2 - new source that have statistics less than 3 months

        For new sources save date diff for getting random days in main query profiling.
        """
        groups = self.get_group_dt()
        dates = self.generate_dates(count=4)
        counter = 0
        if groups['num_group']==1:
            min_dt = self.con.read_pandas_df(f"""
            select  distinct toDate({groups['query_dt']})
            from {self.creds["db_name"]}.{self.table}
            where {groups['query_dt']}>=toDate('{dates['dt_3_months_ago']}')
            and {groups['query_dt']}<=toDate('{dates['dt_2_months_ago']}')
            limit 20""")

            counter+=len(min_dt)
        else:
            counter+=0

        if counter>=20:
            groups['granularity']=1
        elif counter==0 and groups['num_group']==1:
            groups['granularity'] = 2

            deep_table = self.con.read_pandas_df(f"""
                 select max(toDate({groups['query_dt']})) - min(toDate({groups['query_dt']}))  as diff
                 from
                {self.creds["db_name"]}.{self.table}"""
                )
            groups['deep_table'] = deep_table['diff'][0]


        return groups

    def get_cols_for_query(self) -> list:
        """
        The function defines columns as an unparsed for exclusion from profiling and generation of checks.
        Unparsed columns has data type: array, map, row
        """
        exlude_col = self.dtypes[self.dtypes['data_type'].str.startswith(('array', 'row', 'map'))][
            'column_name'].to_list()
        include_col = self.dtypes[~self.dtypes['column_name'].isin(exlude_col)]['column_name'].to_list()

        return include_col

    def make_query_for_profiler(self) -> List[str]:
        """
        Creates basic queries for the received tablesample for 3 periods on the basis of which profiling
        will be considered

        For granularity 1 and groups that have partition and not large tables:
        making query for 3 periods (yesterday + a month ago / yesterday + two months ago / yesterday + three months ago)
        For granularity 1 and large tables: making query for 3 days yesterday/month_ago/two months ago
        For granularity 2: making query random 3 dates
        For none partition tables: making query throw limit+offset
        For empty tables: making query throw limit
        """
        dates = self.generate_dates(count=4)
        include_cols = self.get_cols_for_query()

        queries = []
        for i in range(len(dates) - 1):
            next_month = f'dt_{i}_months_ago' if i != 0 else 'dt_yesterday'
            previos_month = f'dt_{i + 1}_months_ago'
            offset = 0

            if (self.group_dict['num_group']==1
                    and self.group_dict['granularity']==1
                    and self.group_dict['large_table_flg']==0):
                query = f'''
                select {', '.join(include_cols)}
                from {self.creds["db_name"]}.{self.table}
                where
                {self.group_dict["query_dt"]}  >= toDate('{dates[previos_month]}') 
                and {self.group_dict["query_dt"]} <=toDate('{dates[next_month]}')
                order by rand()
                limit 500000
                '''

            elif (self.group_dict['num_group']==1
                    and self.group_dict['granularity']==1
                    and self.group_dict['large_table_flg']==1):
                query = f'''
                select {', '.join(include_cols)}
                from {self.creds["db_name"]}.{self.table}
                where
                toDate({self.group_dict["query_dt"]})= toDate('{dates[next_month]}') 
                order by rand()
                limit 500000
                '''

            elif (self.group_dict['num_group']==1
                  and self.group_dict['granularity']==2
                and not pd.isna(self.group_dict['deep_table'])):
                random_day = random.randint(0, self.group_dict['deep_table'])
                query = f'''
                with get_rand as (
                select toDate(max{self.group_dict['query_dt']} - INTERVAL {random_day} day) as random_day
                from {self.creds["db_name"]}.{self.table}
                )
                select {', '.join(include_cols)}
                from {self.creds["db_name"]}.{self.table}
                where
                toDate{self.group_dict["query_dt"]}= (select random_day from get_rand)
                order by rand()
                limit 500000
                '''

            elif (self.group_dict['num_group']==2):
                query = f'''
                        select  {', '.join(include_cols)}
                        from {self.creds["db_name"]}.{self.table}
                        limit 500000
                        offset {offset}
                        '''
                offset += 500000
            else:
                query=f'''
                select  {', '.join(include_cols)}
                from {self.creds["db_name"]}.{self.table}
                limit 500000
                offset {offset}
                '''

            queries.append(query)

        return queries


    def get_profiler(self)-> pl.DataFrame:
        """
        The function receives profiling for three periods in the polaris dataframe format,
        where each metric is represented as an array for periods
        """
        all_profilers = pl.DataFrame()
        for i, query in enumerate(self.queries):
            data = self.con.read_data(query)
            if not data.collect().is_empty() and data.collect() is not None :
                profiler = self.compute_metrics(data)
                all_profilers = pl.concat([all_profilers, profiler])
            print(f'The profile has completed counting the {i + 1} period!')

        if not all_profilers.is_empty():
            profiler = all_profilers.group_by('column').agg(pl.all())

        else:
            profiler = None

        return profiler

    def get_sample(self)->pl.LazyFrame:
        """
        upload 100 thousand lines for the model to work llm
        """
        include_cols = self.get_cols_for_query()
        data = self.con.read_data(f'''select {', '.join(include_cols)} from {self.creds["db_name"]}.{self.table} limit 100000''')

        return data

    def get_regex_columns(self)-> Optional[Dict[str, str]]:
        regex_dict = self.define_regex_columns(query= self.queries[0], connector= self.con)

        return regex_dict






