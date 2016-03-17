#!/usr/bin/python
""" test_recareas_container.py -- test RecAreasContainer class """
from lib import recareas_container

recareas_obj = recareas_container.RecAreasContainer()

def test_all_facility_objects_dict():
    assert recareas_obj.all_facility_objects_dict()

def test_all_facility_ids_by_recarea():
    assert recareas_obj.all_facility_ids_by_recarea()

def test_recarea_facilities_dict():
    assert recareas_obj.recarea_facilities_dict()

def test_all_recarea_objects_dict():
    assert recareas_obj.all_recarea_objects_dict()

def test_filter_recarea_objects_list():
    assert recareas_obj.filter_recarea_objects_list("National Park")

def test_all_national_park_objects():
    assert recareas_obj.all_national_park_objects()

def test_all_state_park_objects():
    assert recareas_obj.all_state_park_objects()

def test_all_wilderness_objects():
    assert recareas_obj.all_wilderness_objects()

def test_all_national_forest_objects():
    assert recareas_obj.all_national_forest_objects()

def test_all_national_monument_objects():
    assert recareas_obj.all_national_monument_objects()

def test_all_national_preserve_objects():
    assert recareas_obj.all_national_preserve_objects()

def test_all_national_recreation_areas():
    assert recareas_obj.all_national_recreation_areas()

def test_coordinates_of_recarea():
    assert recareas_obj.coordinates_of_recarea(2864)

def test_coordinates_of_recarea_bad_id():
    assert recareas_obj.coordinates_of_recarea(2864342344) is None

def test_reservation_url():
    assert recareas_obj.reservation_url(3102)

def test_reservation_url_bad_id():
    assert recareas_obj.reservation_url(31024324325) is None
