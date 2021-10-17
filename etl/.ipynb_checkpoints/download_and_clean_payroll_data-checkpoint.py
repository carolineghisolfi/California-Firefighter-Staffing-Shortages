#!/usr/bin/env python

import pandas as pd
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
from pathlib import Path
from tqdm import tqdm
from time import sleep
from glob import glob
import cpi



def download_and_unzip(data_path):
    """
    Retrieves zipped files from publicpay.ca.gov and downloads to dir in path
    """
    urls = []
    print('Retrieving and downloading data')
    for year in range(2009, 2021):
        for ftype in ['City', 'County', 'SpecialDistrict', 'StateDepartment']:
            urls.append(f'https://publicpay.ca.gov/RawExport/{year}_{ftype}.zip')
    for url in tqdm(urls):
        with urlopen(url) as zipresp:
            with ZipFile(BytesIO(zipresp.read())) as zfile:
                zfile.extractall(data_path)



def load_and_filter_df(file, columns):
    """
    Loads payroll df and filters to only include firefighter positions
    """
    df = pd.read_csv(file, encoding = "ISO-8859-1", \
        low_memory=False, dtype = {'DepartmentOrSubdivision': 'object', 'Year': 'object'}, usecols=columns)
    df.columns = df.columns.str.lower()
    df.position.fillna('', inplace=True)
    df.position = df.position\
        .str.replace('!ST ', '', regex=False)\
        .str.replace('1ST ', '', regex=False)\
        .str.replace('2ND', '', regex=False)\
        .str.replace('.E.', '', regex=False)\
        .str.replace(' - ', '', regex=False)\
        .str.replace(r'\d', '')\
        .str.replace(r'[.!?\\-]', '')\
        .str.upper()
    df = df[df.position.str.contains('FIRE FIGHTER|FIREFIGHTER')]
    return df



def make_dataframe(input_path):
    """
    Concatenates data into master dataframe, filtering column. 
    """
    print('Concatenating and filtering data')
    files = glob(input_path + '/*')
    columns = ['Year','EmployerType', 'EmployerCounty', 'EmployerName','DepartmentOrSubdivision','Position','OvertimePay']
    dfs = []
    for file in tqdm(files):
        df = load_and_filter_df(file, columns)
        dfs.append(df)
    ff_payroll = pd.concat(dfs)
    return ff_payroll



def adjust_overtime(ff_payroll):
    """
    Adjusts prices for inflation. 
    """
    print('Adjusting overtime')
    ff_payroll.year = pd.to_datetime(ff_payroll.year)
    ff_payroll.year = ff_payroll.year.dt.year
    ff_payroll.overtimepay = ff_payroll.overtimepay.astype(float).fillna(0)
    ff_payroll['adjusted_overtime'] = ff_payroll.apply(lambda x: cpi.inflate(x.overtimepay, x.year), axis=1)
    return ff_payroll



def main():
    print('Updating CPI database')
    cpi.update()
    input_path = str(Path(__file__).resolve().parents[1]) + '/data/source'
    output_path = str(Path(__file__).resolve().parents[1]) + '/data/processed'
    download_and_unzip(input_path)
    ff_payroll = make_dataframe(input_path)
    ff_payroll = adjust_overtime(ff_payroll)
    ff_payroll.to_csv(f'{output_path}/ff_payroll.csv')



if __name__ == "__main__":
    main()