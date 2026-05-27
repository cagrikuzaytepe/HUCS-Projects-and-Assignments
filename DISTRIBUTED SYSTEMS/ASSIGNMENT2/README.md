# Assignment 2 — Distributed Key-Value Store with gRPC

A distributed key-value store implemented in Go using gRPC. Multiple server instances replicate writes to each other; clients can read from any node.
Part of **BBM448 – Distributed Systems**, Hacettepe University.

## Tech Stack

- Go 1.x
- gRPC (`google.golang.org/grpc`)
- Protocol Buffers (`proto3`)

## Project Structure

```
grpc-kvstore/
├── proto/
│   ├── kvstore.proto          # Service definition
│   ├── kvstore.pb.go          # Generated types
│   └── kvstore_grpc.pb.go     # Generated gRPC stubs
├── server/
│   └── main.go                # Server: Put, Get, Replicate, List
├── client/
│   └── main.go                # Interactive client
├── go.mod
└── go.sum
```

## gRPC Service

- `Put(key, value)` — writes a key and replicates to all peer servers
- `Get(key)` — returns the value for a key
- `List()` — streams all key-value pairs
- `Replicate(key, value)` — internal replication call (server-to-server)

## Prerequisites

```bash
go mod download
```

Protobuf compiler (`protoc`) is only needed if you modify `.proto` files. Generated files are already included.

## How to Run

Start two or more server instances, listing each other as peers:

```bash
# Terminal 1: server on port 50051, peer at 50052
cd grpc-kvstore && go run server/main.go 50051 50052

# Terminal 2: server on port 50052, peer at 50051
cd grpc-kvstore && go run server/main.go 50052 50051

# Terminal 3: run client
cd grpc-kvstore && go run client/main.go
```

## Key Learnings

- Implemented synchronous replication: a `Put` only succeeds after all peers acknowledge the write; partial failures are reported back to the client
- Used `sync.RWMutex` for concurrent read/write safety on the in-memory store; multiple `Get` and `List` calls can proceed in parallel
- gRPC server streaming (`List`) is more efficient than returning a large slice for potentially unbounded data sets
