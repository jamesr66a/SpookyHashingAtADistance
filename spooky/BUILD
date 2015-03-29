#Note that this should be changed as soon as bazel's support for protocol buffers is working
genrule(
  name = "service_proto",
  srcs = ["SpookyService.proto"],
  outs = ["SpookyService.pb.cc", "SpookyService.pb.h"],
  cmd = "protoc --cpp_out=bazel-out/local_linux-fastbuild/genfiles/spooky/.. --grpc_out=bazel-out/local_linux-fastbuild/genfiles/spooky/.. --plugin=protoc-gen-grpc=/usr/local/bin/grpc_cpp_plugin spooky/SpookyService.proto"
)

cc_binary(
  name = "server",
  srcs = ["server.cc", "third_party/SpookyV2.cpp", "SpookyService.pb.cc", "SpookyService.pb.h"],
  includes = ["."],
  linkopts = ["-L/usr/local/lib", "-Lspooky/third_party/grpc/libs/opt/protobuf/", "-lgrpc_unsecure", "-lgrpc++_unsecure", "-lgrpc", "-lgpr", "-lprotobuf", "-lpthread", "-ldl", "-lgflags", "-pthread"]
)

cc_binary(
  name = "client",
  srcs = ["client.cc", "third_party/SpookyV2.cpp", "SpookyService.pb.cc", "SpookyService.pb.h"],
  includes = ["."],
  linkopts = ["-Lspooky/third_party/grpc/libs/opt", "-lgrpc++_unsecure", "-lgrpc", "-lgpr", "-lprotobuf", "-lpthread", "-ldl", "-lgflags", "-pthread"],
)
