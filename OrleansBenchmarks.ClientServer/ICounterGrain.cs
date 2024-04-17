using Orleans;

namespace OrleansBenchmarks.ClientServer;

public interface ICounterGrain : IGrainWithIntegerKey
{
    public Task<int> IncrementAsync(int value);
}
