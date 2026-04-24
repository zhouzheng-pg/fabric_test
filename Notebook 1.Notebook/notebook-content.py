# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "jupyter",
# META     "jupyter_kernel_name": "python3.12"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "4018dcb7-aeb5-4c63-9f27-562c2a8d4f61",
# META       "default_lakehouse_name": "ODS",
# META       "default_lakehouse_workspace_id": "11c3d7b1-fce2-4aaf-87c6-b0e9393142ae",
# META       "known_lakehouses": [
# META         {
# META           "id": "4018dcb7-aeb5-4c63-9f27-562c2a8d4f61"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

import requests,json
import duckdb
import polars as pl
from deltalake import write_deltalake

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# # json to file

# CELL ********************

start_date = "2026-04-01"
end_date   = "2026-04-07"

url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&endtime={end_date}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    data = data['features']

    file_path = f"/lakehouse/default/Files/{start_date}_earthquake_data.json"

    with open(file_path,'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data successfully saved to {file_path}")
else:
    print("Failed to fetch data. Status code:", response.status_code)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# # duckdb query

# CELL ********************

duckdb.sql("""
    DESCRIBE
    from read_json("/lakehouse/default/Files/2026-04-01_earthquake_data.json")
""").df()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

duckdb.sql("""
    select unnest(f,recursive:= true)
    from read_json("/lakehouse/default/Files/2026-04-01_earthquake_data.json") as f
    LIMIT 5
""").pl()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# # df write to table

# CELL ********************

pl.read_csv("https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv").head(5)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

import pandas as pd

df = pd.read_csv("https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv")

table_path = "abfss://FabricTest@onelake.dfs.fabric.microsoft.com/ODS.Lakehouse/Tables/dbo/taxi_zone_pandas"

write_deltalake(table_path,df
    ,mode="overwrite"
    ,schema_mode='overwrite'
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

df = pl.read_csv("https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv")

df.write_delta("abfss://FabricTest@onelake.dfs.fabric.microsoft.com/ODS.Lakehouse/Tables/dbo/taxi_zone_pl",
    mode="overwrite",
    delta_write_options={"schema_mode": "overwrite"}
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# # 

# MARKDOWN ********************

# # duckdb write to table

# CELL ********************

data = duckdb.sql("""
    select * 
    from "https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv"
""").arrow()

table_path = "abfss://FabricTest@onelake.dfs.fabric.microsoft.com/ODS.Lakehouse/Tables/dbo/taxi_zone_duck"

write_deltalake(
    table_path,
    data,
    mode="overwrite",
    schema_mode='overwrite'
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# # read delta table

# CELL ********************

duckdb.sql("""
    select * 
    from delta_scan("/lakehouse/default/Tables/dbo/taxi_zone_duck")
    LIMIT 5
""").pl()

# abfss://11c3d7b1-fce2-4aaf-87c6-b0e9393142ae@onelake.dfs.fabric.microsoft.com/4018dcb7-aeb5-4c63-9f27-562c2a8d4f61/Tables/dbo/taxi_zone
# https://onelake.dfs.fabric.microsoft.com/11c3d7b1-fce2-4aaf-87c6-b0e9393142ae/4018dcb7-aeb5-4c63-9f27-562c2a8d4f61/Tables/dbo/taxi_zone

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }
