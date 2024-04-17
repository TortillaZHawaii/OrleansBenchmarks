namespace OrleansBenchmarks.ClientServer.Server.Grains;

public class CounterGrain : Grain, ICounterGrain
{
    public Task<int> IncrementAsync(int value)
    {
        return Task.FromResult(value + 1);
    }
}
