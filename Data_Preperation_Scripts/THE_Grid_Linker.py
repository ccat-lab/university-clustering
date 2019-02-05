import pandas as pd
from fuzzywuzzy import process
import os

dirname = os.path.dirname(__file__)
location = dirname + '/data/raw/'

for file in os.listdir(location):
    df_wiki = pd.read_csv('/Users/Friso/PycharmProjects/Master_Thesis/Project/GRID_Data/WikiDataGridExport.csv')
    df_THE = pd.read_csv(location + file,
                         index_col='Unnamed: 0')

    df_THE['Times_Higher_Education_World_University_ID'] = df_THE['href'].str.replace('/world-university-rankings/', '')

    df = pd.merge(df_THE, df_wiki, on='Times_Higher_Education_World_University_ID', how='left')
    df['fuzz_score'] = -1

    df_grid = pd.read_csv('/Users/Friso/PycharmProjects/Master_Thesis/Project/GRID_Data/grid.csv')
    for index, row in df.iterrows():
        if pd.isnull(df.loc[index, 'GRID_ID']):
            university = df_THE.loc[index, 'Name']
            all_grid = list(df_grid['Name'])
            if university in all_grid:  # try to get exact matches
                df.loc[index, 'GRID_ID'] = df_grid.loc[df_grid['Name'] == university]['ID'].values[0]
            else:  # use fuzzywuzzy
                try:  # try to find match filtering on country
                    country = df_THE.loc[index, 'Location']
                    df_choices = df_grid[df_grid['Country'] == country]
                    choices = list(df_choices['Name'])
                    fuzz = process.extractOne(df_THE.loc[index, 'Name'], choices)
                    grid_name = fuzz[0]
                    fuzz_score = fuzz[1]
                    grid_id = df_grid.loc[df_grid['Name'] == grid_name, 'ID'].iloc[0]
                    if fuzz_score > 89:
                        df.loc[index, 'GRID_ID'] = grid_id
                        df.loc[index, 'fuzz_score'] = fuzz_score

                except TypeError as e:  # use full choice list if country not found
                    print(e)
                    choices = list(df_grid['Name'])
                    fuzz = process.extractOne(df_THE.loc[index, 'Name'], choices)
                    grid_name = fuzz[0]
                    fuzz_score = fuzz[1]
                    grid_id = df_grid.loc[df_grid['Name'] == grid_name, 'ID'].iloc[0]
                    if fuzz_score > 89:
                        df.loc[index, 'GRID_ID'] = grid_id
                        df.loc[index, 'fuzz_score'] = fuzz_score

    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        # print(df)

    print(file, df['GRID_ID'].isnull().sum())
    df.to_csv(dirname + '/data/grid/{}_grid.csv'.format(file.replace('.csv', '')))
