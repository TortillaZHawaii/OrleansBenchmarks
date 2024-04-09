using BenchmarkDotNet.Attributes;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using OrleansBenchmarks.Hello.Grains;

namespace OrleansBenchmarks.Hello.Benchmarks;

public class HelloBenchmark
{
    [Params(0, 100, 200, 300, 400, 500, 1000, 1500, 2000, 2500, 3500, 5000, 7000, 8750, 10000)]
    public int NumberOfGrainsCreated { get; set; }

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
    public async Task CreateGrains()
    {
        // Get the grain factory
        var grainFactory = Host.Services.GetRequiredService<IGrainFactory>();
        
        for (int i = 0; i < NumberOfGrainsCreated; i++)
        {
            var grain = grainFactory.GetGrain<IHelloGrain>($"HelloGrain {i}");
            await grain.WakeUpAsync();
        }
    }

    [Benchmark]
    public async Task CreateGrainsParallel()
    {
        // Get the grain factory
        var grainFactory = Host.Services.GetRequiredService<IGrainFactory>();
        
        var tasks = new List<Task>();
        for (int i = 0; i < NumberOfGrainsCreated; i++)
        {
            var grain = grainFactory.GetGrain<IHelloGrain>($"HelloGrain {i}");
            tasks.Add(grain.WakeUpAsync());
        }
        
        await Task.WhenAll(tasks);
    }
}