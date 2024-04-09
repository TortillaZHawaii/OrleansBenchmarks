using BenchmarkDotNet.Attributes;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using OrleansBenchmarks.ContractNetProtocol.Grains;

namespace OrleansBenchmarks.ContractNetProtocol.Benchmarks;

public class ContractNetProtocolBenchmark
{
    [Params(0, 100, 200, 300, 400, 500, 1000, 1500, 2000, 2500, 3500, 5000, 7000, 8750, 10000)]
    public int NumberOfContractorAgentsInStarTopology { get; set; }

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
    public async Task SendCallForProposals()
    {
        var grainFactory = Host.Services.GetRequiredService<IGrainFactory>();
        var initiator = grainFactory.GetGrain<IInitiatorGrain>(0);
        await initiator.SendCallForProposalsAsync(NumberOfContractorAgentsInStarTopology);
    }
}