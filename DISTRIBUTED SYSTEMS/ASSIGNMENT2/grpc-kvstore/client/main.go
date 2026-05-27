package main

import (
	"bufio"
	"context"
	"fmt"
	"io"
	"log"
	"os"
	"strings"
	"time"

	pb "grpc-kvstore/proto"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {
	if len(os.Args) != 2 {
		log.Fatalf("Usage: %s <server_port>", os.Args[0])
	}
	port := os.Args[1]
	addr := "localhost:" + port

	conn, err := grpc.Dial(addr, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("Did not connect: %v", err)
	}
	defer conn.Close()

	client := pb.NewKVStoreClient(conn)

	log.Printf("Connected to server at %s", addr)

	runCLI(client)
}

func runCLI(client pb.KVStoreClient) {
	scanner := bufio.NewScanner(os.Stdin)
	fmt.Println("Commands: put <key> <value> / get <key> / list / exit")

	for {
		fmt.Print("> ")
		if !scanner.Scan() {
			break
		}
		line := scanner.Text()
		parts := strings.Fields(line)

		if len(parts) == 0 {
			continue
		}

		cmd := parts[0]

		ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()

		switch cmd {
		case "put":
			if len(parts) != 3 {
				fmt.Println("Usage: put <key> <value>")
				continue
			}
			key, value := parts[1], parts[2]
			ack, err := client.Put(ctx, &pb.KeyValue{Key: key, Value: value})
			if err != nil {
				log.Printf("Could not put: %v", err)
			} else {
				fmt.Println(ack.Message)
			}

		case "get":
			if len(parts) != 2 {
				fmt.Println("Usage: get <key>")
				continue
			}
			key := parts[1]
			val, err := client.Get(ctx, &pb.Key{Key: key})
			if err != nil {
				log.Printf("Could not get: %v", err)
			} else {
				fmt.Printf("%s = %s\n", key, val.Value)
			}

		case "list":
			if len(parts) != 1 {
				fmt.Println("Usage: list")
				continue
			}
			stream, err := client.List(ctx, &pb.Empty{})
			if err != nil {
				log.Fatalf("Could not list: %v", err)
			}
			for {
				kv, err := stream.Recv()
				if err == io.EOF {
					break
				}
				if err != nil {
					log.Fatalf("List stream error: %v", err)
				}
				fmt.Printf("%s = %s\n", kv.Key, kv.Value)
			}

		case "exit":
			return

		default:
			fmt.Println("Unknown command. Commands: put <key> <value> / get <key> / list / exit")
		}
	}

	if err := scanner.Err(); err != nil {
		log.Printf("Scanner error: %v", err)
	}
}
