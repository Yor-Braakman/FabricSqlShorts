# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "jupyter",
# META     "jupyter_kernel_name": "python3.11"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "c9a27e5e-8b02-462d-8c85-8aafe546e7d8",
# META       "default_lakehouse_name": "LH_noSchema",
# META       "default_lakehouse_workspace_id": "0256677c-f624-4061-839b-bfe45b6cad74",
# META       "known_lakehouses": []
# META     }
# META   }
# META }

# CELL ********************

# MAGIC %%configure -f 
# MAGIC {"defaultLakehouse": { "name": "LH_noSchema"}}

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

import duckdb
import pandas as pd
from deltalake import write_deltalake, DeltaTable
from deltalake.exceptions import TableNotFoundError

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

notebookutils.runtime.context

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

workspaceId = notebookutils.runtime.context['currentWorkspaceId']
currentWorkspaceName = notebookutils.runtime.context['currentWorkspaceName']
defaultLakehouseId = notebookutils.runtime.context['defaultLakehouseId']
defaultLakehouseName = notebookutils.runtime.context['defaultLakehouseName']

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

table_path = f"abfss://{currentWorkspaceName}@onelake.dfs.fabric.microsoft.com/{defaultLakehouseName}.Lakehouse/Tables/"
storage_options = {"bearer_token": notebookutils.credentials.getToken("storage"), 
                   "use_fabric_endpoint": "true"}

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

try:
    dt = DeltaTable(table_path + "meta_sources", storage_options=storage_options)
    meta_df = dt.to_pyarrow_dataset().head(1000).to_pandas()
except TableNotFoundError:
    meta_df = pd.DataFrame(columns=["data_type", "entity_name", "last_load"])
meta_data = meta_df.to_dict(orient="records")
display(meta_data)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

array_of_files = notebookutils.fs.ls(f"abfss://{workspaceId}@onelake.dfs.fabric.microsoft.com/{defaultLakehouseId}/Files/IN")
array_of_files

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

meta_index = {x["file_name"]: x["last_loaded"] for x in meta_data}
meta_index

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

for file in array_of_files:
    file_name = file.path.split('/')[-1].replace('.csv', '')
    last_loaded = meta_index.get(file_name)

    if last_loaded and int(file.modifyTime) <= int(last_loaded):
        print(f"skipping {file_name} (not modified)")
        continue
    print(f"loading {file_name}")
    df = duckdb.read_csv(file.path).df()
    write_deltalake(table_path + file_name, 
                    df, 
                    mode='overwrite', 
                    schema_mode='merge', 
                    engine='rust', 
                    storage_options=storage_options)
    meta_data.append({"file_name" : file_name, "last_loaded" : file.modifyTime})
meta_df = pd.DataFrame(meta_data)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

meta_data = {x["file_name"]: x for x in meta_data}.values()
meta_df = pd.DataFrame(meta_data)

write_deltalake(table_path + "meta_sources", 
                    meta_df, 
                    mode='overwrite', 
                    schema_mode='merge', 
                    engine='rust', 
                    storage_options=storage_options)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }
