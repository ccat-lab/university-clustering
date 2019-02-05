import pandas as pd
import os
from fuzzywuzzy import process

dirname = os.path.dirname(__file__)
location = dirname + '/data/raw/'

for file in os.listdir(location):
    print(file)
    df_wiki = pd.read_csv('/Users/Friso/PycharmProjects/Master_Thesis/Project/GRID_Data/WikiDataGridExport.csv')
    df_QS = pd.read_csv(location + file, index_col='Unnamed: 0')
    df_QS['QS_World_University_ID'] = df_QS['href'].str.replace('/universities/', '')

    df = pd.merge(df_QS, df_wiki, on='QS_World_University_ID', how='left')
    df['fuzz_score'] = -1

    df_grid = pd.read_csv('/Users/Friso/PycharmProjects/Master_Thesis/Merge/grid/grid.csv')
    for index, row in df.iterrows():
        if pd.isnull(df.loc[index, 'GRID_ID']):
            university = df_QS.loc[index, 'Name']
            all_grid = list(df_grid['Name'])
            if university in all_grid:  # try to get exact matches
                df.loc[index, 'GRID_ID'] = df_grid.loc[df_grid['Name'] == university]['ID'].values[0]
            else:  # use fuzzywuzzy
                try:  # try to find match filtering on country
                    country = df_QS.loc[index, 'location']
                    df_choices = df_grid[df_grid['Country'] == country]
                    choices = list(df_choices['Name'])
                    fuzz = process.extractOne(df_QS.loc[index, 'Name'], choices)
                    grid_name = fuzz[0]
                    fuzz_score = fuzz[1]
                    grid_id = df_grid.loc[df_grid['Name'] == grid_name, 'ID'].iloc[0]
                    if fuzz_score > 89:
                        df.loc[index, 'GRID_ID'] = grid_id
                        df.loc[index, 'fuzz_score'] = fuzz_score

                except TypeError as e:  # use full choice list if country not found
                    print(df_QS.loc[index, 'location'], e)
                    choices = list(df_grid['Name'])
                    fuzz = process.extractOne(df_QS.loc[index, 'Name'], choices)
                    grid_name = fuzz[0]
                    fuzz_score = fuzz[1]
                    grid_id = df_grid.loc[df_grid['Name'] == grid_name, 'ID'].iloc[0]
                    if fuzz_score > 89:
                        df.loc[index, 'GRID_ID'] = grid_id
                        df.loc[index, 'fuzz_score'] = fuzz_score

    df.to_csv(dirname + '/data/grid/{}_grid.csv'.format(file.replace('.csv', '')))
    print(file, df['GRID_ID'].isnull().sum())
