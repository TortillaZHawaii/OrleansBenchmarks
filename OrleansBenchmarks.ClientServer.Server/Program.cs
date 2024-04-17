using Microsoft.Extensions.Hosting;

var hostBuilder = Host.CreateDefaultBuilder(args);

hostBuilder.UseOrleans(builder =>
{
    builder.UseLocalhostClustering();
});

using var host = hostBuilder
    .UseConsoleLifetime()
    .Build();
    
host.Run();
