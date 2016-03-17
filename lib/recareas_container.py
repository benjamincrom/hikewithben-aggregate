#!/usr/bin/python
'''
recareas_container.py -- Contains RecAreasContainer class which extracts and
holds all recarea objects in a dict keyed on RecArea ID.
'''
import json

class RecAreasContainer(object):
    """
    Container for RecArea DB file.  Initialization method reads DB into Python
    dictionary.
    """
    RECAREA_DB = 'files/original_data/recareas_db_files/RecAreas_API_v1.json'
    FACILITIES_DB = 'files/original_data/recareas_db_files/Facilities_API_v1.json'
    RECAREA_FACILITIES_LOOKUP_DB = (
        'files/original_data/recareas_db_files/RecAreaFacilities_API_v1.json'
    )

    def __init__(self):
        self.recarea_objects_dict = self.all_recarea_objects_dict()

    @classmethod
    def all_facility_objects_dict(cls):
        """ Return dictionary of all facility objects keyed on facility id """
        facility_objects_dict = {}
        with open(cls.FACILITIES_DB) as facilities_fh:
            facilities_json = facilities_fh.read().decode(
                'iso-8859-1'
            )

        facilities_list = json.loads(facilities_json).get('RECDATA')
        for facility in facilities_list:
            facility_objects_dict[facility['FacilityID']] = facility

        return facility_objects_dict

    @classmethod
    def all_facility_ids_by_recarea(cls):
        """ Return one to many dictionary of recarea id to facility ids """
        recarea_facilities_dict = {}
        with open(cls.RECAREA_FACILITIES_LOOKUP_DB) as recareas_facilities_fh:
            recareas_facilties_json = recareas_facilities_fh.read().decode(
                'iso-8859-1'
            )

        recarea_facilities_dict = {}
        recareas_facilities_db = json.loads(
            recareas_facilties_json
        ).get('RECDATA')

        for entry in recareas_facilities_db:
            if entry['RecAreaID'] in recarea_facilities_dict:
                recarea_facilities_dict[entry['RecAreaID']].add(
                    entry['FacilityID']
                )
            else:
                recarea_facilities_dict[entry['RecAreaID']] = set()
                recarea_facilities_dict[entry['RecAreaID']].add(
                    entry['FacilityID']
                )

        return recarea_facilities_dict

    @classmethod
    def recarea_facilities_dict(cls):
        """
        Return one-to-many lookup dictionary of recarea ids to facility entries
        """
        recarea_facilities_dict = {}
        recarea_facilities_lookup_dict = cls.all_facility_ids_by_recarea()
        facilities_dict = cls.all_facility_objects_dict()

        for recarea_id in recarea_facilities_lookup_dict:
            facility_id_list = recarea_facilities_lookup_dict[recarea_id]
            facility_list = []
            for facility_id in facility_id_list:
                facility = facilities_dict[facility_id]
                facility_list.append(facility)

            recarea_facilities_dict[recarea_id] = facility_list

        return recarea_facilities_dict

    @classmethod
    def all_recarea_objects_dict(cls):
        """
        Returns list of recarea json dictionaries.
        keys:
            'RecAreaEmail', 'RecAreaFeeDescription', 'RecAreaDescription',
            'StayLimit', 'RecAreaLongitude', 'RecAreaLatitude',
            'LastUpdatedDate', 'RecAreaMapURL', 'Keywords',
            'RecAreaPhone', 'RecAreaDirections', 'RecAreaName',
            'RecAreaReservationURL', 'OrgRecAreaID', 'RecAreaID'
        """
        recarea_objects_dict = {}
        recarea_facilities_dict = cls.recarea_facilities_dict()

        # Dump RIDB database json file to string
        with open(cls.RECAREA_DB) as recareas_filehandle:
            recareas_response_json = recareas_filehandle.read().decode(
                'iso-8859-1'
            )

        recarea_objects_list = json.loads(
            recareas_response_json
        ).get('RECDATA')

        recarea_objects_dict = {}
        for recarea_obj in recarea_objects_list:
            recarea_id = recarea_obj['RecAreaID']
            if recarea_id in recarea_facilities_dict:
                recarea_obj['facilities'] = recarea_facilities_dict[
                    recarea_id
                ]
            recarea_objects_dict[recarea_id] = recarea_obj

        return recarea_objects_dict

    def coordinates_of_recarea(self, recarea_id):
        """ Returns [latitude, longitude] of any recarea. """
        if recarea_id in self.recarea_objects_dict:
            coordinates = [
                self.recarea_objects_dict[recarea_id]['RecAreaLatitude'],
                self.recarea_objects_dict[recarea_id]['RecAreaLongitude']
            ]
        else:
            coordinates = None

        return coordinates

    def reservation_url(self, recarea_id):
        """ Returns reservation url of a given recarea """
        recarea_object = self.recarea_objects_dict.get(recarea_id)
        if recarea_object:
            reservation_url = recarea_object.get('RecAreaReservationURL')
        else:
            reservation_url = None

        return reservation_url
