import pytest
import numpy as np
from spherapy.util import epoch_u
import datetime as dt


import logging
logging.disable(logging.CRITICAL)


@pytest.fixture(scope='module')
def date_ranges() -> tuple[np.ndarray, np.ndarray]:
	date_range1 = np.arange(dt.datetime(2020,7,1), dt.datetime(2021,1,1), dt.timedelta(days=0.5)).astype(dt.datetime)
	date_range2 = np.arange(dt.datetime(2020,7,1,0,0,10), dt.datetime(2021,8,1,0,0,10), dt.timedelta(minutes=1)).astype(dt.datetime)
	return date_range1, date_range2

def test_priorToSourceArr(date_ranges:tuple):
	search_arr = np.arange(dt.datetime(2019,7,1), dt.datetime(2019,7,1,5,59), dt.timedelta(minutes=1)).astype(dt.datetime)
	idxs = epoch_u.findClosestDatetimeIndices(search_arr, date_ranges[0])
	assert len(search_arr) == len(idxs)
	expected_arr = np.zeros(len(search_arr))
	assert np.allclose(idxs, expected_arr)

def test_postSourceArr(date_ranges:tuple):
	search_arr = np.arange(dt.datetime(2022,7,1), dt.datetime(2022,7,1,5,59), dt.timedelta(minutes=1)).astype(dt.datetime)
	idxs = epoch_u.findClosestDatetimeIndices(search_arr, date_ranges[0])
	assert len(search_arr) == len(idxs)
	expected_arr = np.full(len(search_arr),len(date_ranges[0])-1)
	assert np.allclose(idxs, expected_arr)

def test_withinClosestToFirst(date_ranges:tuple):
	# all closest to idx=0
	search_arr = np.arange(dt.datetime(2020,7,1), dt.datetime(2020,7,1,5,59), dt.timedelta(minutes=1)).astype(dt.datetime)
	idxs = epoch_u.findClosestDatetimeIndices(search_arr, date_ranges[0])
	assert len(search_arr) == len(idxs)
	expected_arr = np.zeros(len(search_arr))
	assert np.allclose(idxs, expected_arr)

def test_withinSplitFirstSecond1(date_ranges:tuple):
	# all but last closest to idx=0
	search_arr = np.arange(dt.datetime(2020,7,1), dt.datetime(2020,7,1,6,2), dt.timedelta(minutes=1)).astype(dt.datetime)
	idxs = epoch_u.findClosestDatetimeIndices(search_arr, date_ranges[0])
	assert len(search_arr) == len(idxs)
	expected_arr = np.zeros(len(search_arr))
	expected_arr[-1] = 1
	assert np.allclose(idxs, expected_arr)

def test_withinSplitFirstSecond2(date_ranges:tuple):
	# split between 330 and 331 for idx = 0
	search_arr = np.arange(dt.datetime(2020,7,1,0,30), dt.datetime(2020,7,1,6,32), dt.timedelta(minutes=1)).astype(dt.datetime)
	idxs = epoch_u.findClosestDatetimeIndices(search_arr, date_ranges[0])
	assert len(search_arr) == len(idxs)
	expected_arr = np.zeros(len(search_arr))
	expected_arr[-31:] = 1
	assert np.allclose(idxs, expected_arr)

def test_withinSplitArbitrary1(date_ranges:tuple):
	# all but last closest to idx=317 (randomly chosen)
	search_arr = np.arange(dt.datetime(2020, 12, 6, 12, 0), dt.datetime(2020, 12, 6, 18, 2), dt.timedelta(minutes=1)).astype(dt.datetime)
	idxs = epoch_u.findClosestDatetimeIndices(search_arr, date_ranges[0])
	assert len(search_arr) == len(idxs)
	expected_arr = np.full(len(search_arr), 317)
	expected_arr[-1] = 318
	assert np.allclose(idxs, expected_arr)

def test_withinSplitArbitrary2(date_ranges:tuple):
	# split between 270 and 271 for idx = 317
	search_arr = np.arange(dt.datetime(2020, 12, 6, 13, 30), dt.datetime(2020, 12, 6, 19, 32), dt.timedelta(minutes=1)).astype(dt.datetime)
	idxs = epoch_u.findClosestDatetimeIndices(search_arr, date_ranges[0])
	assert len(search_arr) == len(idxs)
	expected_arr = np.full(len(search_arr), 317)
	expected_arr[-91:] = 318
	assert np.allclose(idxs, expected_arr)

def test_withinMultiSplit1(date_ranges:tuple):
	# closest to 131,132,133,134,135
	search_arr = np.arange(dt.datetime(2020, 9, 4, 9, 5, 25), dt.datetime(2020, 9, 6, 8, 10, 0), dt.timedelta(seconds=477)).astype(dt.datetime)
	idxs = epoch_u.findClosestDatetimeIndices(search_arr, date_ranges[0])
	assert len(search_arr) == len(idxs)
	expected_arr = np.full(len(search_arr), 131)
	expected_arr[68:158] = 132
	expected_arr[158:249] = 133
	expected_arr[249:339] = 134
	expected_arr[339:] = 135
	assert np.allclose(idxs, expected_arr)

def test_withinMultiSplit2(date_ranges:tuple):
	# closest to 131,132,133,134,135
	search_arr = np.arange(dt.datetime(2020, 9, 4, 12, 5, 25), dt.datetime(2020, 9, 6, 11, 10, 0), dt.timedelta(seconds=477)).astype(dt.datetime)
	idxs = epoch_u.findClosestDatetimeIndices(search_arr, date_ranges[0])
	assert len(search_arr) == len(idxs)
	expected_arr = np.full(len(search_arr), 131)
	expected_arr[45:136] = 132
	expected_arr[136:226] = 133
	expected_arr[226:317] = 134
	expected_arr[317:] = 135
	assert np.allclose(idxs, expected_arr)

def test_searchArrStepsLarger(date_ranges:tuple):
	search_arr = np.arange(dt.datetime(2020,7,2), dt.datetime(2020,7,9), dt.timedelta(days=1)).astype(dt.datetime)
	idxs = epoch_u.findClosestDatetimeIndices(search_arr, date_ranges[1])
	assert len(search_arr) == len(idxs)
	expected_arr = np.array((1440, 2880, 4320, 5760, 7200, 8640, 10080))
	assert np.allclose(idxs, expected_arr)
