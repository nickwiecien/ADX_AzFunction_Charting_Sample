# ADX_AzFunction_Charting_Sample

This project contains code for an Azure Function which executes a user-provided query against Azure Data Explorer (ADX), generates an anomaly chart with Matplotlib, and returns as a base64-encoded byte string. This function was developed specifically for identifying anomalies in time-series data using a custom approach that finds anomalous measurements (identified as such using the series_decompose_anomalies() function in ADX) which fall outside of a user specified range. This function allows rapid creation of custom anomaly charts which can be consumed as part of an automated anomaly detection workflow.

![Sample Anomaly Chart](img/anomaly_chart.jpg?raw=true "ADX Anomaly Chart")

## Environment Setup
Before running this project, create a `local.settings.json` file in the root directory. This file needs to have the following entries under the `values` section:

| Key                                 | Value                                    |
|-------------------------------------|------------------------------------------|
| AzureWebJobsStorage                 | The connection string to the storage account used by the Functions runtime.  To use the storage emulator, set the value to UseDevelopmentStorage=true |
| FUNCTIONS_WORKER_RUNTIME            | Set this value to `python` as this is a python Function App |
| CLIENT_ID | Client ID belonging to a service principal that has been granted access to the target ADX database. |
| CLIENT_SECRET     | Client Secret belonging to the service principal referenced above. |
| TENANT_ID     | Tenant ID belonging to the service principal referenced above. |

For more instructions on configuring service principal access to ADX [please review the following document](https://docs.microsoft.com/en-us/azure/data-explorer/manage-database-permissions).

For details on configuring either a local or cloud development environment for python Function Apps, [please refer to the developer guide here](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python).

When deploying this code to a Function App in Azure it is recommended to store sensitive keys and secrets in Azure Key Vault, and then reference these as environment variables in your app configuration. [See this document for more details](https://docs.microsoft.com/en-us/azure/app-service/app-service-key-vault-references).