using BenchmarkDotNet.Attributes;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using OrleansBenchmarks.Messaging.Grains;

namespace OrleansBenchmarks.Messaging.Benchmarks;


public class MessagingBenchmark
{
    [Params(100, 200, 500, 1000, 2000, 5000, 10000)]
    public int NumberOfMessageTransfersInBothDirections { get; set; }
    
    private IHost Host { get; set; } = null!;
    
    [GlobalSetup]
    public async Task Setup()
    {
        Host = new HostBuilder()
            .UseOrleans(builder => builder.UseLocalhostClustering())
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
        // Get the grain factory
        var grainFactory = Host.Services.GetRequiredService<IGrainFactory>();
        
        var sender = grainFactory.GetGrain<ISenderGrain>(0);

        await sender.MessageUntilLimitAsync(NumberOfMessageTransfersInBothDirections);
    }
}