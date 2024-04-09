namespace OrleansBenchmarks.ContractNetProtocol.Grains;

public interface IInitiatorGrain : IGrainWithIntegerKey
{
    public Task SendCallForProposalsAsync(int numberOfContractorsInStarTopology);
}

public class InitiatorGrain : Grain, IInitiatorGrain
{
    private const string TaskDetails = "Details: Design and implement a new e-commerce " + 
                                       "website with payment gateway integration.";
    
    public async Task SendCallForProposalsAsync(int numberOfContractorsInStarTopology)
    {
        var tasks = new List<Task<bool>>();
        for (int i = 0; i < numberOfContractorsInStarTopology; i++)
        {
            var contractor = GrainFactory.GetGrain<IContractorGrain>(i);
            tasks.Add(contractor.HandleCallForProposalAsync("Proposal"));
        }

        await Task.WhenAll(tasks);
    }
}
