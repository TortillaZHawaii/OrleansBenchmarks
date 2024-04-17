# start the server in the background and get its pid
dotnet OrleansBenchmarks.ClientServer.Server.dll &
server_pid=$!

# wait for the server to start
sleep 10

# start the client
dotnet OrleansBenchmarks.ClientServer.Client.dll

# kill the server
kill $server_pid
