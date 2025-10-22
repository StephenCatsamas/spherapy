import pytest
from pytest_check import check
import pathlib
import numpy as np
from spherapy import orbit
from spherapy import timespan
from spherapy import updater
from spherapy.util import orbital_u
import spherapy.util.exceptions as exceptions
import datetime as dt

# Disable logging during testing
import logging
logging.disable(logging.CRITICAL)

	# TODO: test getClosestAttribute
	# TODO: check validity of TLE Gen
	# TODO: check validity of propagated parameters Gen
	# TODO: check validity of Analytical Gen
	# TODO: test non earth orbits
	# TODO: test datetime split across multiple TLE epochs
		# TODO: check listed TLE epochs change at correct point of array
		# TODO: check less than 14 day propagation forward or back is all good

@pytest.fixture(scope='module', autouse=True)
def propagationData(pytestFillPackagedData:None) -> dict: 			#noqa: ARG001
	data = {}
	# Keep number of samples low, no need for lots of samples if only really testing attributes.
	data['t0'] = dt.datetime(2004, 12, 29, 0, 0, 1)
	data['t'] = timespan.TimeSpan(data['t0'], '1S', '2M')
	data['t02'] = dt.datetime(2021, 11, 23, 0, 0, 1)
	data['t1'] = timespan.TimeSpan(data['t02'], '1S', '2M')
	data['pos'] = np.tile(np.linspace(7200,8000,len(data['t']),dtype=np.float64),(3,1)).T

	# From multiple TLEs
	ISS_satcat_id = 25544
	data['ISS_tle_path'] = updater.getTLEFilePaths([ISS_satcat_id], use_packaged=True)[0]

	data['o_tle'] = orbit.Orbit.fromTLE(data['t'], pathlib.Path(data['ISS_tle_path']))
	data['o_tle_astro'] = orbit.Orbit.fromTLE(data['t1'], pathlib.Path(data['ISS_tle_path']), astrobodies=True)

	# From fake TLE
	data['o_ftle'] = orbit.Orbit.fromPropagatedOrbitalParam(data['t'], a=(6378 + 600), ecc=0, inc=45, raan=0, argp=0, mean_nu=0)
	data['o_ftle_astro'] = orbit.Orbit.fromPropagatedOrbitalParam(data['t'], a=(6378 + 600), ecc=0, inc=45, raan=0, argp=0, mean_nu=0, astrobodies=True)

	# Analytic from orbital param
	data['o_analytical'] = orbit.Orbit.fromAnalyticalOrbitalParam(data['t'], a=(6378 + 600), ecc=0, inc=45, raan=0, argp=0, mean_nu=0)
	data['o_analytical_astro'] = orbit.Orbit.fromAnalyticalOrbitalParam(data['t'], a=(6378 + 600), ecc=0, inc=45, raan=0, argp=0, mean_nu=0, astrobodies=True)

	# From list of position
	data['o_poslist'] = orbit.Orbit.fromListOfPositions(data['t'], data['pos'])
	data['o_poslist_astro'] = orbit.Orbit.fromListOfPositions(data['t'], data['pos'], astrobodies=True)

	# Dummy const pos
	data['o_static'] = orbit.Orbit.fromDummyConstantPosition(data['t'], np.zeros((len(data['t']),3)))
	data['o_static_astro'] = orbit.Orbit.fromDummyConstantPosition(data['t'], np.zeros((len(data['t']),3)), sun_pos=np.ones((len(data['t']),3)), moon_pos=-1*np.ones((len(data['t']),3)))

	return data

