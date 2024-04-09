using BenchmarkDotNet.Running;
using OrleansBenchmarks.Hello.Benchmarks;

var summary = BenchmarkRunner.Run<HelloBenchmark>();
