import random

from automatic_contract_creation.scr.utils.data_context_provider import DataContextProvider
from automatic_contract_creation.scr.profilers.profiler import Profiler
from typing import Dict, Any, List, Optional

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import re

import polars as pl
import numpy as np


class ProfilerHelperTrino(DataContextProvider,Profiler):
    def __init__(self, context: str):
        super().__init__(context)
        self.business_dt = self.define_business_date()
        self.orig_type = self.get_orig_type()
        self.group_dict = self.get_granularity()
        self.queries = self.make_query_for_profiler()


    def define_business_date(self)->str:

        """
        This function determines the date on which the partitioning takes place
        If the partitioning goes by the fields year, month, day, then 3 partitioning fields will be defined
        If the table doesn't have a partition, then the priority of the business date will be determined, if there
        is none, then the first datetime will be determined
        """

        show_create_table_query = f'show create table {self.creds["catalog"]}.{self.creds["schema"]}.{self.table}'

        show_create_table = self.con.read_pandas_df(show_create_table_query)
        partition = re.search(r"partitioning = ARRAY\['(.*?)'\]|partitioned_by = ARRAY\[(.*?)\]",
                                     show_create_table.iloc[0, 0])

        if partition and partition.group(1):
            business_dt = partition.group(1)
        elif partition and partition.group(2):
            business_dt = partition.group(2)
        elif not self.dtypes[
           ( self.dtypes['data_type']=='date')
           &
           (~self.dtypes['column_name'].str.contains('load_date', case=False, na=False))
                   ].empty:
            business_dt = self.dtypes[
                (self.dtypes['data_type'] == 'date')
            &
                (~self.dtypes['column_name'].str.contains('load_date', case=False, na=False)
                 )].iloc[0, 0]
        elif not self.dtypes[
            (self.dtypes['data_type'].isin(['timestamp(6) with time zone',
                                            'timestamp',
                                            'timestamp(6)',
                                            'time with time zone',
                                            'time'])
                    )].empty:
            business_dt = self.dtypes[
                self.dtypes['data_type'].isin(['timestamp(6) with time zone',
                                            'timestamp',
                                            'timestamp(6)',
                                            'time with time zone',
                                            'time'])].iloc[0, 0]
        elif not self.dtypes[
            (self.dtypes['data_type']=='varchar')
            &
            (self.dtypes['column_name'].str.contains('timestamp|dt|date', case=False, na=False))
        ].empty:
            business_dt = self.dtypes[
            (self.dtypes['data_type']=='varchar')
            &
            (self.dtypes['column_name'].str.contains('timestamp|dt|date', case=False, na=False))
        ].iloc[0, 0]

        else:
            business_dt = None

        print(business_dt)

        return business_dt

    def get_orig_type(self)-> str:
        """
        Get the date data type of business_dt
        """
        return self.dtypes[
            self.dtypes['column_name']==self.business_dt.replace('day(', '').replace(')', '').replace('month(', '')
            ]['data_type'].values[0] if (
                self.business_dt !=  "'year','month','day','hour'"
        ) and self.business_dt != None else 'varchar'


    def get_group_dt(self)-> dict:

        """
        Classify group of business date.
        Group 1 - the partition goes by 'date'
        Group 2 - the partition goes by 'varchar'
        Group 3 - the partition goes by 'timestamp'
        Group 4 - doesn't have partition and doesn't have columns that access to 'timestamp' or 'date'

        This dictionary also contains the converted date to shorten the code further (key -query_dt)
        """
        group_dict = {'query_dt':[], 'num_group':[]}
        if self.orig_type == 'date' or 'day(' in self.business_dt or 'month(' in self.business_dt:
            group_dict['query_dt']= f"""{self.business_dt.replace('day', 'date').replace('month', 'date')}"""
            group_dict['num_group']= 1
        elif self.orig_type=='varchar' and self.business_dt=="'year','month','day','hour'":
            group_dict['query_dt']= self.business_dt
            group_dict['num_group']= 2
        elif 'timestamp' in self.orig_type:
            group_dict['query_dt']= f"date({self.business_dt})"
            group_dict['num_group']= 3
        else:
            group_dict['query_dt']= 'unknown'
            group_dict['num_group']= 4

        print(group_dict)
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

    def get_dates_from_period(self, start_dt: date, end_dt: date) -> List[date]:
        """Generates a list of dates from start_dt to end_dt inclusive."""
        delta = end_dt - start_dt
        return [start_dt + timedelta(days=i) for i in range(delta.days + 1)]


    def get_granularity(self)-> Dict[str, Any]:
        """
        The function determines the granularity of new sources.
        To determine a new source, we take the interval
        yesterday + 3 months ago and yesterday + 4 months ago
        and count the unique days in this period, if there are at least 20 unique days,
        the source is old, otherwise new

        Granularity 1 - old source that have statistics more than 3 months
        Granularity 2 - new source that have statistics less than 3 months

        For new sources save date diff for getting random days in main query profiling:
        - for date/timestamp business date in diff difference between max date and min date
        - for varchar business date in diff unique dates for random choice
        """
        groups = self.get_group_dt()
        dates = self.generate_dates(count=4)
        counter = 0
        if groups['num_group']==1:
            min_dt = self.con.read_pandas_df(f"""
            select  distinct {groups['query_dt']}
            from {self.creds["catalog"]}.{self.creds["schema"]}.{self.table}
            where {groups['query_dt']}>=date('{dates['dt_3_months_ago']}')
            and {groups['query_dt']}<=date('{dates['dt_2_months_ago']}')
            limit 20""")

            counter+=len(min_dt)
        elif groups['num_group']==2:
            min_dt = self.con.read_pandas_df(f"""
                        select distinct day
                        from {self.creds["catalog"]}.{self.creds["schema"]}.{self.table}
                        where year='{dates['dt_3_months_ago'].year}'
                        and month='{dates['dt_3_months_ago'].month:02d}'
                        limit 20""")
            counter+=len(min_dt)
        elif groups['num_group']==3:
            min_dt =  self.con.read_pandas_df(f"""
            select count(*)
            from
                 {self.creds["catalog"]}.{self.creds["schema"]}.{self.table}
                  where {groups['query_dt']} >=timestamp '{dates['dt_3_months_ago']}'
                  and {groups['query_dt']} <= timestamp'{dates['dt_2_months_ago']}'
                  limit 20
            """)
            counter+=len(min_dt)
        else:
            counter+=0

        if counter>=20:
            groups['granularity']=1
        else:
            if groups['num_group']==1 or groups['num_group']==3:
                groups['granularity'] = 2
                deep_table =  self.con.read_pandas_df(f"""
                 select max({groups['query_dt']}) - min({groups['query_dt']})  as diff
                 from
                 {self.creds["catalog"]}.{self.creds["schema"]}.{self.table}"""
                )
                groups['deep_table'] = deep_table['diff'].dt.days.values


            elif groups['num_group']==2:
                groups['granularity'] = 2
                groups['deep_table'] =  self.con.read_pandas_df(f"""
                select distinct year||month||day as dt_key
                FROM logstream_hive.raw.events_v2_wba_v0_0
                where year||month||day !='{date.today().strftime('%Y%m%d')}'
                limit 6
                """)['dt_key'].to_list()

        return groups




    def get_row_counts(self)->int:
        """
        This function helps to determine the amount of sampling.
        The principle of operation:
        - for  granularity 1
            * calculates the number of rows in 3 days (yesterday / yesterday + a month ago / yesterday + two months ago),
            the maximum is taken relative to which the sampling volume will be calculated

        - for  granularity 2
            * maximum is taken from 3 dates throught limit

        none partition tables will missed

        The function adds a large table flag to the dictionary. A large table is considered a table with
        more than 1 000 000 000 rows per day
        """
        dates = self.generate_dates(count=3)
        dt_yesterday = dates['dt_yesterday']
        dt_month_ago = dates['dt_1_months_ago']
        dt_two_months_ago = dates['dt_2_months_ago']

        counter = []
        i=0
        for dt in (dt_yesterday, dt_month_ago, dt_two_months_ago):
            if self.group_dict['num_group']==1 and self.group_dict['granularity']==1:
                query = f"""
                select
                count(*) as cnt
                from
                {self.creds["catalog"]}.{self.creds["schema"]}.{self.table}
                where
                {self.group_dict['query_dt']}=date('{dt}')
                """

            elif self.group_dict['num_group']==2 and self.group_dict['granularity']==1:
                query = f"""
                select
                count(*) as cnt
                from
                {self.creds["catalog"]}.{self.creds["schema"]}.{self.table}
                where
                year ='{dt.year}'
                and
                month ='{dt.month:02d}'
                and
                day ='{dt.day:02d}'
                """

            elif self.group_dict['num_group']==3 and self.group_dict['granularity']==1:
                query = f"""
                 select
                 count(*) as cnt
                 from
                 {self.creds["catalog"]}.{self.creds["schema"]}.{self.table}
                 where
                 date({self.group_dict["query_dt"]}) = date('{dt}')
                            """

            elif self.group_dict['granularity']==2 and (self.group_dict['num_group']==1
                or self.group_dict['num_group']==3):
                random_day =random.randint(0, self.group_dict['deep_table'])
                query =f"""
                with get_rand as(
                select max({self.group_dict['query_dt']}) - INTERVAL {random_day} day as random_day
                from  {self.creds["catalog"]}.{self.creds["schema"]}.{self.table}
                )
                select 
                count(*) as cnt
                from  {self.creds["catalog"]}.{self.creds["schema"]}.{self.table}
                where {self.group_dict['query_dt']} = (select random_day from get_rand)
                """


            elif self.group_dict['granularity']==2 and self.group_dict['num_group']==2:
                query = f"""
                select count(*) as cnt
                from  {self.creds["catalog"]}.{self.creds["schema"]}.{self.table}
                where year='{self.group_dict['deep_table'][i][:4]}'
                and month='{self.group_dict['deep_table'][i][4:6]}'
                and day='{self.group_dict['deep_table'][i][6:8]}'
                """
                i+=1

            counter.append(self.con.read_data(query).select(pl.col('cnt')).collect()[0, 0])
        else:
            counter.append(0)

        self.group_dict['large_table_flg'] = 1 if max(counter)>1000000000 else 0

        return max(counter)

    def determine_bernoulli_threshold(self, threshold:int=500000)->float:
        """
        The function will calculate which sample we need to take in a guery for
        random upload for a month

        For too large tables the sample is calculated relative to the day
        For new sources group_dict['granularity']==2 the sample is calculated relative to the day

        For none partition and none temporal columns returns 0
        """
        max_len = self.get_row_counts()
        if max_len > 0 and max_len < 1000000000 and self.group_dict['granularity'] == 1:
            sample_percent = (threshold*10)/(max_len*3)
        elif self.group_dict['num_group']==4:
            sample_percent=0
        elif max_len>1000000000 or self.group_dict['granularity']==2:
            sample_percent = threshold/max_len
        else:
            sample_percent = 0

        return sample_percent


    def get_cols_for_query(self) -> list:
        """
        The function defines columns as an unparsed for exclusion from profiling and generation of checks.
        Unparsed columns has data type: array, map, row
        """
        exlude_col = self.dtypes[self.dtypes['data_type'].str.startswith(('array', 'row', 'map'))]['column_name'].to_list()
        include_col = self.dtypes[~self.dtypes['column_name'].isin(exlude_col)]['column_name'].to_list()

        return include_col


    def make_query_for_profiler(self)->List[str]:
        """
        Creates basic queries for the received tablesample for 3 periods on the basis of which profiling
        will be considered

        For granularity 1 and groups that have partition and not large tables:
        making query for 3 periods (yesterday + a month ago / yesterday + two months ago / yesterday + three months ago)
        For granularity 1 and large tables: making query for 3 random days
        For granularity 2: making query 3 dates (yesterday/two months ago/three months ago)
        For none partition tables: making query throw limit+offset
        """
        sample_percent = self.determine_bernoulli_threshold()
        dates = self.generate_dates(count=4)
        days = self.get_dates_from_period(start_dt=dates['dt_3_months_ago'],
                                          end_dt=dates['dt_yesterday'])

        include_cols = self.get_cols_for_query()

        queries = []
        for i in range(len(dates) - 1):
            next_month = f'dt_{i}_months_ago' if i!= 0 else 'dt_yesterday'
            previos_month = f'dt_{i + 1}_months_ago'
            offset = 0

            if (self.group_dict['num_group']==1
                    and self.group_dict['granularity']==1
                    and self.group_dict['large_table_flg']==0):
                query = f'''
                with cte as (
                select {', '.join(include_cols)}
                from {self.creds["catalog"]}.{self.creds["schema"]}.{self.table}
                where
                {self.group_dict["query_dt"]}  >= date('{dates[previos_month]}') 
                and {self.group_dict["query_dt"]} <=date('{dates[next_month]}')
                 )
                 select * from cte
                TABLESAMPLE BERNOULLI({sample_percent})
                '''


            elif (self.group_dict['num_group']==2
                  and self.group_dict['granularity']==1
                  and self.group_dict['large_table_flg']==0):
                query = f'''
                    with cte as (
                    select  {', '.join(include_cols)}
                    from {self.creds["catalog"]}.{self.creds["schema"]}.{self.table}
                    where
                    year in ('{dates[next_month].year}', '{dates[previos_month].year}')
                    and
                    month in ('{dates[next_month].month:02d}', '{dates[previos_month].month:02d}')
                    and
                    day ='{dates[next_month].month:02d}'
                     )
                     select * from cte
                    TABLESAMPLE BERNOULLI({sample_percent})
                    '''

            elif (self.group_dict['num_group']==3
                   and self.group_dict['granularity']==1
                   and self.group_dict['large_table_flg']==0):
                query = f'''
                with cte as (
                select
                  {', '.join(include_cols)}
                 from
                 {self.creds["catalog"]}.{self.creds["schema"]}.{self.table}
                 where
                 date({self.business_dt}) >= date('{dates[previos_month]}') 
                 and date({self.business_dt})<= date('{dates[next_month]}')
                 )
                 select * from cte
                    TABLESAMPLE BERNOULLI({sample_percent})
                '''

            elif ((self.group_dict['num_group']==1  or self.group_dict['num_group']==3)
                  and self.group_dict["granularity"]==2):
                rand_interval = np.random.randint(0, self.groups["deep_table"]+1)
                query=f'''
                with max_date as(
                select max({self.group_dict["query_dt"]}) - interval '{rand_interval}' day as rand_day
                from {self.creds["catalog"]}.{self.creds["schema"]}.{self.table}
                ),
                cte as (
                select  {', '.join(include_cols)}
                from {self.creds["catalog"]}.{self.creds["schema"]}.{self.table}
                where 
                {self.group_dict["query_dt"]} = (select rand_day from max_date) 
                )
                select * from cte
                TABLESAMPLE BERNOULLI({sample_percent})
                '''


            elif self.group_dict['num_group'] == 2\
                    and self.group_dict['granularity']==2:
                random_dt = np.random.choice(self.group_dict['deep_table'])
                query = f'''
                        with cte as(
                        select  {', '.join(include_cols)}
                        from {self.creds["catalog"]}.{self.creds["schema"]}.{self.table}
                        where year= '{random_dt[:4]}'
                        and month='{random_dt[4:6]}'
                        and day='{random_dt[6:8]}'
                        )
                        select * from cte
                        TABLESAMPLE BERNOULLI({sample_percent})
                                '''

            elif ((self.group_dict['num_group']==1 or self.group_dict['num_group']==3)
                  and self.group_dict["granularity"]==1
                  and self.group_dict["large_table_flg"]==1):
                query=f'''
                with cte as (
                select  {', '.join(include_cols)}
                from {self.creds["catalog"]}.{self.creds["schema"]}.{self.table}
                where 
                {self.group_dict["query_dt"]} ={'date(' if self.group_dict['num_group']==1 else 'timestamp'}'{dates[next_month]}'{')' if self.group_dict['num_group']==1 else ''}
                )
                        select * from cte
                        TABLESAMPLE BERNOULLI({sample_percent})
                '''

            elif (self.group_dict['num_group']==2
                and self.group_dict["granularity"]==1
                and self.group_dict["large_table_flg"]==1):
                query=f'''
                with cte as (
                    select  {', '.join(include_cols)}
                    from {self.creds["catalog"]}.{self.creds["schema"]}.{self.table}
                    where
                    year ='{dates[next_month].year}'
                    and
                    month ='{dates[next_month].month:02d}'
                    and
                    day ='{dates[next_month].month:02d}'
                     )
                     select * from cte
                    TABLESAMPLE BERNOULLI({sample_percent})
                '''


            else:
                query = f'''
                select  {', '.join(include_cols)}
                from {self.creds["catalog"]}.{self.creds["schema"]}.{self.table}
                offset {offset}
                limit 500000
                '''
                offset+=500000

            queries.append(query)

        return queries


    def get_profiler(self)-> pl.DataFrame:
        """
        The function receives profiling for three periods in the polaris dataframe format,
        where each metric is represented as an array for periods
        """
        all_profilers = pl.DataFrame()
        for i, query in enumerate(self.queries):
            profiler = self.compute_metrics(self.con.read_data(query))
            if all_profilers.is_empty():
                all_profilers = profiler
                print(f'The profile has completed counting the {i + 1} period!')
            else:
                for col in profiler.columns:
                    if col in all_profilers.columns:
                        if profiler[col].dtype != all_profilers[col].dtype:
                            if profiler[col].dtype==pl.Null:
                                profiler = profiler.cast({col:all_profilers[col].dtype})
                            elif all_profilers[col].dtype==pl.Null:
                                all_profilers = all_profilers.cast({col:profiler[col].dtype})

                all_profilers = pl.concat([all_profilers, profiler])
                print(f'The profile has completed counting the {i + 1} period!')

        return all_profilers.group_by('column').agg(pl.all())

    def get_sample(self)->pl.LazyFrame:
        """
        upload 100 thousand lines for the model to work llm
        """
        include_cols = self.get_cols_for_query()
        print(f'''select {', '.join(include_cols)} from {self.creds["catalog"]}.{self.creds["schema"]}.{self.table} limit 100000''')
        data = self.con.read_data(f'''select {', '.join(include_cols)} from {self.creds["catalog"]}.{self.creds["schema"]}.{self.table} limit 100000''')

        return data

    def get_regex_columns(self)-> Optional[Dict[str, str]]:
        regex_dict = self.define_regex_columns(query= self.queries[0], connector= self.con)

        return regex_dict
