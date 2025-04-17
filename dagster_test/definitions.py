from dagster import Definitions, load_assets_from_package_module
from dagster_test import assets
from dagster_test.utils.s3 import s3
import yaml
import dagster as dg

# Function to build ETL job
def build_etl_job(
    s3_resource: str,
    bucket: str,
    source_object: str,
    target_object: str,
    sql: str,
) -> dg.Definitions:
    @dg.asset(name=f"etl_job_{bucket}_{source_object}_{target_object}")
    def etl_asset(context):
        print("Building ETL job...")
        print(f"Bucket: {bucket}")
        print(f"Source Object: {source_object}")
        print(f"Target Object: {target_object}")
        print(f"SQL: {sql}")
    return dg.Definitions(assets=[etl_asset])

# Function to load ETL jobs from YAML
def load_etl_jobs_from_yaml(yaml_path: str) -> dg.Definitions:
    config = yaml.safe_load(open(yaml_path))
    s3_resource = s3().S3Resource(
        aws_access_key_id=config["aws"]["access_key_id"],
        aws_secret_access_key=config["aws"]["secret_access_key"],
    )
    defs = []
    for job_config in config["etl_jobs"]:
        defs.append(
            build_etl_job(
                s3_resource=s3_resource,
                bucket=job_config["bucket"],
                source_object=job_config["source"],
                target_object=job_config["target"],
                sql=job_config["sql"],
            )
        )
    return dg.Definitions.merge(*defs)

# Combine all Definitions into a single object
defs = Definitions.merge(
    Definitions(assets=load_assets_from_package_module(assets, group_name="assets")),
    load_etl_jobs_from_yaml("dagster_test/yaml_asset/test1.yaml"),
)