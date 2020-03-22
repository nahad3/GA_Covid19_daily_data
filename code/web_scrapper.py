'Scrapes daily cases data and saves into a csv file'

import pandas as pd
import urllib.request
from datetime import date
import os
from bs4 import BeautifulSoup

"URL to scrap data from"
url = "https://dph.georgia.gov/covid-19-daily-status-report"



page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')
captions = soup.find_all('caption')

for caption in captions:
    if caption.get_text() == 'COVID-19 Confirmed Cases by County':
        table = caption.find_parent('table', {'class': 'stacked-row-plus'})

all_rows = table.find_all('tr')


county_list = []
cases = []

all_rows = all_rows[1:]
for row in all_rows:
    columns = row.find_all('td')
    county_list.append(columns[len(columns)-2].get_text())
    cases.append(columns[len(columns)-1].get_text())


date_report = str(date.today())


dict = {'Counties': county_list, date_report : cases }

df = pd.DataFrame(dict)

base_path = os.path.join('..','data/cases/daily_csv_files')
file_name = date_report+'.csv'
full_path = os.path.join(base_path,file_name)
df.to_csv(full_path, index=False)