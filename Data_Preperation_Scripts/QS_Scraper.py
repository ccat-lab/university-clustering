import pandas as pd
from bs4 import BeautifulSoup
import os

dirname = os.path.dirname(__file__)
location = dirname + '/data/html/'

for file in os.listdir(location):
    print(file)
    if file.endswith('.txt'):
        with open(location + file, 'r') as f:
            text = f.read()

        soup = BeautifulSoup(text, 'html.parser')
        table = soup.find('table', {'id': 'qs-rankings-indicators'})

        rank_list = []
        uni_list = []
        score_list = []
        acedemic_reputation_list = []
        href_list = []
        employer_reputation_list = []
        faculty_student_list = []
        international_faculty_list = []
        international_students_list = []
        citations_list = []
        for row in table.findAll('tr')[1:]:
            col = row.findAll('td')
            rank_list.append(col[0].getText())
            uni_list.append(col[1].getText())
            href_list.append(col[1].find('a').get('href'))
            score_list.append(col[2].getText())
            acedemic_reputation_list.append(col[3].getText())
            employer_reputation_list.append(col[4].getText())
            faculty_student_list.append(col[5].getText())
            international_faculty_list.append(col[6].getText())
            international_students_list.append(col[7].getText())
            citations_list.append(col[8].getText())

        with open(location + 'locations/' + file, 'r') as g:
            location_text = g.read()

        location_uni_list = []
        location_list = []
        location_soup = BeautifulSoup(location_text, 'html.parser')
        location_table = location_soup.find('table', {'id': 'qs-rankings'})
        for location_row in location_table.findAll('tr')[1:]:
            location_col = location_row.findAll('td')
            location_uni_list.append(location_col[1].getText().replace('More', ''))
            location_list.append((location_col[2].getText()))

        df = pd.DataFrame({
            'Rank': rank_list,
            'Name': uni_list,
            'score_list': score_list,
            'Academic_reputation': acedemic_reputation_list,
            'Employer_reputation': employer_reputation_list,
            'Faculty_Student': faculty_student_list,
            'International_Faculty': international_faculty_list,
            'International_Students': international_students_list,
            'Citations': citations_list,
            'href': href_list
        })

        df_location = pd.DataFrame({
            'Name': location_uni_list,
            'location': location_list,
        })

        df_merged = pd.merge(df, df_location, on='Name', how='left')
        # print(df_merged)

        df_merged.to_csv(dirname + '/data/raw/{}'.format(file.replace('txt', 'csv')))
