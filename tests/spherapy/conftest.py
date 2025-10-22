import pytest
import spherapy
from importlib import resources

@pytest.fixture(scope='module')

def pytestFillPackagedData():
	old_packaged_TLEs = spherapy.packaged_TLEs
	print('Filling packaged TLEs index from data dir')  		#noqa: T201

	# find path of spherapy package dir
	package_dir = resources.files('spherapy')
	# packaged TLEs stored in
	TLE_dir = package_dir.joinpath('data').joinpath('TLEs')
	entries = TLE_dir.glob('**/*')
	files = [x for x in entries if x.is_file()]

	packaged_TLEs = {}
	# extract TLE files and add to packaged_TLEs
	for file in files:
		try:
			tle_id = int(file.stem)
		except ValueError:
			print("Can't import packaged TLEs, skipping...") 	#noqa: T201
			return None
		packaged_TLEs[tle_id] = file
	spherapy.packaged_TLEs = packaged_TLEs

	yield
	# Tear down
	print('Restoring packaged TLEs:') 							#noqa: T201
	spherapy.packaged_TLEs = old_packaged_TLEs
