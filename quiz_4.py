# Uses data available at http://data.worldbank.org/indicator
# on Forest area (sq. km) and Agricultural land area (sq. km).
# Prompts the user for two distinct years between 1990 and 2014
# as well as for a strictly positive integer N,
# and outputs the top N countries where:
# - agricultural land area has increased from oldest input year to most recent input year;
# - forest area has increased from oldest input year to most recent input year;
# - the ratio of increase in agricultural land area to increase in forest area determines
#   output order.
# Countries are output from those whose ratio is largest to those whose ratio is smallest.
# In the unlikely case where many countries share the same ratio, countries are output in
# lexicographic order.
# In case fewer than N countries are found, only that number of countries is output.


# Written by Daniel Yang and Eric Martin for COMP9021


import sys
import os
import csv

agricultural_land_filename = 'API_AG.LND.AGRI.K2_DS2_en_csv_v2.csv'
if not os.path.exists(agricultural_land_filename):
    print(f'No file named {agricultural_land_filename} in working directory, giving up...')
    sys.exit()
forest_filename = 'API_AG.LND.FRST.K2_DS2_en_csv_v2.csv'
if not os.path.exists(forest_filename):
    print(f'No file named {forest_filename} in working directory, giving up...')
    sys.exit()
try:
    years = {int(year) for year in input('Input two distinct years in the range 1990 -- 2014: ').split('--')}
    if len(years) != 2 or any(year < 1990 or year > 2014 for year in years):
        raise ValueError
except ValueError:
    print('Not a valid range of years, giving up...')
    sys.exit()
try:
    top_n = int(input('Input a strictly positive integer: '))
    if top_n < 0:
        raise ValueError
except ValueError:
    print('Not a valid number, giving up...')
    sys.exit()

countries = []
year_1, year_2 = min(years), max(years)

with open(agricultural_land_filename, newline = "", encoding = "utf-8") as agriFile, open(forest_filename, newline = "", encoding = "utf-8") as forestFile:
    agriList = [row for row in csv.reader(agriFile)][5:]
    forestList = [row for row in csv.reader(forestFile)][5:]
    
agriLand = {row[0]: float(row[34+year_2-1990])-float(row[34+year_1-1990]) for row in agriList if "" not in [row[0],row[34+year_1-1990],row[34+year_2-1990]] and float(row[34+year_2-1990]) > float(row[34+year_1-1990])}
forest = {row[0]: float(row[34+year_2-1990])-float(row[34+year_1-1990]) for row in forestList if "" not in [row[0],row[34+year_1-1990],row[34+year_2-1990]] and float(row[34+year_2-1990]) > float(row[34+year_1-1990])}
ratio = sorted([(agriLand[country]/forest[country], country) for country in agriLand if country in forest], reverse = True)

countries = [f"{e[1]} ({e[0]:.2f})" for e in ratio][:top_n]

print(f'Here are the top {top_n} countries or categories where, between {year_1} and {year_2},\n'
      '  agricultural land and forest land areas have both strictly increased,\n'
      '  listed from the countries where the ratio of agricultural land area increase\n'
      '  to forest area increase is largest, to those where that ratio is smallest:')
print('\n'.join(country for country in countries))
    
