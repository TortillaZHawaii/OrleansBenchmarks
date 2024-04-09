using Microsoft.Extensions.Logging;

namespace OrleansBenchmarks.Messaging.Grains;

public interface ISenderGrain : IGrainWithIntegerKey
{
}

public class SenderGrain(ILogger<SenderGrain> logger) : ISenderGrain
{
    
}