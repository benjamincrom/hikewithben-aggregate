'''
create_db_file - Turn library of source data into a single recareas.json file for importing int
                 redis.
'''
import json
import re

from bs4 import BeautifulSoup

from lib.recareas_container import RecAreasContainer
from lib.weather_container import WeatherContainer

FACILITY_DESCRIPTION_REGEX = (
    r'Overview(?P<overview>.*)Natural Features:(?P<natural_features>.*)'
    r'Recreation:(?P<recreation>.*)Facilities:(?P<facilities>.*)'
)

RESERVATION_URL = ("http://www.recreation.gov/campsiteCalendar.do?page=''matrix"
                   "&contractCode=NRSO&parkId=%s")

OUTPUT_FILE_STR = 'files/recareas-{file_id}-of-{total_files}.json'
FILE_SIZE_LIMIT = 30000000

def clean_text(html):
    ''' If a bracket if found in input string, remove all html from input. '''
    if html.find('<') != -1:
        html = BeautifulSoup(html).get_text()

    return html

def create_facility_dict(facility_description):
    '''
    Turn a default facility description into a facility dict organized by
    overview, natural features, recreation, and facilities
    '''
    result = re.match(FACILITY_DESCRIPTION_REGEX, facility_description)
    if result:
        facility_description_dict = {
            'overview': result.group('overview'),
            'natural_features': result.group('natural_features'),
            'recreation': result.group('recreation'),
            'facilities': result.group('facilities'),
        }
    else:
        facility_description_dict = {
            'overview': facility_description,
            'natural_features': '',
            'recreation': '',
            'facilities': '',
        }

    return facility_description_dict

def get_output_str(recareas_dict):
    ''' Creates JSON output string respresentation of recareas_objects_dict. '''
    output_str_list = []
    j = len(recareas_dict.keys())
    i = 0
    output_str_list.append('{')
    for recarea_id, recarea in recareas_dict.iteritems():
        output_str_list.append(
            '"{}": {}'.format(recarea_id, json.dumps(recarea))
        )

        i += 1
        if i < j:
            output_str_list.append(',')

    output_str_list.append('}')
    output_str = ''.join(output_str_list)

    return output_str

def write_out(output_str):
    '''
    Write all aggregate recareas info out to a JSON file
    '''
    num_files = (len(output_str) // FILE_SIZE_LIMIT) + 1
    substring_size = (len(output_str) / num_files) + 1
    output_json_list = [output_str[x:x+substring_size]
                        for x in range(0, len(output_str), substring_size)]

    for file_index, output_json in enumerate(output_json_list):
        output_filename = OUTPUT_FILE_STR.format(file_id=file_index+1,
                                                 total_files=num_files)

        with open(output_filename, 'w') as filehandle:
            filehandle.write(output_json)

def run():
    ''' Run this module '''
    recareas_container = RecAreasContainer()
    weather_container = WeatherContainer()

    for recarea in recareas_container.recarea_objects_dict.values():
        if recarea['RecAreaLatitude'] and recarea['RecAreaLongitude']:
            (station_id, dist) = weather_container.find_closest_station(
                (recarea['RecAreaLatitude'],
                 recarea['RecAreaLongitude'])
            )

            if dist < 15.0:
                weather_dict = weather_container.locations_weather_dict[
                    station_id
                ]
                recarea['RecAreaWeatherStationID'] = station_id
                recarea['RecAreaWeatherStationDist'] = dist
                recarea['RecAreaWeatherDict'] = weather_dict
                recarea['RecAreaDescription'] = clean_text(
                    recarea['RecAreaDescription']
                )
                recarea['RecAreaDirections'] = clean_text(
                    recarea['RecAreaDirections']
                )

            for facility in recarea.get('facilities', []):
                facility['FacilityDescription'] = create_facility_dict(
                    clean_text(
                        facility['FacilityDescription']
                    )
                )
                facility['FacilityDirections'] = clean_text(
                    facility['FacilityDirections']
                )

                if facility['LegacyFacilityID']:
                    facility['ReservationUrl'] = (
                        RESERVATION_URL % int(facility['LegacyFacilityID'])
                    )
                else:
                    facility['ReservationUrl'] = ''

    output_str = get_output_str(recareas_container.recarea_objects_dict)
    write_out(output_str)

if __name__ == '__main__':
    run()