def test_TLEGenAttributes(propagationData:dict):
	'''
	Test for existance of required attributes in the orbit class
	'''

	propagationData['o_tle'].name
	propagationData['o_tle'].satcat_id
	propagationData['o_tle'].gen_type
	propagationData['o_tle'].timespan
	propagationData['o_tle'].TLE_epochs
	propagationData['o_tle'].pos
	propagationData['o_tle'].pos_ecef
	propagationData['o_tle'].vel_ecef
	propagationData['o_tle'].vel
	propagationData['o_tle'].lat
	propagationData['o_tle'].lon
	propagationData['o_tle'].sun_pos
	propagationData['o_tle'].moon_pos
	propagationData['o_tle'].alt
	propagationData['o_tle'].eclipse
	propagationData['o_tle'].central_body
	propagationData['o_tle'].period
	propagationData['o_tle'].period_steps
	propagationData['o_tle'].semi_major
	propagationData['o_tle'].ecc
	propagationData['o_tle'].inc
	propagationData['o_tle'].raan
	propagationData['o_tle'].argp
	assert propagationData['o_tle'].timespan is not None
	assert propagationData['o_tle'].satcat_id is not None
	assert propagationData['o_tle'].name is not None
	assert propagationData['o_tle'].gen_type is not None
	assert propagationData['o_tle'].central_body is not None
	assert propagationData['o_tle'].pos is not None
	assert propagationData['o_tle'].vel is not None
	assert propagationData['o_tle'].alt is not None
	assert propagationData['o_tle'].pos_ecef is not None
	assert propagationData['o_tle'].vel_ecef is not None
	assert propagationData['o_tle'].lat is not None
	assert propagationData['o_tle'].lon is not None
	assert propagationData['o_tle'].ecc is not None
	assert propagationData['o_tle'].inc is not None
	assert propagationData['o_tle'].semi_major is not None
	assert propagationData['o_tle'].semi_major is not None
	assert propagationData['o_tle'].raan is not None
	assert propagationData['o_tle'].argp is not None
	assert propagationData['o_tle'].TLE_epochs is not None
	assert propagationData['o_tle'].period is not None
	assert propagationData['o_tle'].period_steps is not None

	propagationData['o_tle_astro'].name
	propagationData['o_tle_astro'].satcat_id
	propagationData['o_tle_astro'].gen_type
	propagationData['o_tle_astro'].timespan
	propagationData['o_tle_astro'].TLE_epochs
	propagationData['o_tle_astro'].pos
	propagationData['o_tle_astro'].pos_ecef
	propagationData['o_tle_astro'].vel_ecef
	propagationData['o_tle_astro'].vel
	propagationData['o_tle_astro'].lat
	propagationData['o_tle_astro'].lon
	propagationData['o_tle_astro'].sun_pos
	propagationData['o_tle_astro'].moon_pos
	propagationData['o_tle_astro'].alt
	propagationData['o_tle_astro'].eclipse
	propagationData['o_tle_astro'].central_body
	propagationData['o_tle_astro'].period
	propagationData['o_tle_astro'].period_steps
	propagationData['o_tle_astro'].semi_major
	propagationData['o_tle_astro'].ecc
	propagationData['o_tle_astro'].inc
	propagationData['o_tle_astro'].raan
	propagationData['o_tle_astro'].argp
	assert propagationData['o_tle_astro'].timespan is not None
	assert propagationData['o_tle_astro'].satcat_id is not None
	assert propagationData['o_tle_astro'].name is not None
	assert propagationData['o_tle_astro'].gen_type is not None
	assert propagationData['o_tle_astro'].central_body is not None
	assert propagationData['o_tle_astro'].pos is not None
	assert propagationData['o_tle_astro'].vel is not None
	assert propagationData['o_tle_astro'].alt is not None
	assert propagationData['o_tle_astro'].pos_ecef is not None
	assert propagationData['o_tle_astro'].vel_ecef is not None
	assert propagationData['o_tle_astro'].lat is not None
	assert propagationData['o_tle_astro'].lon is not None
	assert propagationData['o_tle_astro'].ecc is not None
	assert propagationData['o_tle_astro'].inc is not None
	assert propagationData['o_tle_astro'].semi_major is not None
	assert propagationData['o_tle_astro'].semi_major is not None
	assert propagationData['o_tle_astro'].raan is not None
	assert propagationData['o_tle_astro'].argp is not None
	assert propagationData['o_tle_astro'].TLE_epochs is not None
	assert propagationData['o_tle_astro'].period is not None
	assert propagationData['o_tle_astro'].period_steps is not None
	assert propagationData['o_tle_astro'].sun_pos is not None
	assert propagationData['o_tle_astro'].moon_pos is not None
	assert propagationData['o_tle_astro'].eclipse is not None

