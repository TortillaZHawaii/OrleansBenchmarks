#!/bin/bash
echo "Starting server"

# start the server in the background and get its pid
dotnet OrleansBenchmarks.ClientServer.Server.dll &
server_pid=$!

# wait for the server to start
sleep 10

echo "Starting client"

# start the client
dotnet OrleansBenchmarks.ClientServer.Client.dll

echo "Client finished"

# kill the server
kill $server_pid

echo "Server finished"
