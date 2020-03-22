'Combines daily csv files into a historical CSV file'

import pandas as pd
import os
from datetime import  date

daily_csv = os.path.join('..','data/cases/daily_csv_files')
save_path = os.path.join('..' , 'data/cases/historical_data')
county_list = []
frames_list = []
no_days = 0


column_list = [ ]
column_list.append("County")
for file in os.listdir(daily_csv ):
    if file.endswith(".csv"):
        data_temp = pd.read_csv(os.path.join(daily_csv,file))
        column_list.append(list(data_temp.columns)[-1])
        day_county_list = data_temp['Counties'].apply(lambda x: x.rstrip()).to_list()
        frames_list.append(data_temp)
        county_list.extend(day_county_list)
        no_days = no_days + 1


unique_counties = list(set(county_list))

county_cases = [ ]
for county in unique_counties:
    list_cases = [ ]
    list_cases.append(county)
    for df in frames_list:
        pz = df[df['Counties'].apply(lambda x : x.lower()) == county.lower()].iloc[:, 1].to_list()
        if not pz:
            list_cases.append(0)
        else:
            list_cases.append(pz[0])

    county_cases.append(list_cases)





combined_df = pd.DataFrame(columns= column_list, data = county_cases)
combined_df.to_csv(os.path.join( save_path, 'Cases_'+str( date.today ( ) ) +'.csv' ))