def test_FakeTLEGenAttributes(propagationData:dict):
	'''
	Test for existance of required attributes in the orbit class
	'''

	propagationData['o_ftle'].name
	propagationData['o_ftle'].satcat_id
	propagationData['o_ftle'].gen_type
	propagationData['o_ftle'].timespan
	propagationData['o_ftle'].TLE_epochs
	propagationData['o_ftle'].pos
	propagationData['o_ftle'].pos_ecef
	propagationData['o_ftle'].vel_ecef
	propagationData['o_ftle'].vel
	propagationData['o_ftle'].lat
	propagationData['o_ftle'].lon
	propagationData['o_ftle'].sun_pos
	propagationData['o_ftle'].moon_pos
	propagationData['o_ftle'].alt
	propagationData['o_ftle'].eclipse
	propagationData['o_ftle'].central_body
	propagationData['o_ftle'].period
	propagationData['o_ftle'].period_steps
	propagationData['o_ftle'].semi_major
	propagationData['o_ftle'].ecc
	propagationData['o_ftle'].inc
	propagationData['o_ftle'].raan
	propagationData['o_ftle'].argp
	assert propagationData['o_ftle'].name is not None
	assert propagationData['o_ftle'].timespan is not None
	assert propagationData['o_ftle'].gen_type is not None
	assert propagationData['o_ftle'].central_body is not None
	assert propagationData['o_ftle'].pos is not None
	assert propagationData['o_ftle'].vel is not None
	assert propagationData['o_ftle'].alt is not None
	# TODO: include pos_ecef, vel_ecef, lat, lon once these are included in the generation
	assert propagationData['o_ftle'].ecc is not None
	assert propagationData['o_ftle'].inc is not None
	assert propagationData['o_ftle'].semi_major is not None
	assert propagationData['o_ftle'].raan is not None
	assert propagationData['o_ftle'].argp is not None
	assert propagationData['o_ftle'].TLE_epochs is not None
	assert propagationData['o_ftle'].period is not None
	assert propagationData['o_ftle'].period_steps is not None


	propagationData['o_ftle_astro'].name
	propagationData['o_ftle_astro'].satcat_id
	propagationData['o_ftle_astro'].gen_type
	propagationData['o_ftle_astro'].timespan
	propagationData['o_ftle_astro'].TLE_epochs
	propagationData['o_ftle_astro'].pos
	propagationData['o_ftle_astro'].pos_ecef
	propagationData['o_ftle_astro'].vel_ecef
	propagationData['o_ftle_astro'].vel
	propagationData['o_ftle_astro'].lat
	propagationData['o_ftle_astro'].lon
	propagationData['o_ftle_astro'].sun_pos
	propagationData['o_ftle_astro'].moon_pos
	propagationData['o_ftle_astro'].alt
	propagationData['o_ftle_astro'].eclipse
	propagationData['o_ftle_astro'].central_body
	propagationData['o_ftle_astro'].period
	propagationData['o_ftle_astro'].period_steps
	propagationData['o_ftle_astro'].semi_major
	propagationData['o_ftle_astro'].ecc
	propagationData['o_ftle_astro'].inc
	propagationData['o_ftle_astro'].raan
	propagationData['o_ftle_astro'].argp
	assert propagationData['o_ftle_astro'].name is not None
	assert propagationData['o_ftle_astro'].timespan is not None
	assert propagationData['o_ftle_astro'].gen_type is not None
	assert propagationData['o_ftle_astro'].central_body is not None
	assert propagationData['o_ftle_astro'].pos is not None
	assert propagationData['o_ftle_astro'].vel is not None
	assert propagationData['o_ftle_astro'].alt is not None
	# TODO: include pos_ecef, vel_ecef, lat, lon once these are included in the generation
	assert propagationData['o_ftle_astro'].ecc is not None
	assert propagationData['o_ftle_astro'].inc is not None
	assert propagationData['o_ftle_astro'].semi_major is not None
	assert propagationData['o_ftle_astro'].raan is not None
	assert propagationData['o_ftle_astro'].argp is not None
	assert propagationData['o_ftle_astro'].TLE_epochs is not None
	assert propagationData['o_ftle_astro'].period is not None
	assert propagationData['o_ftle_astro'].period_steps is not None
	assert propagationData['o_ftle_astro'].sun_pos is not None
	assert propagationData['o_ftle_astro'].moon_pos is not None
	assert propagationData['o_ftle_astro'].eclipse is not None

