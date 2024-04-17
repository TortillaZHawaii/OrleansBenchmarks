using BenchmarkDotNet.Attributes;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

namespace OrleansBenchmarks.ClientServer.Client.Benchmarks;

public class ClientServerBenchmark
{
    [Params(100, 200, 500, 1000, 2000, 5000, 10000)]
    public int NumberOfMessageTransfersInBothDirections { get; set; }
    
    private IHost Host { get; set; } = null!;
    
    [GlobalSetup]
    public async Task Setup()
    {
        Host = new HostBuilder()
            .UseOrleansClient(builder => builder.UseLocalhostClustering())
            .Build();
        
        await Host.StartAsync();
    }
    
    [GlobalCleanup]
    public async Task Cleanup()
    {
        await Host.StopAsync();
        Host.Dispose();
    }
    
    [Benchmark]
    public async Task SendMessages()
    {
        var clusterClient = Host.Services.GetRequiredService<IClusterClient>();
        var receiver = clusterClient.GetGrain<ICounterGrain>(0);
        int value = 0;
        while (value < NumberOfMessageTransfersInBothDirections)
        {
            value = await receiver.IncrementAsync(value);
        }
    }
}