import pytest

import dagster_testing.jobs as jobs  # noqa: F401
import dagster_testing.schedules as schedules  # noqa: F401
import dagster_testing.sensors as sensors  # noqa: F401
from dagster_testing.assets import lesson_6  # noqa: F401
from dagster_testing.definitions import defs


@pytest.fixture()
def file_output():
    return [
        {
            "City": "New York",
            "Population": "8804190",
        },
        {
            "City": "Buffalo",
            "Population": "278349",
        },
        {
            "City": "Yonkers",
            "Population": "211569",
        },
    ]


# Asset Checks
def test_non_negative():
    asset_check_pass = lesson_6.non_negative(10)
    assert asset_check_pass.passed
    asset_check_fail = lesson_6.non_negative(-10)
    assert not asset_check_fail.passed


# Jobs
def test_jobs():
    pass


def test_job_selection():
    pass



# Schedules
def test_schedule():
    pass


# Sensors
def test_sensors():
    pass


def test_sensor_skip():
    pass


def test_sensor_run():
    pass


# Definitions
# Test the definitions of assets, jobs, schedules, and sensors
def test_def():
    assert defs.get_assets_def("total_population")
    assert defs.get_job_def("jobs_config")
    assert defs.get_schedule_def("my_schedule")
    assert defs.get_sensor_def("my_sensor")


def test_def_objects():
    pass

def test_job_config():
    assert (
        jobs.my_job_configured.config["ops"]["population_file_config"]["config"]["path"]
        == "dagster_testing_tests/data/test.csv"
    )


# Schedules
def test_schedule():
    assert schedules.my_schedule
    assert schedules.my_schedule.cron_schedule == "0 0 5 * *"
    assert schedules.my_schedule.job == jobs.my_job
