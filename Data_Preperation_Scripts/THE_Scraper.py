import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import os

dirname = os.path.dirname(__file__)

for i in range(9):
    year = str(2011 + i)
    print(year)
    url = ('https://www.timeshighereducation.com/world-university-rankings/' + year +
           '/world-ranking#!/page/0/length/-1/sort_by/rank/sort_order/asc/cols/scores')

    firefoxProfile = webdriver.FirefoxProfile()
    firefoxProfile.set_preference('permissions.default.stylesheet', 2)
    firefoxProfile.set_preference('permissions.default.image', 2)
    firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    firefoxProfile.set_preference("http.response.timeout", 10)
    firefoxProfile.set_preference("dom.max_script_run_time", 10)

    driver = webdriver.Firefox(executable_path='Path_To_GeckoDriver',
                               firefox_profile=firefoxProfile)
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    table = soup.find('table', {'id': 'datatable-1'})
    # print(table)

    rank_list = []
    university_name_list = []
    location_list = []
    overall_list = []
    teaching_list = []
    research_list = []
    citations_list = []
    industry_income_list = []
    international_outlook_list = []
    for row in table.findAll('tr')[1:]:
        col = row.findAll('td')
        rank_list.append(col[0].getText())
        university_name_list.append(col[1].find('a', {'class': 'ranking-institution-title'}).getText())
        location_list.append(col[1].find('div', {'class': 'location'}).getText())
        overall_list.append(col[2].getText())
        teaching_list.append(col[3].getText())
        research_list.append(col[4].getText())
        citations_list.append(col[5].getText())
        industry_income_list.append(col[6].getText())
        international_outlook_list.append(col[7].getText())

    # retrieve stats
    url = ('https://www.timeshighereducation.com/world-university-rankings/' + year +
           '/world-ranking#!/page/0/length/-1/sort_by/rank/sort_order/asc/cols/stats')

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    table = soup.find('table', {'id': 'datatable-1'})

    rank_list = []
    university_name_list = []
    location_list = []
    n_students = []
    n_students_staff = []
    international_students = []
    m_v_ratio = []
    href = []
    for row in table.findAll('tr')[1:]:
        col = row.findAll('td')
        rank_list.append(col[0].getText())
        university_name_list.append(col[1].find('a', {'class': 'ranking-institution-title'}).getText())
        location_list.append(col[1].find('div', {'class': 'location'}).getText())
        href.append(col[1].find('a').get('href'))
        n_students.append(col[2].getText())
        n_students_staff.append(col[3].getText())
        international_students.append(col[4].getText())
        m_v_ratio.append(col[5].getText())

    df = pd.DataFrame({
        'rank': rank_list,
        'Name': university_name_list,
        'Location': location_list,
        'Overall': overall_list,
        'Teaching': teaching_list,
        'Rechearch': research_list,
        'Citations': citations_list,
        'Industry_Income': industry_income_list,
        'Internationals_Outlook': international_outlook_list,
        'n_students': n_students,
        'student_staff_ratio': n_students_staff,
        'n_international_students': international_students,
        'm_v_ratio': m_v_ratio,
        'href': href
    })

    df.to_csv(dirname + '/data/raw/THERanking_{}.csv'.format(year))
