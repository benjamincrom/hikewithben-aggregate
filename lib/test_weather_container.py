#!/usr/bin/python
"""
test_weather_container.py -- Unit tests for WeatherContainer class
"""
from lib import weather_container

weather_obj = weather_container.WeatherContainer()

def test_read_lines():
    lines = weather_obj.read_lines('test_weather_container.py')
    assert lines

def test_read_data_file():
    weather_obj.read_data_file('weather_db_files/dly-tavg-normal.txt',
                               'average_temp',
                               10.0)
    assert weather_obj.locations_weather_dict

def test_read_locations_file():
    weather_obj.read_locations_file('weather_db_files/ghcnd-stations.txt')
    assert weather_obj.coordinates_list and weather_obj.locations_metadata

def test_find_closest_station():
    assert weather_obj.find_closest_station((33.82, -84.32))
