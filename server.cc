#include <gflags/gflags.h>
#include <grpc++/server.h>
#include <grpc++/server_builder.h>
#include <grpc++/server_credentials.h>
#include <iostream>

#include "third_party/SpookyV2.h"
#include "SpookyService.pb.h"

DEFINE_string(server_address, "0.0.0.0:50051", "Server address to expose the "
                                               "SpookyHashService on. Defaults "
                                               "to 0.0.0.0:50051");

namespace spooky {

using namespace grpc;

class SpookyServiceImpl : public SpookyHashService::Service {
  Status Hash128(ServerContext *context, const HashRequest *request,
                 HashResponse *response) override {
    uint64 inout1, inout2;
    inout1 = request->seed1();
    inout2 = request->seed2();
    SpookyHash::Hash128(request->data().c_str(), request->data().length(),
                        &inout1, &inout2);
    response->set_hash1(inout1);
    response->set_hash2(inout2);
    return Status::OK;
  }
};

} // namespace spooky

void RunServer() {
  spooky::SpookyServiceImpl service;

  grpc::ServerBuilder builder;
  builder.AddPort(FLAGS_server_address, grpc::InsecureServerCredentials());
  builder.RegisterService(&service);
  std::unique_ptr<grpc::Server> server(builder.BuildAndStart());
  std::cout << "Server listening on " << FLAGS_server_address << std::endl;
  server->Wait();
}

int main(int argc, char **argv) {
  gflags::ParseCommandLineFlags(&argc, &argv, true);
  grpc_init();

  RunServer();

  grpc_shutdown();
}
