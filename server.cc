#include <grpc++/server.h>
#include <grpc++/server_builder.h>
#include <grpc++/server_credentials.h>
#include <iostream>

#include "SpookyV2.h"
#include "SpookyService.pb.h"

namespace spooky {

using namespace grpc;

class SpookyServiceImpl : public SpookyHashService::Service {
  Status Hash128(ServerContext *context, const HashRequest *request,
                         HashResponse *response) override {
    uint64 inout1, inout2;
    inout1 = request->seed1();
    inout2 = request->seed2();
    SpookyHash::Hash128(request->data().c_str(), request->data().length(), &inout1, &inout2);
    response->set_hash1(inout1);
    response->set_hash2(inout2);
    return Status::OK; 
  }
};

} // namespace spooky

void RunServer() {
  std::string server_address("0.0.0.0:50051");
  spooky::SpookyServiceImpl service;

  grpc::ServerBuilder builder;
  builder.AddPort(server_address, grpc::InsecureServerCredentials());
  builder.RegisterService(&service);
  std::unique_ptr<grpc::Server> server(builder.BuildAndStart());
  std::cout << "Server listening on " << server_address << std::endl;
  server->Wait();
}

int main() {
  grpc_init();

  RunServer(); 

  grpc_shutdown();
}
