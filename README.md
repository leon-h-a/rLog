# rLog

Many-to-many logging system

    ┌───────┐
    │ OTHER │   ┌─────┐
    └───▲───┘   │ ORM │   ┌────────┐
        │       └──▲──┘   │  CSV   │ (loggers)
        │          │      └────▲───┘
        │          │           │
        │   ┌──────┴──────┐    │
        └───┤  RECEIVER   ├────┘ (queue)
            └──────▲──────┘
                   │
                   │
                   │
                   │
            ┌──────┴──────┐
            │ GENERATORS  │
            └─────────────┘

### Receiver
Receiver is a process that dispatches handlers as subprocesses,
each implementing queue of received log requests from a single client.

### Handlers
Handler subprocesses are instantiated on newly connected clients and
are alive until socket connection is alive.
They hold socket and logger objects.

### Loggers
Hold output format definitions (table/format) as dataclass objects.

### Log requests
Each log request shall include header that contains message length,
unique source ID and output type (db write, csv log, etc)

### Protocol
SSL Sockets (?)

Request-response, client connects and receiver spawns subprocess that is
responsible for handling single client connection.

Client requests data write to specified output, spawned client checks
data integrity and writes data to requested output/s
(file, csv, db, etc).

Handler responds to client with ACK/NACK bits per requested write
action (file write might succeed but db write might fail).

### Parsing
Both generator and receiver objects must implement same parsing logic.
Messages are transported in JSON format.

### ToDo
Implement hash field in message header with timeout on response (ACK/NACK)
if hash does not match locally saved creds.

### Grafana/InfluxDB
When adding InfluxDB source to Grafana:

Auth: basic auth toggle
Basic auth details: user/pass
custom HTTP Headers:
Header: "Authorization" Value: "Token <token_string>"
Database: <bucket_name>
HTTP method: GET
Min time interval: 1s
