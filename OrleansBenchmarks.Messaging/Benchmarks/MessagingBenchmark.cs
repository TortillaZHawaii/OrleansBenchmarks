using BenchmarkDotNet.Attributes;

namespace OrleansBenchmarks.Messaging.Benchmarks;


public class MessagingBenchmark
{
    [IterationSetup]
    public void IterationSetup()
    {
    }
}