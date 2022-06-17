import requests
import pandas as pd
import myconfig as cfg

path = '..\Data\\'

cities_df = pd.read_csv(path+'cities.csv')
cities = cities_df['city']

airports = pd.DataFrame(columns=['city_id','lat','lon','icao','iata','name'])


for city in ['Berlin']:#cities:
    lat = float(cities_df.loc[cities_df['city']==city]['latitude'])
    lon = float(cities_df.loc[cities_df['city']==city]['longitude'])

    url = f"https://aerodatabox.p.rapidapi.com/airports/search/location/{lat}/{lon}/km/50/16"
    
    querystring = {"withFlightInfoOnly":"0"}
    
    headers = {
            	"X-RapidAPI-Key": cfg.get_data('AIR_API_KEY'),
            	"X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
            }
    
    response = requests.request("GET", url, headers=headers)#, params=querystring)
    print('Status code',response.status_code)
    airp_js = response.json()
    
    for a in airp_js["items"]:
        airports = airports.append({'city_id': cities_df[cities_df['city']==city].city_id.iloc[0],
                      'lat':a["location"]["lat"],
                      'lon':a["location"]["lon"],
                      'icao':a["icao"],
                      'iata':a["iata"],
                      'name':a["name"]
                      }
                      ,ignore_index=True)

        
airports.to_csv(path+'airports.csv', index=False)
