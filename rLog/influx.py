from random import randint
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


# token = os.environ.get("INFLUXDB_TOKEN")
token = "QhjMd-f0cPHEZTdPxy_0f1VBH0Hz01fgf5goLFGdBLPdEqmR9XSD1t6pcfV1elbZs3EWyFBOSsMz5amu7fYOjw=="

org = "test"
url = "http://192.168.1.107:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="test_bucket"

write_api = client.write_api(write_options=SYNCHRONOUS)

# for value in range(20):
while True:
    point = (
        Point("measurement1")
        .tag("tagname1", "tagvalue1")
        #.field("field1", value)
        .field("field1", randint(19, 32))
        )
    write_api.write(bucket=bucket, org="test", record=point)
    time.sleep(1) # separate points by 1 second