def test_AnalyticalGenAttributes(propagationData:dict):
	'''
	Test for existance of required attributes in the orbit class
	'''

	propagationData['o_analytical'].name
	propagationData['o_analytical'].satcat_id
	propagationData['o_analytical'].gen_type
	propagationData['o_analytical'].timespan
	propagationData['o_analytical'].TLE_epochs
	propagationData['o_analytical'].pos
	propagationData['o_analytical'].pos_ecef
	propagationData['o_analytical'].vel_ecef
	propagationData['o_analytical'].vel
	propagationData['o_analytical'].lat
	propagationData['o_analytical'].lon
	propagationData['o_analytical'].sun_pos
	propagationData['o_analytical'].moon_pos
	propagationData['o_analytical'].alt
	propagationData['o_analytical'].eclipse
	propagationData['o_analytical'].central_body
	propagationData['o_analytical'].period
	propagationData['o_analytical'].period_steps
	propagationData['o_analytical'].semi_major
	propagationData['o_analytical'].ecc
	propagationData['o_analytical'].inc
	propagationData['o_analytical'].raan
	propagationData['o_analytical'].argp
	assert propagationData['o_analytical'].name is not None
	assert propagationData['o_analytical'].timespan is not None
	assert propagationData['o_analytical'].gen_type is not None
	assert propagationData['o_analytical'].central_body is not None
	assert propagationData['o_analytical'].pos is not None
	assert propagationData['o_analytical'].vel is not None
	assert propagationData['o_analytical'].alt is not None
	assert propagationData['o_analytical'].ecc is not None
	assert propagationData['o_analytical'].inc is not None
	assert propagationData['o_analytical'].semi_major is not None
	assert propagationData['o_analytical'].raan is not None
	assert propagationData['o_analytical'].argp is not None
	assert propagationData['o_analytical'].period is not None
	assert propagationData['o_analytical'].period_steps is not None

	propagationData['o_analytical_astro'].name
	propagationData['o_analytical_astro'].satcat_id
	propagationData['o_analytical_astro'].gen_type
	propagationData['o_analytical_astro'].timespan
	propagationData['o_analytical_astro'].TLE_epochs
	propagationData['o_analytical_astro'].pos
	propagationData['o_analytical_astro'].pos_ecef
	propagationData['o_analytical_astro'].vel_ecef
	propagationData['o_analytical_astro'].vel
	propagationData['o_analytical_astro'].lat
	propagationData['o_analytical_astro'].lon
	propagationData['o_analytical_astro'].sun_pos
	propagationData['o_analytical_astro'].moon_pos
	propagationData['o_analytical_astro'].alt
	propagationData['o_analytical_astro'].eclipse
	propagationData['o_analytical_astro'].central_body
	propagationData['o_analytical_astro'].period
	propagationData['o_analytical_astro'].period_steps
	propagationData['o_analytical_astro'].semi_major
	propagationData['o_analytical_astro'].ecc
	propagationData['o_analytical_astro'].inc
	propagationData['o_analytical_astro'].raan
	propagationData['o_analytical_astro'].argp
	assert propagationData['o_analytical_astro'].name is not None
	assert propagationData['o_analytical_astro'].timespan is not None
	assert propagationData['o_analytical_astro'].gen_type is not None
	assert propagationData['o_analytical_astro'].central_body is not None
	assert propagationData['o_analytical_astro'].pos is not None
	assert propagationData['o_analytical_astro'].vel is not None
	assert propagationData['o_analytical_astro'].alt is not None
	assert propagationData['o_analytical_astro'].ecc is not None
	assert propagationData['o_analytical_astro'].inc is not None
	assert propagationData['o_analytical_astro'].semi_major is not None
	assert propagationData['o_analytical_astro'].raan is not None
	assert propagationData['o_analytical_astro'].argp is not None
	assert propagationData['o_analytical_astro'].period is not None
	assert propagationData['o_analytical_astro'].period_steps is not None
	assert propagationData['o_analytical_astro'].sun_pos is not None
	assert propagationData['o_analytical_astro'].moon_pos is not None
	assert propagationData['o_analytical_astro'].eclipse is not None

