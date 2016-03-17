#!/usr/bin/python
'''
weather_container.py -- read NOAA 1981-2010 U.S. Climate Normals from
                        files/original_data/weather_db_files into a single
                        Python dictionary
'''
import datetime
import os

from lib.common_utilities import travel

class WeatherContainer(object):
    '''
    Compile several weather value dictionaries into a single nested dictionary
    which gives several daily averages throught the year
    '''
    DAILY_AVERAGE_TEMP_FILE = 'files/original_data/weather_db_files/dly-tavg-normal.txt'
    AVERAGE_TEMP_LABEL = 'average_temp'

    DAILY_MAX_TEMP_FILE = 'files/original_data/weather_db_files/dly-tmax-normal.txt'
    MAX_TEMP_LABEL = 'max_temp'

    DAILY_MIN_TEMP_FILE = 'files/original_data/weather_db_files/dly-tmin-normal.txt'
    MIN_TEMP_LABEL = 'min_temp'

    DAILY_RAIN_25_FILE = 'files/original_data/weather_db_files/dly-prcp-25pctl.txt'
    RAIN_25_LABEL = 'quartile_25_precip'

    DAILY_RAIN_50_FILE = 'files/original_data/weather_db_files/dly-prcp-50pctl.txt'
    RAIN_50_LABEL = 'quartile_50_precip'

    DAILY_RAIN_75_FILE = 'files/original_data/weather_db_files/dly-prcp-75pctl.txt'
    RAIN_75_LABEL = 'quartile_75_precip'

    STATIONS_METADATA_FILE = 'files/original_data/weather_db_files/ghcnd-stations.txt'
    NULL_DATE_VALUE = '-8888'

    def __init__(self):
        self.locations_weather_dict = {}
        self.read_data_file(self.DAILY_AVERAGE_TEMP_FILE,
                            self.AVERAGE_TEMP_LABEL, 10.0)
        self.read_data_file(self.DAILY_MAX_TEMP_FILE, self.MAX_TEMP_LABEL, 10.0)
        self.read_data_file(self.DAILY_MIN_TEMP_FILE, self.MIN_TEMP_LABEL, 10.0)
        self.read_data_file(self.DAILY_RAIN_25_FILE, self.RAIN_25_LABEL, 1.0)
        self.read_data_file(self.DAILY_RAIN_50_FILE, self.RAIN_50_LABEL, 1.0)
        self.read_data_file(self.DAILY_RAIN_75_FILE, self.RAIN_75_LABEL, 1.0)

        self.erase_entries_with_no_temp_data()

        self.locations_metadata = {}
        self.coordinates_list = []
        self.read_locations_file(self.STATIONS_METADATA_FILE)

    def erase_entries_with_no_temp_data(self):
        ''' Erase weather station entries with no temperature data '''
        keys_to_be_removed = []
        for station_id in self.locations_weather_dict:
            has_temp = True
            for date_tuple in self.locations_weather_dict[station_id]:
                entry_dict = self.locations_weather_dict[station_id][date_tuple]
                if ('min_temp' not in entry_dict or
                        'max_temp' not in entry_dict or
                        'average_temp' not in entry_dict):
                    has_temp = False

            if not has_temp:
                keys_to_be_removed.append(station_id)

        for key in keys_to_be_removed:
            self.locations_weather_dict.pop(key)

    @staticmethod
    def read_lines(file_name):
        ''' readlines() on file_name '''
        with open(file_name) as file_handle:
            return file_handle.readlines()

    def read_data_file(self, file_name, label, divisor):
        '''
        Read a weather file and add its data to self.locations_weather_dict
        '''
        lines_array = self.read_lines(file_name)
        for line in lines_array:
            line_list = line.split()
            while self.NULL_DATE_VALUE in line_list:
                line_list.remove(self.NULL_DATE_VALUE)

            station_id = line_list.pop(0)
            month = int(line_list.pop(0))

            if station_id not in self.locations_weather_dict:
                self.locations_weather_dict[station_id] = {}

            month_day_dict = self.locations_weather_dict[station_id]

            for index in range(len(line_list)):
                day = index + 1
                day_of_year = int(
                    datetime.datetime(
                        2000,
                        month,
                        day
                    ).timetuple().tm_yday
                )
                if day_of_year not in month_day_dict:
                    month_day_dict[day_of_year] = {}

                value = int(line_list[index][:-1]) / divisor
                month_day_dict[day_of_year][label] = value

    def read_locations_file(self, file_name):
        ''' Read locations metadata file into object '''
        lines_array = self.read_lines(file_name)
        for line in lines_array:
            line_list = line.split()
            station_id = line_list.pop(0)
            if station_id in self.locations_weather_dict:
                latitude = float(line_list.pop(0))
                longitude = float(line_list.pop(0))
                coordinate = (latitude, longitude)
                self.locations_metadata[coordinate] = station_id
                self.coordinates_list.append(coordinate)

    def find_closest_station(self, coordinate):
        '''
        Calculate the distance to every weather station and return the ID of
        the closest one.
        '''
        distance_coordinate_dict = travel.distance_dict_from_coordinate(
            coordinate,
            self.coordinates_list
        )

        shortest_distance = min(distance_coordinate_dict)
        nearest_coordinate = distance_coordinate_dict[shortest_distance]
        station_id = self.locations_metadata[nearest_coordinate]

        return (station_id, shortest_distance)
