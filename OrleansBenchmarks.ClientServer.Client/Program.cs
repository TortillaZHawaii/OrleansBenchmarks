using BenchmarkDotNet.Running;
using OrleansBenchmarks.ClientServer.Client.Benchmarks;

var summary = BenchmarkRunner.Run<ClientServerBenchmark>();