def test_PosListGenAttributes(propagationData:dict):
	'''
	Test for existance of required attributes in the orbit class
	'''

	propagationData['o_poslist'].name
	propagationData['o_poslist'].satcat_id
	propagationData['o_poslist'].gen_type
	propagationData['o_poslist'].timespan
	propagationData['o_poslist'].TLE_epochs
	propagationData['o_poslist'].pos
	propagationData['o_poslist'].pos_ecef
	propagationData['o_poslist'].vel_ecef
	propagationData['o_poslist'].vel
	propagationData['o_poslist'].lat
	propagationData['o_poslist'].lon
	propagationData['o_poslist'].sun_pos
	propagationData['o_poslist'].moon_pos
	propagationData['o_poslist'].alt
	propagationData['o_poslist'].eclipse
	propagationData['o_poslist'].central_body
	propagationData['o_poslist'].period
	propagationData['o_poslist'].period_steps
	propagationData['o_poslist'].semi_major
	propagationData['o_poslist'].ecc
	propagationData['o_poslist'].inc
	propagationData['o_poslist'].raan
	propagationData['o_poslist'].argp
	assert propagationData['o_poslist'].timespan is not None
	assert propagationData['o_poslist'].name is not None
	assert propagationData['o_poslist'].gen_type is not None
	assert propagationData['o_poslist'].pos is not None
	assert propagationData['o_poslist'].vel is not None

	propagationData['o_poslist_astro'].name
	propagationData['o_poslist_astro'].satcat_id
	propagationData['o_poslist_astro'].gen_type
	propagationData['o_poslist_astro'].timespan
	propagationData['o_poslist_astro'].TLE_epochs
	propagationData['o_poslist_astro'].pos
	propagationData['o_poslist_astro'].pos_ecef
	propagationData['o_poslist_astro'].vel_ecef
	propagationData['o_poslist_astro'].vel
	propagationData['o_poslist_astro'].lat
	propagationData['o_poslist_astro'].lon
	propagationData['o_poslist_astro'].sun_pos
	propagationData['o_poslist_astro'].moon_pos
	propagationData['o_poslist_astro'].alt
	propagationData['o_poslist_astro'].eclipse
	propagationData['o_poslist_astro'].central_body
	propagationData['o_poslist_astro'].period
	propagationData['o_poslist_astro'].period_steps
	propagationData['o_poslist_astro'].semi_major
	propagationData['o_poslist_astro'].ecc
	propagationData['o_poslist_astro'].inc
	propagationData['o_poslist_astro'].raan
	propagationData['o_poslist_astro'].argp
	assert propagationData['o_poslist_astro'].timespan is not None
	assert propagationData['o_poslist_astro'].name is not None
	assert propagationData['o_poslist_astro'].gen_type is not None
	assert propagationData['o_poslist_astro'].pos is not None
	assert propagationData['o_poslist_astro'].vel is not None
	assert propagationData['o_poslist_astro'].sun_pos is not None
	assert propagationData['o_poslist_astro'].moon_pos is not None
	assert propagationData['o_poslist_astro'].eclipse is not None

