from datetime import datetime, timedelta, timezone

from influxdb_client import InfluxDBClient
from matplotlib import pyplot as plt

from config import ORG, TOKEN_INTERNAL_READ, TOKEN_PUBLIC_READ, URL_INTERNAL, URL_PUBLIC

client_public = InfluxDBClient(url=URL_PUBLIC, token=TOKEN_PUBLIC_READ, org=ORG)
client_internal = InfluxDBClient(url=URL_INTERNAL, token=TOKEN_INTERNAL_READ, org=ORG)


start_time = (datetime.now(tz=timezone.utc) - timedelta(days=7)).strftime(
    "%Y-%m-%dT%H:%M:%SZ"
)
stop_time = (datetime.now(tz=timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")


bucket = "chmi_data"

station_query = f"""
    from(bucket: "{bucket}")
    |> range(start: {start_time}, stop: {stop_time})
    |> filter(fn: (r) => r["_measurement"] == "SRA10M")
    |> filter(fn: (r) => r["_field"] == "H3CHTU01")
"""


public_query_api = client_public.query_api()

tables = public_query_api.query(station_query)


time = []
rainfall = []

for table in tables:
    for record in table.records:
        time.append(record.get_time())
        rainfall.append(record.get_value())


plt.figure(figsize=(10, 5))
plt.plot(time, rainfall)
plt.xlabel("Cas")
plt.ylabel("Srazky [mm]")
plt.show()


cml_bucket = "realtime_cbl"

temp_query = f"""
    from(bucket: "realtime_cbl")
    |> range(start: {start_time}, stop: {stop_time})
    |> filter(fn: (r) => r["_measurement"] == "1s10")
    |> filter(fn: (r) => r["_field"] == "Teplota")
    |> filter(fn: (r) => r["agent_host"] == "10.126.1.179" or r["agent_host"] == "10.126.1.180")
    |> aggregateWindow(every: 10m, fn: mean)
    |> yield(name: "mean")
    """.strip()

internal_query_api = client_internal.query_api()
tables = internal_query_api.query(temp_query)


temp_data_by_host = {}

for table in tables:
    for record in table.records:
        host = record.values.get("agent_host")
        if host not in temp_data_by_host:
            temp_data_by_host[host] = {"time": [], "temperature": []}
        temp_data_by_host[host]["time"].append(record.get_time())
        temp_data_by_host[host]["temperature"].append(record.get_value())


plt.figure(figsize=(10, 5))
for host, data in temp_data_by_host.items():
    plt.plot(data["time"], data["temperature"], label=f"Teplota {host}")

plt.xlabel("Cas")
plt.ylabel("Teplota [°C]")
plt.legend()
plt.show()
