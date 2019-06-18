import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style
import numpy as np
import os

style.use('ggplot')

grid_list = ['grid.168010.e', 'grid.1032.0', 'grid.7177.6', 'grid.194645.b', 'grid.6571.5']

dirname = os.getcwd()
dirname = dirname + '/Data/'

df_ARWU2018 = pd.read_csv(dirname + 'ARWU/ARWURanking_2018_grid.csv')
df_ARWU2017 = pd.read_csv(dirname + 'ARWU/ARWURanking_2017_grid.csv')
df_ARWU2016 = pd.read_csv(dirname + 'ARWU/ARWURanking_2016_grid.csv')
df_ARWU2015 = pd.read_csv(dirname + 'ARWU/ARWURanking_2015_grid.csv')
df_ARWU2014 = pd.read_csv(dirname + 'ARWU/ARWURanking_2014_grid.csv')
df_ARWU2013 = pd.read_csv(dirname + 'ARWU/ARWURanking_2013_grid.csv')
df_ARWU2012 = pd.read_csv(dirname + 'ARWU/ARWURanking_2012_grid.csv')

ARWU_DATA = ["GRID_ID", "Alumni", "Award", "HiCi", "NS", "PUB"]

df_ARWU2012 = df_ARWU2012[ARWU_DATA].dropna()
df_ARWU2013 = df_ARWU2013[ARWU_DATA].dropna()
df_ARWU2014 = df_ARWU2014[ARWU_DATA].dropna()
df_ARWU2015 = df_ARWU2015[ARWU_DATA].dropna()
df_ARWU2016 = df_ARWU2016[ARWU_DATA].dropna()
df_ARWU2017 = df_ARWU2017[ARWU_DATA].dropna()
df_ARWU2018 = df_ARWU2018[ARWU_DATA].dropna()

df_THE2012 = pd.read_csv(dirname + 'THE/THERanking2013__grid.csv')
df_THE2013 = pd.read_csv(dirname + 'THE/THERanking2014__grid.csv')
df_THE2014 = pd.read_csv(dirname + 'THE/THERanking2015__grid.csv')
df_THE2015 = pd.read_csv(dirname + 'THE/THERanking2016__grid.csv')
df_THE2016 = pd.read_csv(dirname + 'THE/THERanking2017__grid.csv')
df_THE2017 = pd.read_csv(dirname + 'THE/THERanking2018__grid.csv')
df_THE2018 = pd.read_csv(dirname + 'THE/THERanking2019__grid.csv')

THE_DATA = ["GRID_ID", "Teaching", "Rechearch", "Citations", "Industry_Income", "Internationals_Outlook"]

df_THE2012 = df_THE2012[THE_DATA].dropna()
df_THE2013 = df_THE2013[THE_DATA].dropna()
df_THE2014 = df_THE2014[THE_DATA].dropna()
df_THE2015 = df_THE2015[THE_DATA].dropna()
df_THE2016 = df_THE2016[THE_DATA].dropna()
df_THE2017 = df_THE2017[THE_DATA].dropna()
df_THE2018 = df_THE2018[THE_DATA].dropna()

df_QS2012 = pd.read_csv(dirname + 'QS/qs2013_grid.csv')
df_QS2013 = pd.read_csv(dirname + 'QS/qs2014_grid.csv')
df_QS2014 = pd.read_csv(dirname + 'QS/qs2015_grid.csv')
df_QS2015 = pd.read_csv(dirname + 'QS/qs2016_grid.csv')
df_QS2016 = pd.read_csv(dirname + 'QS/qs2017_grid.csv')
df_QS2017 = pd.read_csv(dirname + 'QS/qs2018_grid.csv')
df_QS2018 = pd.read_csv(dirname + 'QS/qs2019_grid.csv')

QS_DATA = ["GRID_ID", "Academic_reputation", "Employer_reputation", "Faculty_Student", "International_Faculty",
           "International_Students", "Citations"]

df_QS2018 = df_QS2018.replace(0, np.nan)
df_QS2017 = df_QS2017.replace(0, np.nan)
df_QS2016 = df_QS2016.replace(0, np.nan)
df_QS2015 = df_QS2015.replace(0, np.nan)
df_QS2014 = df_QS2014.replace(0, np.nan)
df_QS2013 = df_QS2013.replace(0, np.nan)
df_QS2012 = df_QS2012.replace(0, np.nan)

df_QS2018 = df_QS2018[QS_DATA].dropna()
df_QS2017 = df_QS2017[QS_DATA].dropna()
df_QS2016 = df_QS2016[QS_DATA].dropna()
df_QS2015 = df_QS2015[QS_DATA].dropna()
df_QS2014 = df_QS2014[QS_DATA].dropna()
df_QS2013 = df_QS2013[QS_DATA].dropna()
df_QS2012 = df_QS2012[QS_DATA].dropna()


