from unittest.mock import Mock, patch  # noqa: F401

import dagster as dg  # noqa: F401
import pytest

from dagster_testing.assets import lesson_4  # noqa: F401


@pytest.fixture
def example_response():
    return {
        "cities": [
            {
                "city_name": "New York",
                "city_population": 8804190,
            },
            {
                "city_name": "Buffalo",
                "city_population": 278349,
            },
        ],
    }


@pytest.fixture
def example_response2():
    return {
        "cities": [
            {
                "city": "New York",
                "population": 8804190,
            },
            {
                "city": "Buffalo",
                "population": 278349,
            },
        ],
    }

@pytest.fixture
def api_output():
    return [
        {
            "city": "New York",
            "population": 8804190,
        },
        {
            "city": "Buffalo",
            "population": 278349,
        },
    ]


@pytest.fixture
def fake_city():
    return {
        "city": "Fakestown",
        "population": 42,
    }
# use patch decorator to state which part will be replaced by the mock.
# The mock will replace the requests.get method in the lesson_4 module.
# This allows us to control the behavior of the requests.get method during the test.
# The mock will return a predefined response when called, simulating the behavior of the actual API.
# This is useful for testing the function without making actual API calls.
# The test will check if the function correctly processes the mocked response and returns the expected output.
@patch("requests.get")
def test_state_population_api(mock_get, example_response2):
    # Mock the API response
    mock_response = Mock()
    mock_response.json.return_value = example_response2
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    print(mock_response.json.return_value)

    result = lesson_4.state_population_api()
    assert len(result) == 2
    # print(result["cities"][0])
    # assert result == example_response
    # assert result[0]["population"] == example_response["cities"][0]["city_population"]


@patch("requests.get")    
def test_state_population_api_resource_mock(mock_get, example_response):
    # Mock the API response 
    mock_response=Mock()
    mock_response.json.return_value = example_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result=lesson_4.state_population_api_resource(
        lesson_4.StatePopulation()  )
    assert len(result) == 2
    assert result[0]["city"] == example_response["cities"][0]["city_name"]
    assert result[0]["population"] == example_response["cities"][0]["city_population"]

# The test checks if the function correctly processes the mocked response and returns the expected output.
# This is useful for testing the function without making actual API calls.  


def test_state_population_api_assets():
    pass


def test_state_population_api_assets_config():
    pass

# @patch("requests.get")
def test_state_population_api_mocked_resource(fake_city):
    # Mock the resource to return a fake city
    mocked_resource=Mock()
    mocked_resource.get_cities.return_value = [fake_city]
    result=dg.materialize(
       assets=[lesson_4.state_population_api_resource_config,
        lesson_4.total_population_resource_config,] ,
        
    resources={"state_population_resource": mocked_resource},
    run_config=dg.RunConfig(
        {"state_population_api_resource_config": lesson_4.StateConfig(name="ny")},
        # This is the configuration for the state_population_api_resource_config asset.
        # "state_population_api_resource_config": {"config": {"name": "ny"}},
    ),
    )
    assert result.success
    assert result.output_for_node("state_population_api_resource_config")==[fake_city]
    assert result.output_for_node("total_population_resource_config")==42
    # assert len(result) == 1
    # assert result[0].city == fake_city["city"]
    # assert result[0].population == fake_city["population"]

def test_state_population_api_assets_mocked_resource():
    pass
