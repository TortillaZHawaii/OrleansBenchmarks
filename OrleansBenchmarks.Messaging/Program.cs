using BenchmarkDotNet.Running;
using OrleansBenchmarks.Messaging.Benchmarks;

var summary = BenchmarkRunner.Run<MessagingBenchmark>();