def test_StaticGenAttributes(propagationData:dict):
	'''
	Test for existance of required attributes in the orbit class
	'''

	propagationData['o_static'].name
	propagationData['o_static'].satcat_id
	propagationData['o_static'].gen_type
	propagationData['o_static'].timespan
	propagationData['o_static'].TLE_epochs
	propagationData['o_static'].pos
	propagationData['o_static'].pos_ecef
	propagationData['o_static'].vel_ecef
	propagationData['o_static'].vel
	propagationData['o_static'].lat
	propagationData['o_static'].lon
	propagationData['o_static'].sun_pos
	propagationData['o_static'].moon_pos
	propagationData['o_static'].alt
	propagationData['o_static'].eclipse
	propagationData['o_static'].central_body
	propagationData['o_static'].period
	propagationData['o_static'].period_steps
	propagationData['o_static'].semi_major
	propagationData['o_static'].ecc
	propagationData['o_static'].inc
	propagationData['o_static'].raan
	propagationData['o_static'].argp
	assert propagationData['o_static'].timespan is not None
	assert propagationData['o_static'].name is not None
	assert propagationData['o_static'].gen_type is not None
	assert propagationData['o_static'].pos is not None
	assert propagationData['o_static'].vel is not None

	propagationData['o_static_astro'].name
	propagationData['o_static_astro'].satcat_id
	propagationData['o_static_astro'].gen_type
	propagationData['o_static_astro'].timespan
	propagationData['o_static_astro'].TLE_epochs
	propagationData['o_static_astro'].pos
	propagationData['o_static_astro'].pos_ecef
	propagationData['o_static_astro'].vel_ecef
	propagationData['o_static_astro'].vel
	propagationData['o_static_astro'].lat
	propagationData['o_static_astro'].lon
	propagationData['o_static_astro'].sun_pos
	propagationData['o_static_astro'].moon_pos
	propagationData['o_static_astro'].alt
	propagationData['o_static_astro'].eclipse
	propagationData['o_static_astro'].central_body
	propagationData['o_static_astro'].period
	propagationData['o_static_astro'].period_steps
	propagationData['o_static_astro'].semi_major
	propagationData['o_static_astro'].ecc
	propagationData['o_static_astro'].inc
	propagationData['o_static_astro'].raan
	propagationData['o_static_astro'].argp
	assert propagationData['o_static_astro'].timespan is not None
	assert propagationData['o_static_astro'].name is not None
	assert propagationData['o_static_astro'].gen_type is not None
	assert propagationData['o_static_astro'].pos is not None
	assert propagationData['o_static_astro'].vel is not None
	assert propagationData['o_static_astro'].sun_pos is not None
	assert propagationData['o_static_astro'].moon_pos is not None

def test_dimensions(propagationData:dict):
# 	'''
# 	Test pos and vel attributes are same dimensions as timespan
# 	'''

	# From TLE
	check.equal(propagationData['o_tle'].pos.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_tle'].vel.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_tle'].pos_ecef.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_tle'].vel_ecef.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_tle'].lat.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_tle'].lon.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_tle'].alt.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_tle'].eclipse.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_tle'].TLE_epochs.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_tle_astro'].sun_pos.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_tle_astro'].moon_pos.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_tle'].semi_major.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_tle'].ecc.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_tle'].inc.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_tle'].raan.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_tle'].argp.shape[0], len(propagationData['t']))

	# From fake TLE
	check.equal(propagationData['o_ftle'].pos.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_ftle'].vel.shape[0], len(propagationData['t']))
	# TODO: include pos_ecef, vel_ecef, lat, lon once these are included in the generati']on
	check.equal(propagationData['o_ftle'].alt.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_ftle'].eclipse.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_ftle'].TLE_epochs.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_ftle_astro'].sun_pos.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_ftle_astro'].moon_pos.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_ftle'].semi_major.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_ftle'].ecc.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_ftle'].inc.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_ftle'].raan.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_ftle'].argp.shape[0], len(propagationData['t']))

	# From orbital param
	check.equal(propagationData['o_analytical'].pos.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_analytical'].vel.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_analytical'].alt.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_analytical'].eclipse.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_analytical_astro'].sun_pos.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_analytical_astro'].moon_pos.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_analytical'].semi_major.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_analytical'].ecc.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_analytical'].inc.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_analytical'].raan.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_analytical'].argp.shape[0], len(propagationData['t']))

	# From position list
	check.equal(propagationData['o_poslist'].pos.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_poslist'].vel.shape[0], len(propagationData['t']))

	# From const pos
	check.equal(propagationData['o_static'].pos.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_static'].vel.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_static_astro'].sun_pos.shape[0], len(propagationData['t']))
	check.equal(propagationData['o_static_astro'].moon_pos.shape[0], len(propagationData['t']))

