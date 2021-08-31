import logging
import os
import json

from azure.kusto.data import KustoClient, KustoConnectionStringBuilder, ClientRequestProperties 
from azure.kusto.data.helpers import dataframe_from_result_table
import pandas as pd
import matplotlib
from datetime import datetime
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import matplotlib.pyplot as plt
import tempfile
import base64

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    query = req_body.get('query')
    cluster = req_body.get('cluster')
    database = req_body.get('database')

    client_id = os.getenv('CLIENT_ID')
    tenant_id = os.getenv('TENANT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(cluster, client_id, client_secret, tenant_id)
    client = KustoClient(kcsb)
   
    response = client.execute(database, query)
    df = dataframe_from_result_table(response.primary_results[0])

    telemetry_values = df['telemetry_series'][0]
    event_times = df['event_time'][0]
    true_anomalies = df['true_anomalies'][0]

    dates = matplotlib.dates.date2num([datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f0Z') for x in df['event_time'][0]])

    plot_anomalies = []
    plot_dates = []

    for idx, anomaly in enumerate(true_anomalies):
        if anomaly!=0:
            plot_anomalies.append(telemetry_values[idx])
            plot_dates.append(dates[idx])

    fig, ax = plt.subplots(figsize= (13,6.5))
    ax.plot_date(dates,df['telemetry_series'][0], 'black', lw=1)
    
    ax.set_xlim(dates[0]-.0005, dates[-1]+ 0.0005)
    ax.fmt_xdata = DateFormatter('% Y-% m-% d % H:% M:% S')
    fig.autofmt_xdate()
    ax.plot(plot_dates, plot_anomalies, 'red', lw=0, ms=7, marker='o')
    plt.title('Anomalies Detected')

    tempdir = tempfile.gettempdir()
    temp_path = os.path.join(tempdir, 'output.jpg')

    plt.savefig(temp_path)
    b64_img_string = base64.b64encode(open(temp_path, 'rb').read()).decode()
    os.remove(temp_path)

    return func.HttpResponse(b64_img_string, status_code=200)
