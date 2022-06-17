import geocoder
import pandas as pd
import time
import myconfig as cfg

path = "..\Data\\"

cities_df = pd.DataFrame(columns=['city_id',
                                  'city',
                                  'country',
                                  'country_code',
                                  'population',
                                  'time_zone',
                                  'latitude',
                                  'longitude']) 
ec = pd.read_csv(path+'EuroCitiesPopulation15.csv')
wc = pd.read_csv(path+'world_cities.csv')

countries = ec.country
cities = ec.name

city_id=[]
for co,ci in zip(countries,cities):
    city_id=city_id+[(wc.set_index('country').loc[co].set_index('name').loc[ci].geonameid)]
    
   
if time.daylight!=0:
    dt=1
else:
    dt=0
    
for idx,c in enumerate(city_id):
    
    g = geocoder.geonames(c, method='details', key=cfg.get_data('GEO_NAMES_KEY'))
    cities_df=cities_df.append({'city_id':c,
                                'city':ec['name'].loc[idx],
                                'country': ec['country'].loc[idx],
                                'country_code':g.geojson['features'][0]['properties']['country_code'],
                                'population':g.geojson['features'][0]['properties']['population'],
                                'time_zone':3600*(dt+g.geojson['features'][0]['properties']['raw']['timezone']['gmtOffset']),
                                'latitude':g.geojson['features'][0]['properties']['lat'],
                                'longitude':g.geojson['features'][0]['properties']['lng']
                                },
                               ignore_index=True)

        
cities_df.to_csv(path+'cities.csv', index=False) 
