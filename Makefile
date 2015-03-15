LDFLAGS += -L/usr/local/lib -lgrpc++_unsecure -lgrpc -lgpr -lprotobuf -lpthread -ldl -lgflags -pthread
LIBRARY_PATH = /usr/local/lib

GRPC_CPP_PLUGIN = grpc_cpp_plugin
GRPC_CPP_PLUGIN_PATH ?= `which $(GRPC_CPP_PLUGIN)`

client: service client.cc
	g++ -DNDEBUG -std=c++11 -O3 -o ./client service.o client.cc $(LDFLAGS)

server: spooky_hash service server.cc
	g++ -DNDEBUG -std=c++11 -O3 -o ./server third_party/spooky.o service.o server.cc $(LDFLAGS) 

service: service_proto
	g++ -DNDEBUG -c -std=c++11 -o ./service.o SpookyService.pb.cc

spooky_hash : third_party/SpookyV2.h third_party/SpookyV2.cpp
	g++ -c -O3 -o ./third_party/spooky.o third_party/SpookyV2.cpp

service_proto: SpookyService.proto
	protoc --cpp_out=. --grpc_out=. --plugin=protoc-gen-grpc=$(GRPC_CPP_PLUGIN_PATH) SpookyService.proto
	
clean:
	rm SpookyService.pb.cc SpookyService.pb.h third_party/spooky.o server client service.o
