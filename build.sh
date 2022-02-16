#!/bin/sh

docker build -t rpc_image .

#if [ "$1" = client ]
#then
#  docker build -t rpc_client src/client/.
#
#elif [ "$1" = server ]
#then
#  docker build -t rpc_server src/server/.
#
#elif [ "$1" = both ]
#then
#  docker build -t rpc_client src/client/.
#  docker build -t rpc_server src/server/.
#
#else
#  echo Specify the a build option: server, client or both. E.g.: ./build.sh client
#fi