@pytest.mark.filterwarnings("ignore::erfa.ErfaWarning")
def test_unsafe(propagationData:dict):
	# TLE prior to earliest zarya epoch
	prior_start_t = timespan.TimeSpan(dt.datetime(1997,1,1),'1S','1M')
	# timespan begins more than 14 days after last TLE epoch
	post_start_t = timespan.TimeSpan(dt.datetime.now() + dt.timedelta(days=30),'1S','1M')
	# timespan begins within given TLE epochs, but more than 14 days after last TLE epoch
	# needs to be earlier than 2100 for external library compatibility
	post_end_t = timespan.TimeSpan(dt.datetime(2005,6,1),'365d','34310d')

	with check.raises(exceptions.OutOfRangeError):
		orbit.Orbit.fromTLE(prior_start_t, pathlib.Path(propagationData['ISS_tle_path']))
		orbit.Orbit.fromTLE(post_start_t, pathlib.Path(propagationData['ISS_tle_path']))
		orbit.Orbit.fromTLE(post_end_t, pathlib.Path(propagationData['ISS_tle_path']))

	orbit.Orbit.fromTLE(prior_start_t, pathlib.Path(propagationData['ISS_tle_path']), unsafe=True)
	orbit.Orbit.fromTLE(post_start_t, pathlib.Path(propagationData['ISS_tle_path']), unsafe=True)
	orbit.Orbit.fromTLE(post_end_t, pathlib.Path(propagationData['ISS_tle_path']), unsafe=True)

	with check.raises(exceptions.OutOfRangeError):
		orbit.Orbit.fromPropagatedOrbitalParam(propagationData['t'], a=(6378 - 600), ecc=0, inc=45, raan=0, argp=0, mean_nu=0)
		orbit.Orbit.fromPropagatedOrbitalParam(propagationData['t'], a=(6378 - 600), ecc=0, inc=45, raan=0, argp=0, mean_nu=0)

	orbit.Orbit.fromPropagatedOrbitalParam(propagationData['t'], a=(6378 - 600), ecc=0, inc=45, raan=0, argp=0, mean_nu=0, unsafe=True)
	orbit.Orbit.fromPropagatedOrbitalParam(propagationData['t'], a=(6378 - 600), ecc=0, inc=45, raan=0, argp=0, mean_nu=0, unsafe=True)

def test_analyticalValidity():
		'''
		Tests to check pos and vel values are sensible for an orbit
		'''

		t0 = dt.datetime(2021, 1, 1, 0, 0, 1)
		t = timespan.TimeSpan(t0, '1S', '180M')
		a = 6378+600
		o = orbit.Orbit.fromAnalyticalOrbitalParam(t, a=a, ecc=0, inc=45, raan=0, argp=0, mean_nu=0)

		# Circular orbit should have the same semi-major for its duration
		check.is_true(np.all(np.isclose(np.linalg.norm(o.pos, axis=1), a)))
		# Circular orbit should have the same orbital speed for its duration
		speed = orbital_u.calcOrbitalVel(a * 1e3, np.array((a * 1e3, 0, 0)))
		check.is_true(np.all(np.isclose(np.linalg.norm(o.vel, axis=1), speed)))
