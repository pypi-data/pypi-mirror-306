import os
from moto import mock_aws
from dotenv import load_dotenv, find_dotenv
from water_column_sonar_processing.cruise.create_empty_zarr_store import CreateEmptyZarrStore


#######################################################
def setup_module():
    print('setup')

    env_file = find_dotenv('.env-test')
    # env_file = find_dotenv('.env-prod')
    load_dotenv(dotenv_path=env_file, override=True)


def teardown_module():
    print('teardown')

TEMPDIR = "/tmp"

#######################################################
@mock_aws
def test_create_empty_zarr_store(tmp_path=TEMPDIR):
    # temporary_directory = str(tmp_path)
    temporary_directory = str(tmp_path)

    cruise_name = "HB0706A" # HB0706

    # TODO:
    #  [1] load dynamodb
    #  [2] create empty bucket
    create_empty_zarr_store = CreateEmptyZarrStore()
    create_empty_zarr_store.create_cruise_level_zarr_store(
        ship_name="Henry_B._Bigelow",
        cruise_name=cruise_name,
        sensor_name="EK60",
        table_name="r2d2-dev-echofish-EchoFish-File-Info",
    )

    assert os.path.exists(f"{temporary_directory}/{cruise_name}.zarr")


#######################################################
#######################################################
# april 9th, 2024, last run of all henry bigelow cruises for carrie's presentation
#    cruises = [
#       "HB0802",
        # "HB0803",
        # "HB0805",
        # "HB0807",
        # "HB0901",
        # "HB0902",
        # "HB0904",
        # "HB0905",
        # "HB1002",
        # "HB1006",
        # "HB1102",
        # "HB1103",
        # "HB1105",
        # "HB1201",
        # "HB1206",
        # "HB1301",
        # "HB1303",
        # "HB1304",
        # "HB1401",
        # "HB1403",
        # "HB1405",
        # "HB1501",
        # "HB1502",
        # "HB1503",
        # "HB1506",
        # "HB1507",
        # "HB1601",
        # "HB1603",
        # "HB1604",
        # "HB1701",
        # "HB1702",
        # "HB1801",
        # "HB1802",
        # "HB1803",
        # "HB1804",
        # "HB1805",
        # "HB1806",
        # "HB1901",
        # "HB1902",
        # "HB1903",
        # "HB1906",
        # "HB1907",
        # "HB2001",
#    ]
#######################################################