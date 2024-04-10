using BenchmarkDotNet.Attributes;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using OrleansBenchmarks.ContractNetProtocol.Grains;

namespace OrleansBenchmarks.ContractNetProtocol.Benchmarks;

public class ContractNetProtocolBenchmark
{
    [Params(100, 200, 500, 1000, 2000, 5000, 10000)]
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