# Spooky Hashing At A Distance™

## What is it?

Me playing around with GRPC and various other things.

## What can it do right now?

Right now there is an implementation of both a client and a server. The server implements the service outlined in `service SpookyHashService` in the SpookyService.proto file. The server listens for RPCs made to the Hash128 function, computes the SpookyHash based on the passed in `message HashRequest` and returns the hash in a `message HashResponse`.

The client simply reads in from stdin until EOF and makes a grpc request to the server. It then prints out the hash it received.

## Dependencies
* [GRPC](http://www.grpc.io/)
* [gflags](http://gflags.github.io/gflags/)
* [Bazel](http://bazel.io/)
* [Protocol Buffers and protoc](https://github.com/google/protobuf)

Note: a Makefile is still present but its use is deprecated. Bazel is the officially-supported build system.

## Building

The python script ./install.py will clone, build and install the needed dependencies. Installation of grpc assumes openjdk-8 is present on the system.

The client can be built with `bazel build client`. Similarly, the server can be built with `bazel build server`.

## Running

The server can simply be started with `./server`. The most important command line flag is --server\_address, which allows you to specify the address and port on which to listen on. Default is 'localhost:50051'

The client can similarly be run with `./client`, using whatever method you prefer to provide data to stdin.

Both of the programs support a --help option for full descriptions of the available command line flags
