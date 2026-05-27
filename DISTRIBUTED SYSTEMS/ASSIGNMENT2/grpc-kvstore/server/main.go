package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"os"
	"strings"
	"sync"
	"time"

	pb "grpc-kvstore/proto"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

type server struct {
	pb.UnimplementedKVStoreServer
	mu        sync.RWMutex
	store     map[string]string           // Key-value deposu
	peers     map[string]pb.KVStoreClient // Diğer sunuculara (peer) gRPC istemcileri
	peerAddrs []string                    // Diğer sunucuların adres listesi
}

func (s *server) Put(ctx context.Context, kv *pb.KeyValue) (*pb.Ack, error) {
	s.mu.Lock()
	s.store[kv.Key] = kv.Value
	s.mu.Unlock()

	log.Printf("PUT key=%s, value=%s. Replicating...", kv.Key, kv.Value)

	var wg sync.WaitGroup
	errChan := make(chan error, len(s.peers))

	for addr, peer := range s.peers {
		wg.Add(1)
		go func(addr string, peer pb.KVStoreClient) {
			defer wg.Done()
			_, err := peer.Replicate(context.Background(), kv)
			if err != nil {
				log.Printf("Failed to replicate to %s: %v", addr, err)
				errChan <- fmt.Errorf("peer %s failed: %v", addr, err)
			}
		}(addr, peer)
	}

	wg.Wait()
	close(errChan)

	var allErrors []string
	for err := range errChan {
		allErrors = append(allErrors, err.Error())
	}

	if len(allErrors) > 0 {
		return nil, fmt.Errorf("replication failed on %d peers: %s",
			len(allErrors), strings.Join(allErrors, "; "))
	}

	log.Printf("Key %s replicated successfully.", kv.Key)
	return &pb.Ack{Message: "Stored and replicated"}, nil
}

func (s *server) Replicate(ctx context.Context, kv *pb.KeyValue) (*pb.Ack, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	s.store[kv.Key] = kv.Value
	log.Printf("REPLICATED key=%s, value=%s", kv.Key, kv.Value)

	return &pb.Ack{Message: "Replicated"}, nil
}

func (s *server) Get(ctx context.Context, k *pb.Key) (*pb.Value, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	val := s.store[k.Key]
	log.Printf("GET key=%s, value=%s", k.Key, val)

	return &pb.Value{Value: val}, nil
}

func (s *server) List(empty *pb.Empty, stream pb.KVStore_ListServer) error {
	s.mu.RLock()
	kvs := make(map[string]string)
	for k, v := range s.store {
		kvs[k] = v
	}
	s.mu.RUnlock()

	log.Printf("LIST request received. Streaming %d items.", len(kvs))

	for k, v := range kvs {
		if err := stream.Send(&pb.KeyValue{Key: k, Value: v}); err != nil {
			log.Printf("List stream error: %v", err)
			return err
		}
	}
	return nil
}

func main() {
	if len(os.Args) != 3 {
		log.Fatalf("Usage: %s <port> <comma_separated_peer_ports>", os.Args[0])
	}
	port := os.Args[1]
	peerAddrs := strings.Split(os.Args[2], ",")

	lis, err := net.Listen("tcp", ":"+port)
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	s := grpc.NewServer()
	kvServer := &server{
		store:     make(map[string]string),
		peers:     make(map[string]pb.KVStoreClient),
		peerAddrs: peerAddrs,
	}
	pb.RegisterKVStoreServer(s, kvServer) // Servisi kaydet

	log.Printf("Server listening at %v", lis.Addr())

	go func() {
		if err := s.Serve(lis); err != nil {
			log.Fatalf("Failed to serve: %v", err)
		}
	}()

	log.Println("Waiting 3 seconds to connect to peers...")
	time.Sleep(3 * time.Second)

	for _, peerPort := range kvServer.peerAddrs {
		addr := "localhost:" + peerPort
		conn, err := grpc.Dial(addr, grpc.WithTransportCredentials(insecure.NewCredentials()))
		if err != nil {
			log.Printf("Warning: Could not connect to peer %s: %v", addr, err)
			continue // Bir peer'a bağlanamazsa bile devam et
		}
		client := pb.NewKVStoreClient(conn)
		kvServer.peers[addr] = client
		log.Printf("Connected to peer %s", addr)
	}

	log.Println("Connected to all peers. Server is. Server is ready.")

	select {}
}
