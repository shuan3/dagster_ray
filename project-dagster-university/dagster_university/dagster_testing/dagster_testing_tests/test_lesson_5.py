from contextlib import contextmanager
from pathlib import Path
import subprocess

import dagster as dg
import psycopg2
import pytest
from dagster_snowflake import SnowflakeResource

from dagster_testing.assets import lesson_5

from .fixtures import docker_compose  # noqa: F401
import time


@pytest.fixture(scope="session",autouse=True)
def docker_compoase():
    file_path=Path(__file__).parent.parent / "docker-compose.yml"
    subprocess.run(
        ["docker-compose", "-f", str(file_path), "up", "-d"],
        check=True,
        capture_output=True,
    )
    max_retries=5
    for i in range(max_retries):
        result=subprocess.run(
            ["docker", "exec", "postgresql", "pg_isready"],
            capture_output=True,)
        if result.returncode==0:
            break
        time.sleep(5)

@pytest.fixture
def query_output_ny():
    return [
        ("New York", 8804190),
        ("Buffalo", 278349),
    ]


@pytest.fixture
def query_output_ca():
    return [
        ("Los Angeles", 3898747),
    ]


@pytest.fixture
def postgres_resource():
    return PostgresResource(
        host="localhost",
        user="test_user",
        password="test_pass",
        database="test_db",
    )


class PostgresResource(dg.ConfigurableResource):
    user: str
    password: str
    host: str
    database: str

    def _connection(self):
        return psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database,
        )

    @contextmanager
    def get_connection(self):
        yield self._connection()


# Snowflake not configured
@pytest.mark.skip
def test_snowflake_staging():
    snowflake_staging_resource = SnowflakeResource(
        account=dg.EnvVar("SNOWFLAKE_ACCOUNT"),
        user=dg.EnvVar("SNOWFLAKE_USERNAME"),
        password=dg.EnvVar("SNOWFLAKE_PASSWORD"),
        database="STAGING",
        warehouse="STAGING_WAREHOUSE",
    )

    lesson_5.state_population_database(snowflake_staging_resource)


def test_state_population_database():
    postgres_resource = PostgresResource(
        host="localhost",
        user="test_user",
        password="test_pass",
        database="test_db",
    )

    result=lesson_5.state_population_database(postgres_resource)
    assert result == [
        ("New York", 8804190),
        ("Buffalo", 278349),
    ]



def test_total_population_database():
    pass
    # postgres_resource = PostgresResource(
    #     host="localhost",
    #     user="test_user",
    #     password="test_pass",
    #     database="test_db",
    # )
    # result=lesson_5.total_population_database(postgres_resource)
    # assert result == 9082539



def test_assets(docker_compose, postgres_resource, query_output_ny):
    result=dg.materialize(
        assets=[lesson_5.state_population_database, 
                lesson_5.total_population_database],
        resources={"database": postgres_resource},

    )
    assert result.success
    assert result.output_for_node("state_population_database") == query_output_ny
    assert result.output_for_node("total_population_database") == 9082539