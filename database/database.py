#!/usr/bin/python3 
import pandas as pd
from domain.scheme import init_schema
from database.functions import fill_table_wrapper,tag,song,artist,album


def insert():
    init_schema()
    # df = pd.read_csv('./spotify/csv/tags.csv',sep=';',error_bad_lines=False)
    # fill_table_wrapper(df,tag)
