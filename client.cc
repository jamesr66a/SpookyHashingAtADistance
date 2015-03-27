#include <cstdint>
#include <gflags/gflags.h>
#include <grpc/grpc.h>
#include <grpc++/channel_arguments.h>
#include <grpc++/channel_interface.h>
#include <grpc++/client_context.h>
#include <grpc++/create_channel.h>
#include <grpc++/credentials.h>
#include <grpc++/status.h>
#include <iostream>
#include <memory>

#include "SpookyService.pb.h"

DEFINE_string(server_address, "localhost:50051",
              "Server to call the SpookyHashService on");

namespace spooky {
using namespace grpc;

class SpookyServiceClient {
public:
  SpookyServiceClient(std::shared_ptr<ChannelInterface> channel)
      : stub_(SpookyHashService::NewStub(channel)) {}

  std::pair<uint64_t, uint64_t> Hash128(const std::string &data) {
    HashRequest request;
    request.set_data(data);
    request.set_seed1(0);
    request.set_seed2(0);
    HashResponse response;
    ClientContext context;

    Status status = stub_->Hash128(&context, request, &response);
    if (status.IsOk()) {
      return std::make_pair<uint64_t, uint64_t>(response.hash1(),
                                                response.hash2());
    } else {
      std::cerr << "sux";
      return std::make_pair<uint64_t, uint64_t>(0,0);
    }
  }

  void Shutdown() { stub_.reset(); }

private:
  std::unique_ptr<SpookyHashService::Stub> stub_;
};

} // namespace spooky

int main(int argc, char **argv) {
  gflags::ParseCommandLineFlags(&argc, &argv, true);
  grpc_init();

  spooky::SpookyServiceClient client(
      grpc::CreateChannel(FLAGS_server_address, grpc::InsecureCredentials(),
                          grpc::ChannelArguments()));

  std::cin >> std::noskipws;
  std::istream_iterator<char> it(std::cin);
  std::istream_iterator<char> end;
  std::string data(it, end);

  std::pair<uint64_t, uint64_t> hash = client.Hash128(data);

  std::cout << hash.first << " " << hash.second << std::endl;

  client.Shutdown();

  grpc_shutdown();
}
