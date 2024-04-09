using BenchmarkDotNet.Running;
using OrleansBenchmarks.ContractNetProtocol.Benchmarks;

var result = BenchmarkRunner.Run<ContractNetProtocolBenchmark>();
