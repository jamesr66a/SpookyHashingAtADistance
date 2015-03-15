LDFLAGS += -L/usr/local/lib -lgrpc++_unsecure -lgrpc -lgpr -lprotobuf -lpthread -ldl
LIBRARY_PATH = /usr/local/lib

GRPC_CPP_PLUGIN = grpc_cpp_plugin
GRPC_CPP_PLUGIN_PATH ?= `which $(GRPC_CPP_PLUGIN)`

client: service_proto client.cc
	g++ -std=c++11 -O3 -o ./client SpookyService.pb.cc client.cc $(LDFLAGS)

server: spooky_hash service_proto server.cc
	g++ -std=c++11 -O3 -o ./server spooky.o SpookyService.pb.cc server.cc $(LDFLAGS) 

spooky_hash : SpookyV2.h SpookyV2.cpp
	g++ -c -O3 -o ./spooky.o SpookyV2.cpp

service_proto: SpookyService.proto
	protoc --cpp_out=. --grpc_out=. --plugin=protoc-gen-grpc=$(GRPC_CPP_PLUGIN_PATH) SpookyService.proto
	
clean:
	rm SpookyService.pb.cc SpookyService.pb.h spooky.o server client
