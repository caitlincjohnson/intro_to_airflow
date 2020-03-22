import database_connections as db
import pandas as pd
import logging
import json
import urllib3
import yaml
from datetime import date


logging.basicConfig(filename='logs/etl.log', format='%(asctime)s %(message)s', level=logging.INFO)


class API:
    def __init__(self):
        with open("config.yaml", 'r') as f:
            try:
                self.config = yaml.load(Loader=yaml.FullLoader, stream=f)
            except yaml.YAMLError as exc:
                print(exc)

    def main(self):
        """
        Main script that executes the ETL
        """
        logging.info('Connecting to database')
        engine = db.postgres_connection()

        logging.info('Pull JSON data from NASA\'s public API')
        http = urllib3.PoolManager()
        start_date = '2020-02-03'
        end_date = '2020-02-10'
        pre_formatted_nasa_api = self.config['apis']['nasa']
        nasa_api = pre_formatted_nasa_api.format(start_date=start_date
                                                 , end_date=end_date)

        r = http.request('GET', nasa_api)
        data = json.loads(r.data.decode('utf-8'))

        columns = ['id', 'neo_reference_id', 'name', 'absolute_magnitude_h', 'estimated_diameter_min_meters'
            , 'estimated_diameter_max_meters', 'is_potentially_hazardous_asteroid', 'close_approach_date'
            , 'relative_velocity_kmph', 'miss_distance_km']
        df = pd.DataFrame(columns=columns)

        logging.info('Inserting relevant JSON data into Pandas dataframe')
        for group in data['near_earth_objects']:
            for asteroid in data['near_earth_objects'][group]:
                row = {
                    'id': asteroid['id']
                    , 'neo_reference_id': asteroid['neo_reference_id']
                    , 'name': asteroid['name']
                    , 'absolute_magnitude_h': asteroid['absolute_magnitude_h']
                    ,
                    'estimated_diameter_min_meters': asteroid['estimated_diameter']['meters']['estimated_diameter_min']
                    ,
                    'estimated_diameter_max_meters': asteroid['estimated_diameter']['meters']['estimated_diameter_max']
                    , 'is_potentially_hazardous_asteroid': asteroid['is_potentially_hazardous_asteroid']
                    , 'close_approach_date': asteroid['close_approach_data'][0]['close_approach_date']
                    , 'relative_velocity_kmph': asteroid['close_approach_data'][0]['relative_velocity'][
                        'kilometers_per_hour']
                    , 'miss_distance_km': asteroid['close_approach_data'][0]['miss_distance']['kilometers']
                }
                df = df.append(row, ignore_index=True)

        logging.info('Transforming data')
        df['load_date'] = date.today()

        logging.info('Inserting data into table')
        df.to_sql('asteroids', con=engine, if_exists='replace')
