#! /usr/bin/env python2

import os, subprocess, distutils.dir_util, ctypes, getopt, sys
from ctypes.util import find_library

bazel_repo = "https://github.com/google/bazel.git"

grpc_repo = "https://github.com/grpc/grpc.git"
grpc_commit = "bc6f3f04d81dbe71433d1187767c7263cef66764"

gflags_repo = "https://github.com/gflags/gflags.git"
gflags_commit = "16a168763e2cb41f8bf9f40505fcba494e316a35"

protobuf_repo = "https://github.com/google/protobuf.git"

par_build_count = 9

try:
  opts, args = getopt.getopt(sys.argv[1:], "i")
except getopt.GetoptError:
  print 'Error parsing command line flags'
  exit()

def try_load_so(name, version=-1):
  lib_path = find_library(name)
  if version != -1:
    lib_path = lib_path + ".%s" % version;
  if lib_path == None:
    return False
  try:
    lib = ctypes.CDLL(lib_path);
  except:
    return False
  print "succeeded loading so %s" % lib_path
  return True

def install_protobuf():
  print "Installing protobuf"
  if not os.path.exists("./protobuf"):
    if subprocess.call(["git", "clone", protobuf_repo]) != 0:
      print "Error cloning protobuf repo"
      exit()
  os.chdir("./protobuf")
  if subprocess.call(["git", "checkout", "tags/v3.0.0-alpha-2"]) != 0:
    print "Error checking out 3.0.0 tag of protobuf"
    exit()
  if subprocess.call(["./autogen.sh"]) != 0:
    print "Error calling autogen on protobuf"
    exit()
  if subprocess.call(["./configure"]) != 0:
    print "Error calling configure on protobuf"
    exit()
  if subprocess.call(["make", "-j%s" % par_build_count]) != 0:
    print "Error building protobuf"
    exit()
  if subprocess.call(["sudo", "make", "install"]) != 0:
    print "Error installing protobuf. Are you running as root?"
    exit()
  os.chdir("../")

def install_grpc():
  print "Installing GRPC"
  if not os.path.exists("./grpc"):
    if subprocess.call(["git", "clone", grpc_repo]) != 0:
      print "ERROR cloning grpc repo"
      exit()
  os.chdir("./grpc")
  if subprocess.call(["git", "checkout", grpc_commit]) != 0:
    print "Clould not checkout grpc commit"
    exit()
  if subprocess.call(["git", "submodule", "update", "--init"]) != 0:
    print "Could not git submodule update --init"
    exit()
  if subprocess.call(["make", "-j%s" % par_build_count]) != 0:
    print "Could not make grpc"
    exit()
  if subprocess.call(["sudo", "make", "install"]) != 0:
    print "Could not install grpc"
    exit();
  os.chdir("..")

def which(file):
  for path in os.environ["PATH"].split(":"):
    if os.path.exists(path + "/" + file):
      return path + "/" + file
  return None

def install_bazel():
  if subprocess.call(["git", "clone", bazel_repo]) != 0:
    print "ERROR cloning bazel repo"
    exit()
  os.chdir("./bazel")
  if subprocess.call(["./compile.sh"]) != 0:
    print "ERROR compiling bazel"
    exit()
  os.chdir("..")
  if not os.path.exists("./bazel/output/bazel"):
    print "ERROR: bazel executable not created!"
    exit()
  return "./bazel/output/bazel"

def install_gflags():
  if not os.path.exists("./gflags") and subprocess.call(["git", "clone", gflags_repo]) != 0:
    print "ERROR cloning gflags"
    exit()
  os.chdir("./gflags")
  if subprocess.call(["git", "checkout", gflags_commit]) != 0:
    print "Could not checkout gflags commit"
    exit()
  if not os.path.exists("./build"):
    os.makedirs("./build")
  os.chdir("./build")
  if subprocess.call(["cmake", ".."]) != 0:
    print "ERROR: ccmake failed"
    exit()
  if subprocess.call(["make", "-j%s" % par_build_count]) != 0:
    print "ERROR: could not build gflags"
    exit()
  if subprocess.call(["sudo", "make", "install"]) != 0:
    print "ERROR: could not install grpc. Are you running as root?"
    exit()


os.chdir("spooky/third_party")

bazel_path = which("bazel")
if bazel_path == None:
  if not os.path.exists("./bazel/output/bazel"):
    bazel_path = install_bazel()
  else:
    bazel_path = "./bazel/output/bazel"

if bazel_path != None: 
  print "Bazel executable located: " + bazel_path 

bazel_path = os.path.abspath(bazel_path)

if not os.path.exists("../bazel"):
  os.symlink(bazel_path, "../bazel")

distutils.dir_util.copy_tree(os.path.dirname(bazel_path) + "/../base_workspace/", "../../")

if try_load_so("protobuf"):
  print "libprotobuf found"
  if try_load_so("protoc"):
    print "libprotoc found"
  else:
    install_protobuf()
else:
  install_protobuf()

if try_load_so("grpc++_unsecure"): #or os.path.exists("grpc/libs/opt/libgrpc++_unsecure.so"):
  print "libgrpc++_unsecure found"
  if try_load_so("grpc"): #or os.path.exists("grpc/libs/opt/libgrpc.so"):
    print "libgrpc found"
  else:
    install_grpc()
else:
  install_grpc()

#if try_load_so("gflags"):
#  print "libgflags found"
#else:
install_gflags()
