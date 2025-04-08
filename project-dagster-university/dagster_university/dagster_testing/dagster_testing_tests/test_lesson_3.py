from pathlib import Path  # noqa: F401

import pytest
import yaml  # noqa: F401
from dagster._core.errors import DagsterTypeCheckDidNotPass  # noqa: F401

from dagster_testing.assets import lesson_3
import dagster as dg

@pytest.fixture()
def config_file():
    file_path = Path(__file__).absolute().parent / "data/test.csv"
    return lesson_3.FilepathConfig(path=file_path.as_posix())


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


@pytest.fixture()
def file_example_output():
    return [
        {
            "City": "Example 1",
            "Population": "4500000",
        },
        {
            "City": "Example 2",
            "Population": "3000000",
        },
        {
            "City": "Example 3",
            "Population": "1000000",
        },
    ]


@pytest.fixture()
def file_population():
    return 9294108


def test_state_population_file():
    pass


def test_total_population():
    pass


def test_func_wrong_type():
    assert lesson_3.func_wrong_type() == 2


def test_wrong_type_annotation_error():
    pass


def test_assets():
    pass


def test_state_population_file_config():
    pass


def test_state_population_file_config_fixture_1():
    pass


def test_state_population_file_config_fixture_2():
    pass


def test_assets_config():
    pass


def test_assets_config_yaml():
    pass


def test_state_population_file_logging():
    pass


def test_assets_context():
    pass


def test_partition_asset_number():
    print("test_partition_asset_number")
    pass


def test_assets_partition():
    pass


class Test_dagster_testing:
    def test_dagster_testing(self):
        assert lesson_3.dagster_testing() == 2
        print("Test Completed")

    # def test_dagster_testing_wrong_type(self):
    #     with pytest.raises(DagsterTypeCheckDidNotPass):
    #         lesson_3.dagster_testing_wrong_type()

    def test_total_population(self):
        state_population=[
          {  "City": "New York",
            "Population": "8804190"},
            {"City": "Buffalo","Population": "278349"},
            {"City": "Yonkers","Population": "211569"}
        ]
        assert lesson_3.total_population(state_population) == 9294108
        print("Test Completed again")
        
    def test_assets(self):
        #see logging of dagster logs as the test output
        _assets=[
            lesson_3.state_population_file,
            lesson_3.total_population,
        ]
        result=dg.materialize(_assets)
        assert result.success