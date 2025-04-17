from dagster import Definitions,load_assets_from_package_module 

from dagster_test import assets
# from dagster_test.assets import assets

defs = load_assets_from_package_module(assets,group_name="assets")