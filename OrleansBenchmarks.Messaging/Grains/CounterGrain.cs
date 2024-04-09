namespace OrleansBenchmarks.Messaging.Grains;

public interface ICounterGrain : IGrainWithIntegerKey
{
    public Task<int> IncrementAsync(int value);
}

public class CounterGrain : Grain, ICounterGrain
{
    public Task<int> IncrementAsync(int value)
    {
        return Task.FromResult(value + 1);
    }
}