def create_constructs(df_ARWU, df_THE, df_QS, year):
    df_ARWU['Reputation_ARWU'] = (df_ARWU['Alumni'] + df_ARWU['Award']) / 2
    df_ARWU['Publication_ARWU'] = (df_ARWU['HiCi'] + df_ARWU['NS'] + df_ARWU['PUB']) / 3
    df_ARWU = df_ARWU[['GRID_ID', 'Reputation_ARWU', 'Publication_ARWU']]
    df_ARWU['year'] = year
    df_ARWU = df_ARWU[['GRID_ID', 'year', 'Reputation_ARWU', 'Publication_ARWU']]
    df_ARWU.columns = ['GRID_ID', 'year', 'Reputation_ARWU', 'Publication_ARWU']

    df_THE['Reputation_THE'] = (df_THE['Teaching'] + df_THE['Rechearch']) / 2
    df_THE['Publication_THE'] = df_THE['Citations']
    df_THE = df_THE[['GRID_ID', 'Reputation_THE', 'Publication_THE']]
    df_THE['year'] = year
    df_THE = df_THE[['GRID_ID', 'year', 'Reputation_THE', 'Publication_THE']]
    df_THE.columns = ['GRID_ID', 'year', 'Reputation_THE', 'Publication_THE']

    df_QS['Reputation_QS'] = (df_QS['Academic_reputation'] + df_QS['Employer_reputation']) / 2
    df_QS['Publication_QS'] = df_QS['Citations']
    df_QS = df_QS[['GRID_ID', 'Reputation_QS', 'Publication_QS']]
    df_QS['year'] = year
    df_QS = df_QS[['GRID_ID', 'year', 'Reputation_QS', 'Publication_QS']]
    df_QS.columns = ['GRID_ID', 'year', 'Reputation_QS', 'Publication_QS']

    return df_ARWU, df_THE, df_QS


def add_arrow(line, position=None, direction='right', size=20, color=None):
    if color is None:
        color = line.get_color()

    xdata = line.get_xdata()
    ydata = line.get_ydata()

    for i in range(len(xdata) -1):
        position = xdata[i]
        start_ind = np.argmin(np.absolute(xdata - position))
        if direction == 'right':
            end_ind = start_ind + 1
        else:
            end_ind = start_ind - 1

        line.axes.annotate('',
            xytext=(xdata[start_ind], ydata[start_ind]),
            xy=(xdata[end_ind], ydata[end_ind]),
            arrowprops=dict(arrowstyle="-|>", color=color),
            size=size
        )
        

df_ARWU2018, df_THE2018, df_QS2018 = create_constructs(df_ARWU2018, df_THE2018, df_QS2018, '2018')
df_ARWU2017, df_THE2017, df_QS2017 = create_constructs(df_ARWU2017, df_THE2017, df_QS2017, '2017')
df_ARWU2016, df_THE2016, df_QS2016 = create_constructs(df_ARWU2016, df_THE2016, df_QS2016, '2016')
df_ARWU2015, df_THE2015, df_QS2015 = create_constructs(df_ARWU2015, df_THE2015, df_QS2015, '2015')
df_ARWU2014, df_THE2014, df_QS2014 = create_constructs(df_ARWU2014, df_THE2014, df_QS2014, '2014')
df_ARWU2013, df_THE2013, df_QS2013 = create_constructs(df_ARWU2013, df_THE2013, df_QS2013, '2013')
df_ARWU2012, df_THE2012, df_QS2012 = create_constructs(df_ARWU2012, df_THE2012, df_QS2012, '2012')

df_ARWU = df_ARWU2018
listARWU = [df_ARWU2017, df_ARWU2016, df_ARWU2015, df_ARWU2014, df_ARWU2013, df_ARWU2012]
for i in listARWU:
    df_ARWU = df_ARWU.append(i)

df_THE = df_THE2018
listTHE = [df_THE2017, df_THE2016, df_THE2015, df_THE2014, df_THE2013, df_THE2012]
for i in listTHE:
    df_THE = df_THE.append(i)

df_QS = df_QS2018
listQS = [df_QS2017, df_QS2016, df_QS2015, df_QS2014, df_QS2013, df_QS2012]
for i in listQS:
    df_QS = df_QS.append(i)


def create_uni_df(ARWU, THE, QS, GRID):
    ARWU = ARWU[ARWU['GRID_ID'] == GRID]
    THE = THE[THE['GRID_ID'] == GRID]
    QS = QS[QS['GRID_ID'] == GRID]

    return ARWU, THE, QS


fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

for i in grid_list:
    df_stanford_ARWU, df_stanford_THE, df_stanford_QS = create_uni_df(df_ARWU, df_THE, df_QS, i)
    
    line = ax1.plot(df_stanford_ARWU['Reputation_ARWU'], df_stanford_ARWU['Publication_ARWU'])[0]
    add_arrow(line)
    line = ax2.plot(df_stanford_THE['Reputation_THE'], df_stanford_THE['Publication_THE'])[0]
    add_arrow(line)
    line = ax3.plot(df_stanford_QS['Reputation_QS'], df_stanford_QS['Publication_QS'])[0]
    add_arrow(line)

ax1.set_title('ARWU')
ax2.set_title('THE')
ax3.set_title('QS')
fig.text(0.5, 0.04, 'Reputation', ha='center', va='center', fontsize=15)
fig.text(0.09, 0.5, 'Publication', ha='center', va='center', rotation='vertical', fontsize=15)
ax3.legend(grid_list, loc='right',
           bbox_to_anchor=(1.5, 0.5), ncol=1, fontsize='large', frameon=False)

plt.show()
