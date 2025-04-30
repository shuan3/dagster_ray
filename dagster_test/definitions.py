import importlib
import os
from dagster import Definitions, fs_io_manager, load_assets_from_package_module
from dagster_test import assets
from dagster_test.utils.s3 import s3
import yaml
import dagster as dg

# Function to dynamically import a class or function
def import_from_string(import_path: str):
    module_name, class_name = import_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)

# Function to build ETL job
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

# def build_etl_job(
#     s3_resource: str,
#     bucket: str,
#     source_object: str,
#     target_object: str,
#     sql: str,
#     handler: str,
# ) -> dg.Definitions:
#     # Dynamically import the handler class or function
#     handler_class = import_from_string(handler)

#     @dg.asset(name=f"etl_job_{bucket}_{source_object}_{target_object}")
#     def etl_asset(context):
#         print("Building ETL job...")
#         print(f"Bucket: {bucket}")
#         print(f"Source Object: {source_object}")
#         print(f"Target Object: {target_object}")
#         print(f"SQL: {sql}")
#         # Use the handler class or function
#         handler_instance = handler_class()
#         handler_instance.handle(bucket, source_object, target_object, sql)

#     return dg.Definitions(assets=[etl_asset])

# Function to load ETL jobs from a single YAML file
# Function to load ETL jobs from a single YAML file
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

# Function to load ETL jobs from all YAML files in a folder
def load_etl_jobs_from_folder(folder_path: str) -> dg.Definitions:
    defs = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".yaml"):
            yaml_path = os.path.join(folder_path, file_name)
            defs.append(load_etl_jobs_from_yaml(yaml_path))
    return dg.Definitions.merge(*defs)


# Combine all Definitions into a single object
defs = Definitions.merge(
    Definitions(assets=load_assets_from_package_module(assets, group_name="assets"), resources={"my_resource": fs_io_manager}),
    load_etl_jobs_from_folder("dagster_test/yaml_asset"),
    # Definitions( assets=dg.load_assets_from_package_module(assets), resources={"my_resource": MyResource(foo="bar")}, )

)