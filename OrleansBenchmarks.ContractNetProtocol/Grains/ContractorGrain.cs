namespace OrleansBenchmarks.ContractNetProtocol.Grains;

public interface IContractorGrain : IGrainWithIntegerKey
{
    Task<bool> HandleCallForProposalAsync(string proposal);
}

public class ContractorGrain : Grain, IContractorGrain
{
    public Task<bool> HandleCallForProposalAsync(string proposal)
    {
        bool shouldAccept = this.GetPrimaryKeyLong() % 2 == 0;
        return Task.FromResult(shouldAccept);
    }
}