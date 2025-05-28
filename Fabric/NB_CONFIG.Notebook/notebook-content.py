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
# META       "default_lakehouse_workspace_id": "0256677c-f624-4061-839b-bfe45b6cad74"
# META     }
# META   }
# META }

# CELL ********************

# MAGIC %%configure -f
# MAGIC {
# MAGIC     "vCores": 2, 
# MAGIC     "defaultLakehouse": {  
# MAGIC         "name": "<lakehouse-name>",
# MAGIC         "id": "<(optional) lakehouse-id>",
# MAGIC         "workspaceId": "<(optional) workspace-id-that-contains-the-lakehouse>"
# MAGIC     },
# MAGIC     "mountPoints": [
# MAGIC         {
# MAGIC             "mountPoint": "/myMountPoint",
# MAGIC             "source": "abfs[s]://<file_system>@<account_name>.dfs.core.windows.net/<path>"
# MAGIC         },
# MAGIC         {
# MAGIC             "mountPoint": "/myMountPoint1",
# MAGIC             "source": "abfs[s]://<file_system>@<account_name>.dfs.core.windows.net/<path1>"
# MAGIC         },
# MAGIC     ],
# MAGIC }

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# vCores: Recommended values: [4, 8, 16, 32, 64], Fabric will allocate matched memory according to the specified vCores.
# 
# defaultLakehouse will override the default Lakehouse if it was already set on the notebook!  
#  - pick either id or lakehouse name
#  - You can modify the workspace ID if this lakehouse is in another workspace
