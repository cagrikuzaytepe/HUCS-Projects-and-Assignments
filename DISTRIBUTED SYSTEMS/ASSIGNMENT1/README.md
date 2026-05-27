# Assignment 1 — HTTP Commit Log Server

A simple in-memory commit log server exposed over HTTP. Supports appending records, reading by offset, listing all records, and clearing the log.
Part of **BBM448 – Distributed Systems**, Hacettepe University.

## Tech Stack

- Go 1.x
- `gorilla/mux` (HTTP router)

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/` | Append a record, returns offset |
| GET | `/` | Read a record by offset |
| GET | `/records` | List all records |
| DELETE | `/records` | Clear the log |

## Prerequisites

```bash
go mod download
```

## How to Run

```bash
go run http.go
```

The server starts on the address configured in `main` (default `:8080`). Use `curl` or any HTTP client to interact with the endpoints.

```bash
# Append a record
curl -X POST localhost:8080 -d '{"record": {"value": "aGVsbG8="}}'

# Read at offset 0
curl -X GET localhost:8080 -d '{"offset": 0}'

# List all
curl localhost:8080/records
```

## Key Learnings

- Built a thread-safe in-memory log using a mutex-protected slice; offset is the index into the slice
- Used `gorilla/mux` for method-based routing, decoupling HTTP handling from the log logic
- Implemented produce/consume semantics, which is the foundation of distributed log systems like Apache Kafka
