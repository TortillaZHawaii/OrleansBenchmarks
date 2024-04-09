using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using OrleansBenchmarks.Messaging.Grains;

using var host = new HostBuilder()
    .UseOrleans(builder => builder.UseLocalhostClustering())
    .Build();
    
await host.StartAsync();

var grainFactory = host.Services.GetRequiredService<IGrainFactory>();

var grain = grainFactory.GetGrain<ISenderGrain>(0);


