using Microsoft.Extensions.Logging;

namespace OrleansBenchmarks.Hello.Grains;

public interface IHelloGrain : IGrainWithStringKey
{
    public Task WakeUpAsync();   
}

public class HelloGrain(ILogger<HelloGrain> logger) : Grain, IHelloGrain
{
    public override Task OnActivateAsync(CancellationToken cancellationToken)
    {
        logger.LogInformation("Hello World! My name is {Name}", this.GetPrimaryKeyString());
        return base.OnActivateAsync(cancellationToken);
    }

    // This method is called by the client to wake up the grain
    // This is required, as there is no real notion of being manually started in Orleans.
    // Life cycle is managed by the runtime.
    public Task WakeUpAsync() => Task.CompletedTask;
}
