# Dagster University

Welcome to [Dagster University](https://courses.dagster.io/). This contains all the courses offered by Dagster. Within each project you will find the starting point for each project as alongside the completed code for each lesson. Refer to the `README.md` of the particular course for more details.

| Course Directory | Course Page |
|-------------|-------------|
| [`Dagster Essentials`](dagster_university/dagster_essentials/README.md) | [Dagster Essentials Course](https://courses.dagster.io/courses/dagster-essentials) |
| [`Dagster & dbt`](dagster_university/dagster_and_dbt/README.md) | [Dagster + dbt Course](https://courses.dagster.io/courses/dagster-dbt) |
| [`Testing with Dagster`](dagster_university/dagster_testing/README.md) | [Testing with Dagster Course](https://courses.dagster.io/courses/dagster-testing) |



git clone git@github.com:dagster-io/project-dagster-university.git
cd project-dagster-university/dagster_university/dagster_testing/
uv sync
python -m venv .venv
virtualenv .venv
source .venv/Scripts/activate
pip install -e ".[dev]"

pytest 'd:/Github/dagster_ray/project-dagster-university/dagster_university/dagster_testing/dagster_testing_tests/test_lesson_3.py'
# Check priint out in the class
 pytest -rP 'd:/Github/dagster_ray/project-dagster-university/dagster_university/dagster_testing/dagster_testing_tests/test_lesson_3.py'