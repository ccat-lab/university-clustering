import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

dirname = os.path.dirname(__file__)

for i in range(14):
    year = str(2005 + i)
    print(year)
    url = ('http://www.shanghairanking.com/ARWU' + year + '.html')
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', {'name': 'UniversityRanking'})

    worldrank_list = []
    nationalrank_list = []
    university_list = []
    ARWU_university_ID_list = []
    country_list = []
    totalscore_list = []
    alumni_list = []
    award_list = []
    hici_list = []
    ns_list = []
    pub_list = []
    pcp_list = []
    for row in table.findAll('tr')[1:]:
        col = row.findAll('td')
        worldrank_list.append((col[0].getText()))
        university_list.append((col[1].getText()))
        ARWU_university_ID_list.append(col[1].find('a').get('href').replace('World-University-Rankings/', '')
                                       .replace('.html', ''))
        country_list.append(col[2].a.img['src'].replace('image/flag/', '').replace('.png', '').strip().lower())
        nationalrank_list.append((col[3].getText()))
        totalscore_list.append((col[4].getText()))
        alumni_list.append((col[5].getText()))
        award_list.append((col[6].getText()))
        hici_list.append((col[7].getText()))
        ns_list.append((col[8].getText()))
        pub_list.append((col[9].getText()))
        pcp_list.append((col[10].getText()))

    df = pd.DataFrame({
        'WorldRank': worldrank_list,
        'NationalRank': nationalrank_list,
        'Name': university_list,
        'ARWU_university_ID': ARWU_university_ID_list,
        'Country': country_list,
        'TotalScore': totalscore_list,
        'Alumni': alumni_list,
        'Award': award_list,
        'HiCi': hici_list,
        'NS': ns_list,
        'PUB': pub_list,
        'PCP': pcp_list
    })

    df.to_csv(dirname + '/data/raw/ARWURanking_{}.csv'.format(year))





