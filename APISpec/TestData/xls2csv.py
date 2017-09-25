#!/c/Python27/python

import pandas as pd
import argparse
import os

import argparse

parser = argparse.ArgumentParser(description='Export CSV files from an Excel File.')
parser.add_argument('inputfile', metavar='inputfile', type=str,
                    help='The Excel file containing CSV tabs to be exported')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')

args = parser.parse_args()

prefix = os.path.dirname(args.inputfile)
data_xls = pd.ExcelFile(args.inputfile)
print data_xls.sheet_names
print len(data_xls.sheet_names)
for tab in data_xls.sheet_names:
  if ".csv" in tab:
    # Get the names of the columns
    column_list = []
    df_column = pd.read_excel(data_xls, tab).columns
    for i in df_column:
        column_list.append(i)
    # Create a converter for each to be string
    converter = {col: str for col in column_list}
    tab_xls =  pd.read_excel(data_xls, tab, index_col=None, converters=converter)
    if len(prefix) > 0:
      prefix = prefix + "/"
    tab_xls.to_csv(prefix + tab, encoding='utf-8', index=False)
