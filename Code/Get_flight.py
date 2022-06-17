import requests
import datetime
import pandas as pd
import numpy as np
import myconfig as cfg

path = '..\Data\\'

airpotrs=pd.read_csv(path+'airports.csv')

flights = pd.DataFrame(columns=['icao','date','num_of_arriv','num_of_depart'])

for a_icao in ['EDDB']:# airpotrs['icao']:
    n_arr = 0
    n_dep = 0
    date = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d') 
    t1=['00:00','12:00']
    t2=['11:59','23:59']
    
    headers = {
    	"X-RapidAPI-Host": "aerodatabox.p.rapidapi.com",
    	"X-RapidAPI-Key": cfg.get_data('AIR_API_KEY')
    }
    
    for i in range(2):
        url = f"https://aerodatabox.p.rapidapi.com/flights/airports/icao/{a_icao}/{date}T{t1[i]}/{date}T{t2[i]}"
        
        response = requests.request("GET", url, headers=headers)#, params=querystring)
        print('Status code',response.status_code)
        if response.status_code==200:
            flights_js = response.json()
            n_arr = n_arr + len(flights_js['arrivals'])
            n_dep = n_dep + len(flights_js['departures'])
        else:
            n_arr = np.nan
            n_dep = np.nan
 
    flights = flights.append({'icao':a_icao,
                  'date':date,
                  'num_of_arriv':n_arr,
                  'num_of_depart':n_dep
                  }
                  ,ignore_index=True)
        
flights.to_csv(path+'flights.csv', index=False)
