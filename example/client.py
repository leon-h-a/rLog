import time
from rLog.client.client_basic import ClientBasic

cli = ClientBasic(
    client_id="test_client",
    host="172.104.155.142",
    port=9898
)
cli.connect()

resp = cli.send({
    "streams": ["csv", "influx"],
    "filename": cli.cli_id,
    "telemetry": {
        "ts": time.time(),
        "temperature": 23,
        "humidity": 53
    }
})
