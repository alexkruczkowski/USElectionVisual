import pandas as pd
from urllib.request import urlopen
import json
import numpy as np
import os

def read_file(path: str, FIPS_column: str):
    """
    Determines if file extension is valid. 
    Raises TypeError if it is not. 
    Reads file into pd df if valid and converts FIPS column to string.

    Parameters 
    ----------
    path : str
        The path to the file

    Returns
    -------
    pandas dataframe

    Examples
    --------

    """
    filename, file_extension = os.path.splitext(path)
    valid_file_extensions = ['.csv']

    if file_extension in valid_file_extensions:
        if path == 'countypres_2000-2016.csv':
            df = pd.read_csv(path, dtype={FIPS_column: str})
        else:
            df = pd.read_csv(path)
    else:
        error_msg_file_extension = ', '.join(valid_file_extensions)
        raise TypeError(f'Please input either one of the following file formats: {error_msg_file_extension}')

    return(df)


def clean_up(dataframe: str,unique_val: str):
    """
    Dataframe reformatting. 
    Combine rows to be at a county level,
    create columns for each party's total votes, 
    

    Parameters 
    ----------
    dataframe : str
        The name of the pandas dataframe

    unique_val: str
        The name of the column to sum by unique value

    Returns
    -------
    reformatted pandas dataframe

    Examples
    --------

    """
    # create totals columns by party for later aggregation
    uniques = dataframe[unique_val].unique().tolist()
    df = dataframe
    for party_name in uniques:
        if party_name in ['republican', 'democrat', 'libertarian', 'green']:
            name = str(party_name) + '_total'
            df[name] = df.loc[df[unique_val] == party_name,['candidatevotes']].sum(axis=1)
            df[name].fillna(0, inplace=True)
        else:
            df['oth_total'] = df.loc[pd.isna(df[unique_val]),['candidatevotes']].sum(axis=1)
            df['oth_total'].fillna(0, inplace=True)
    
    # groupby totals to aggregate at a county level
    df2 = df.groupby(['year','state','state_po','county','FIPS','office','totalvotes','version'], as_index=False)\
        ['democrat_total','republican_total','green_total','oth_total'].sum()
    # find the proportion of democratic to republican votes for the chloropeth map
    df2['dem_vs_rep']=df2['democrat_total']/(df2['democrat_total']+df2['republican_total'])
    # ensure that the FIPS codes are 5 digits as california, alabama, and several other states were originally being dropped
    df2['fips_code'] = np.where(df2['FIPS'].str.len()<5, '0'+df2['FIPS'], df2['FIPS'])

    return(df2)

def format_table(dataframe_orig: str, dataframe_join: str):
    """
    Dataframe reformatting. 
    for table display
    

    Parameters 
    ----------
    dataframe_orig : str
        The name of the original pandas dataframe

    dataframe_join: str
        The name of the df to join for electoral data

    Returns
    -------
    reformatted pandas dataframe

    Examples
    --------

    """
    df2 = dataframe_orig
    df3 = df2.groupby(['year','state','state_po','office'], as_index=False)['totalvotes','democrat_total','republican_total','green_total','oth_total'].sum()
    df3['dem_vs_tot']=(df3['democrat_total']/(df3['totalvotes']))*100
    df3['rep_vs_tot']=(df3['republican_total']/(df3['totalvotes']))*100
    df3 = df3.merge(dataframe_join[['state_po','Votes']], left_on='state_po', right_on='state_po', how = 'left')
    df3['state_winner'] = np.where(df3['dem_vs_tot'] > df3['rep_vs_tot'], 'Democrat', 'Republican')
    df3['dem_vs_tot']=df3['dem_vs_tot'].map('{:,.2f}%'.format)
    df3['rep_vs_tot']=df3['rep_vs_tot'].map('{:,.2f}%'.format)
    df3['electoral_votes']=df3['Votes']
    df3['dem%']=df3['dem_vs_tot']
    df3['rep%']=df3['rep_vs_tot']
    df_output = df3[['year', 'state', 'state_winner', 'dem%', 'rep%', 'totalvotes','electoral_votes']]

    return(df_output)
