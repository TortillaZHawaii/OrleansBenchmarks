import pandas as pd
from typing import Sequence
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from scipy.stats import norm


def load_data():
    # available: jobname;execution;timestamp;cpu;os;method;size;mean;error;stddev;median;unit
    columns_to_read = ['timestamp', 'jobname', 'method', 'size', 'mean', 'stddev', 'cpu']
    data = pd.read_csv('results.csv', usecols=columns_to_read, sep=',', decimal=',')

    # data cleaning, strings to numbers
    data = data.loc[data['mean'] != '']
    data = data.loc[data['mean'] != ' ']
    data['mean'] = data['mean'].str.replace(',', '.', regex=True).astype(float)


    # convert units from micro- to miliseconds
    data['mean'] = data['mean'].apply(lambda mean: mean / 1000)


    # scenariusze to nazwy te same co jobname, z wyjątkiem jobname "orleans-hello" i method "CreateGrainsParallel"
    def unnest_scenario(row):
        if row['jobname'] == 'orleans-hello' and row['method'] == 'CreateGrainsParallel':
            return 'orleans-hello-parallel'
        return row['jobname']

    data['scenario'] = data.apply(unnest_scenario, axis='columns')

    # convert string to datetime
    data['timestamp'] = data['timestamp'].apply(lambda timestamp: datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ"))



    # oczyść nazwy procesorów ze szczegółów, niech będzie sama nazwa modelu
    data['cpu'] = data['cpu'].apply(lambda cpu: cpu[:-39])



    # pogrupowane tak, żeby finalnie mieć listę z data frame'ami, w każdym tylko jedna para (scenario, size)
    grouped_by_scenario_and_size = data.groupby(['scenario', 'size'])
    groups: Sequence[pd.DataFrame] = [grouped_by_scenario_and_size.get_group(group) for group in grouped_by_scenario_and_size.groups]

    return groups



#   orleans-hello                   nnn
#   orleans-hello-parallel          nnn
#   orleans-messaging               389
#   orleans-contract-net-protocol   388
#   orleans-client-server           304

# Draw one scenario, rather don't use
def draw_scenario(groups: Sequence[pd.DataFrame]):
    # available scenarios: 
    #   - orleans-hello
    #   - orleans-hello-parallel
    #   - orleans-messaging
    #   - orleans-contract-net-protocol
    #   - orleans-client-server

    # scenario = "orleans-hello"
    # scenario = "orleans-hello-parallel"
    # scenario = "orleans-messaging"
    # scenario = "orleans-contract-net-protocol"
    scenario = "orleans-client-server"

    desired_groups = list(filter(lambda group: group.iloc[0]["scenario"] == scenario, groups))
    num_charts = len(desired_groups)
    fig, axes = plt.subplots(1, num_charts)
    for idx, group in enumerate(desired_groups):
        first_row = group.iloc[0]
        axes[idx].hist(group['mean'], bins=30)
        mean = group['mean'].mean()
        std = group['mean'].std()
        title_first_row = first_row['scenario'] + ', ' + str(first_row['size'])
        title_sec_row = 'mean = ' + "{:.1f}".format(mean) + ', stddev = ' + "{:.1f}".format(std)
        axes[idx].set_title(title_first_row + '\n' + title_sec_row)

    plt.legend()
    plt.show()




def draw_all(groups: Sequence[pd.DataFrame]):
    scenarios = [
        # "orleans-hello",
        # "orleans-hello-parallel",
        "orleans-messaging",
        "orleans-contract-net-protocol",
        "orleans-client-server"
    ]

    fig, axes = plt.subplots(3, 7, figsize=(20, 10))
    for scenario_idx, scenario in enumerate(scenarios):
        scenario_groups = list(filter(lambda group: group.iloc[0]["scenario"] == scenario, groups))
        for idx, group in enumerate(scenario_groups):
            first_row = group.iloc[0]
            axes[scenario_idx, idx].hist(group['mean'], bins=30)
            mean = group['mean'].mean()
            std = group['mean'].std()
            title_first_row = first_row['scenario'][8:] + ', ' + str(first_row['size'])
            if scenario_idx == 0:
                title = title_first_row  # for messaging scenario we don't calculate mean and stdev since it doesn't make sense
            else:
                title_sec_row = 'mean = ' + "{:.1f}".format(mean) + ', stddev = ' + "{:.1f}".format(std)
                title = title_first_row + '\n' + title_sec_row
            axes[scenario_idx, idx].set_title(title)
            axes[scenario_idx, idx].set_xlabel("Execution time [ms]")
            axes[scenario_idx, idx].set_ylabel("Count")
    
    fig.subplots_adjust(left=0.03, right=0.95, top=0.93, bottom=0.06, wspace=0.5, hspace=0.6)
    plt.legend()
    fig.savefig('charts.pdf')
    # plt.show()




def draw_cvs(groups: Sequence[pd.DataFrame]):
    scenarios = [
        "orleans-messaging",
        "orleans-contract-net-protocol",
        "orleans-client-server"
    ]

    fig, axes = plt.subplots(len(scenarios), 1, figsize=(20, 10))
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    for scenario_idx, scenario in enumerate(scenarios):
        scenario_groups = list(filter(lambda group: group.iloc[0]["scenario"] == scenario, groups))

        # calculate cv for each group
        cvs = []
        for group in scenario_groups:
            mean = group['mean'].mean()
            std = group['mean'].std()
            cv = std / mean * 100 # percent
            cvs.append(cv)

        # draw cv for each group
        axes[scenario_idx].hist(cvs, bins=bins)
        axes[scenario_idx].set_title(scenario[8:])
        axes[scenario_idx].set_xlabel("Coefficient Variance [%]")
        axes[scenario_idx].set_ylabel("Count")

    fig.subplots_adjust(left=0.03, right=0.95, top=0.93, bottom=0.06, wspace=0.5, hspace=0.6)
    plt.show()




def draw_all_with_respect_to_cpu(groups: Sequence[pd.DataFrame]):
    scenarios = [
        "orleans-messaging",
        "orleans-contract-net-protocol",
        "orleans-client-server"
    ]

    fig, axes = plt.subplots(3, 7, figsize=(20, 10))
    for scenario_idx, scenario in enumerate(scenarios):
        scenario_groups = list(filter(lambda group: group.iloc[0]["scenario"] == scenario, groups))
        for idx, group in enumerate(scenario_groups):
            cpu_groups = group.groupby('cpu')
            bins = np.linspace(group['mean'].min(), group['mean'].max(), 30)
            first_row = group.iloc[0]
            bottom = np.zeros(len(bins) - 1)
            for cpu_name, cpu_group in cpu_groups:
                counts, _ = np.histogram(cpu_group['mean'], bins=bins)
                axes[scenario_idx, idx].bar(bins[:-1], counts, width=np.diff(bins), bottom=bottom, label=cpu_name)
                bottom += counts
                title = first_row['scenario'][8:] + ', ' + str(first_row['size'])
                axes[scenario_idx, idx].set_title(title)
                axes[scenario_idx, idx].set_xlabel("Execution time [ms]")
                axes[scenario_idx, idx].set_ylabel("Count")
    
    fig.subplots_adjust(left=0.03, right=0.95, top=0.93, bottom=0.12, wspace=0.5, hspace=0.5)
    plt.legend(loc='upper center', bbox_to_anchor=(-4, -0.3), fancybox=False, shadow=False, ncol=5)
    fig.savefig('charts.pdf')
    # plt.show()



# narysuj z podziałem na godzinę
def draw_all_with_respect_to_hour(groups: Sequence[pd.DataFrame]):
    scenarios = [
        "orleans-messaging",
        "orleans-contract-net-protocol",
        "orleans-client-server"
    ]

    colors = {
        0:  '#0000FF', # blue
        1:  '#0028D7',
        2:  '#0050AF',
        3:  '#007887',
        4:  '#00A05F',
        5:  '#00C837',
        6:  '#00FF00',
        7:  '#28FF00',
        8:  '#50FF00',
        9:  '#78FF00',
        10: '#A0FF00',
        11: '#C8FF00',
        12: '#DCFF00', # yellow
        13: '#B4FF00',
        14: '#8CFF00',
        15: '#64FF00',
        16: '#3CFF00',
        17: '#14FF00',
        18: '#00DC23',
        19: '#00B44B',
        20: '#008C73',
        21: '#00649B',
        22: '#003CC3',
        23: '#0014EB', # blue again
    }

    fig, axes = plt.subplots(3, 7, figsize=(20, 10))
    for scenario_idx, scenario in enumerate(scenarios):
        scenario_groups = list(filter(lambda group: group.iloc[0]["scenario"] == scenario, groups))
        for idx, group in enumerate(scenario_groups):
            hour_groups = group.groupby(group['timestamp'].apply(lambda timestamp: timestamp.hour))
            bins = np.linspace(group['mean'].min(), group['mean'].max(), 30)
            first_row = group.iloc[0]
            bottom = np.zeros(len(bins) - 1)
            for hour, hour_group in hour_groups:
                counts, _ = np.histogram(hour_group['mean'], bins=bins)
                axes[scenario_idx, idx].bar(bins[:-1], counts, width=np.diff(bins), bottom=bottom, label=hour, color=colors[hour])
                bottom += counts
                title = first_row['scenario'][8:] + ', ' + str(first_row['size'])
                axes[scenario_idx, idx].set_title(title)
                axes[scenario_idx, idx].set_xlabel("Execution time [ms]")
                axes[scenario_idx, idx].set_ylabel("Count")
    
    fig.subplots_adjust(left=0.03, right=0.95, top=0.93, bottom=0.12, wspace=0.4, hspace=0.4)
    plt.legend(loc='upper center', bbox_to_anchor=(-3.6, -0.3), fancybox=False, shadow=False, ncol=24)
    fig.savefig('charts.pdf')
    # plt.show()




# narysuj z podziałem na procesor i wybierz najpierw wybrane przeze mnie
def draw_chosen_with_respect_to_cpu(groups: Sequence[pd.DataFrame]):
    scenarios = [
        # "orleans-hello",
        # "orleans-hello-parallel",
        "orleans-messaging",
        "orleans-contract-net-protocol",
        "orleans-client-server"
    ]

    allowed_scenario_sizes_pairs = {
        0: [0, 3, 6],
        1: [4, 5, 6],
        2: [3, 4, 5],
    }

    fig, axes = plt.subplots(3, 3, figsize=(10, 10))
    for scenario_idx, scenario in enumerate(scenarios):
        scenario_groups = list(filter(lambda group: group.iloc[0]["scenario"] == scenario, groups))
        group_in_plot_idx = 0
        for idx, group in enumerate(scenario_groups):
            size_in_allowed_idx = allowed_scenario_sizes_pairs[scenario_idx]
            if idx in size_in_allowed_idx:
                cpu_groups = group.groupby('cpu')
                bins = np.linspace(group['mean'].min(), group['mean'].max(), 30)
                first_row = group.iloc[0]
                bottom = np.zeros(len(bins) - 1)
                for cpu_name, cpu_group in cpu_groups:
                    counts, _ = np.histogram(cpu_group['mean'], bins=bins)
                    axes[scenario_idx, group_in_plot_idx].bar(bins[:-1], counts, width=np.diff(bins), bottom=bottom, label=cpu_name)
                    bottom += counts
                    title = first_row['scenario'][8:] + ', ' + str(first_row['size'])
                    axes[scenario_idx, group_in_plot_idx].set_title(title)
                    axes[scenario_idx, group_in_plot_idx].set_xlabel("Execution time [ms]")
                    axes[scenario_idx, group_in_plot_idx].set_ylabel("Count")
                
                group_in_plot_idx = group_in_plot_idx + 1
    
    fig.subplots_adjust(left=0.03, right=0.95, top=0.93, bottom=0.12, wspace=0.4, hspace=0.4)
    plt.legend(loc='upper center', bbox_to_anchor=(-1, -0.2), fancybox=False, shadow=False, ncol=4)
    fig.savefig('charts.pdf')
    # plt.show()




# narysuj z podziałem na godzinę wybrane przeze mnie
def draw_chosen_with_respect_to_hour(groups: Sequence[pd.DataFrame]):
    scenarios = [
        # "orleans-hello",
        # "orleans-hello-parallel",
        "orleans-messaging",
        "orleans-contract-net-protocol",
        "orleans-client-server"
    ]

    colors = {
        0:  '#0000FF', # blue
        1:  '#0028D7',
        2:  '#0050AF',
        3:  '#007887',
        4:  '#00A05F',
        5:  '#00C837',
        6:  '#00FF00',
        7:  '#28FF00',
        8:  '#50FF00',
        9:  '#78FF00',
        10: '#A0FF00',
        11: '#C8FF00',
        12: '#DCFF00', # yellow
        13: '#B4FF00',
        14: '#8CFF00',
        15: '#64FF00',
        16: '#3CFF00',
        17: '#14FF00',
        18: '#00DC23',
        19: '#00B44B',
        20: '#008C73',
        21: '#00649B',
        22: '#003CC3',
        23: '#0014EB', # blue
    }

    allowed_scenario_sizes_pairs = {
        0: [2, 3, 4],
        1: [4, 5, 6],
        2: [3, 4, 5],
    }

    fig, axes = plt.subplots(3, 3, figsize=(10, 10))
    for scenario_idx, scenario in enumerate(scenarios):
        scenario_groups = list(filter(lambda group: group.iloc[0]["scenario"] == scenario, groups))
        group_in_plot_idx = 0
        for idx, group in enumerate(scenario_groups):
            size_in_allowed_idx = allowed_scenario_sizes_pairs[scenario_idx]
            if idx in size_in_allowed_idx:
                hour_groups = group.groupby(group['timestamp'].apply(lambda timestamp: timestamp.hour))
                bins = np.linspace(group['mean'].min(), group['mean'].max(), 30)
                first_row = group.iloc[0]
                bottom = np.zeros(len(bins) - 1)
                for hour, hour_group in hour_groups:
                    counts, _ = np.histogram(hour_group['mean'], bins=bins)
                    axes[scenario_idx, group_in_plot_idx].bar(bins[:-1], counts, width=np.diff(bins), bottom=bottom, label=hour, color=colors[hour])
                    bottom += counts
                    title = first_row['scenario'][8:] + ', ' + str(first_row['size'])
                    axes[scenario_idx, group_in_plot_idx].set_title(title)
                    axes[scenario_idx, group_in_plot_idx].set_xlabel("Execution time [ms]")
                    axes[scenario_idx, group_in_plot_idx].set_ylabel("Count")
                group_in_plot_idx = group_in_plot_idx + 1

    fig.subplots_adjust(left=0.03, right=0.95, top=0.93, bottom=0.12, wspace=0.4, hspace=0.4)
    plt.legend(loc='upper center', bbox_to_anchor=(-0.9, -0.2), fancybox=False, shadow=False, ncol=12)
    fig.savefig('charts.pdf')
    # plt.show()




# narysuj wybrane z rozkładem
def draw_chosen_with_normal(groups: Sequence[pd.DataFrame]):
    scenarios = [
        # "orleans-hello",
        # "orleans-hello-parallel",
        "orleans-messaging",
        "orleans-contract-net-protocol",
        "orleans-client-server"
    ]

    allowed_scenario_sizes_pairs = [0, 4]

    fig, axes = plt.subplots(2, 1, figsize=(5, 8))
    for scenario_idx, scenario in enumerate(scenarios):
        scenario_groups = list(filter(lambda group: group.iloc[0]["scenario"] == scenario, groups))
        group_in_plot_idx = 0
        for idx, group in enumerate(scenario_groups):
            if scenario_idx != 0:
                continue
            # allowed_scenario_sizes_pairs size_in_allowed_idx = allowed_scenario_sizes_pairs.get(scenario_idx, None)
            if idx in allowed_scenario_sizes_pairs:
                first_row = group.iloc[0]
                axes[group_in_plot_idx].hist(group['mean'], bins=30)
                title_first_row = first_row['scenario'][8:] + ', ' + str(first_row['size'])
                axes[group_in_plot_idx].set_title(title_first_row)
                axes[group_in_plot_idx].set_xlabel("Execution time [ms]")
                axes[group_in_plot_idx].set_ylabel("Count")

                if idx == 0:
                    xmin = 0.5
                    xmax = 4.0
                    x = np.linspace(xmin, xmax, 100)
                    p1 = norm.pdf(x, 0.9, 0.16)
                    for idx, elem in enumerate(p1):
                        p1[idx] = 33 * elem

                    p2 = norm.pdf(x, 2.17, 0.13)
                    for idx, elem in enumerate(p2):
                        p2[idx] = 13 * elem

                    pres = []
                    for idx, _ in enumerate(p1):
                        pres.append(p1[idx] + p2[idx])
                
                    axes[group_in_plot_idx].plot(x, pres, color='red', linewidth=3)



                if idx == 4:
                    xmin = 1
                    xmax = 49
                    x = np.linspace(xmin, xmax, 100)
                    p1 = norm.pdf(x, 11, 1.7)
                    for idx, elem in enumerate(p1):
                        p1[idx] = 270 * elem

                    p2 = norm.pdf(x, 18.5, 2.0)
                    for idx, elem in enumerate(p2):
                        p2[idx] = 90 * elem

                    p3 = norm.pdf(x, 35, 2.8)
                    for idx, elem in enumerate(p3):
                        p3[idx] = 130 * elem

                    pres = []
                    for idx, _ in enumerate(p1):
                        pres.append(p1[idx] + p2[idx] + p3[idx])
                
                    axes[group_in_plot_idx].plot(x, pres, color='red', linewidth=3)


                axes[group_in_plot_idx].set_xlabel("Execution time [ms]")
                axes[group_in_plot_idx].set_ylabel("Count")

                group_in_plot_idx = group_in_plot_idx + 1
    
    fig.subplots_adjust(left=0.06, right=0.98, top=0.93, bottom=0.08, wspace=0.3, hspace=0.24)
    plt.legend()
    fig.savefig('charts.pdf')





if __name__ == "__main__":
    groups = load_data()
    draw_cvs(groups)
    # draw_all(groups)

