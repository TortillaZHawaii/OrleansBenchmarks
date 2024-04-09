using Microsoft.Extensions.Logging;

namespace OrleansBenchmarks.Messaging.Grains;

public interface ISenderGrain : IGrainWithIntegerKey
{
    public Task MessageUntilLimitAsync(int limit);
}

public class SenderGrain(ILogger<SenderGrain> logger, IGrainFactory grainFactory) : Grain, ISenderGrain
{
    
    public async Task MessageUntilLimitAsync(int limit)
    {
        var receiver = grainFactory.GetGrain<ICounterGrain>(this.GetPrimaryKeyLong());
        int value = 0;
        while (value < limit)
        {
            value = await receiver.IncrementAsync(value);
        }
        logger.LogInformation("SenderGrain {} Reached limit {Limit}", this.GetPrimaryKeyLong(), limit);
    }
}