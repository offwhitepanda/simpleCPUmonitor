import pandas as pd
import psutil
import time
import threading
import matplotlib.pyplot as plt

def run_all():

    def get_cpu_utilization():
        cpu_percent = psutil.cpu_percent(percpu=True)
        cpu_cores = range(len(cpu_percent))
        df = pd.DataFrame({'Utilization': cpu_percent}, index=cpu_cores)
        return df

    def update_dataframe(df_cpu):
        new_df = get_cpu_utilization()
        if df_cpu.shape[1] >= 5:
            print("Removing a row")
            print(str(df_cpu.shape[1]))
            breakpoint()
            df_cpu = df_cpu.iloc[1:]  # Remove the first row
        df_cpu = pd.concat([df_cpu, new_df], axis=1)
        return df_cpu

    # initialize the dataframe
    df_cpu = get_cpu_utilization()

    # Convert the DataFrame to a NumPy array.
    df_cpu_array = df_cpu.to_numpy()

    # Sum each row of the NumPy array.
    df_cpu_sums = df_cpu_array.sum(axis=1)

    # Create a new DataFrame with the summed values.
    df_cpu_sums_df = pd.DataFrame({'Utilization': df_cpu_sums})

    print(df_cpu.transpose())

    # Plot the new DataFrame as a line graph, with each row representing a single line on the graph.
    fig, ax = plt.subplots()
    line, = ax.plot(df_cpu_sums_df.index, df_cpu_sums_df['Utilization'])
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('CPU Utilization (%)')
    ax.set_title('CPU Utilization over Time')
    plt.show(block=False)

    # Limit the number of plot points to a maximum of five per row.
    ax.set_xlim(0, 5)

    while True:
        df_cpu = update_dataframe(df_cpu)

        # Convert the DataFrame to a NumPy array.
        df_cpu_array = df_cpu.to_numpy()

        # Sum each row of the NumPy array.
        df_cpu_sums = df_cpu_array.sum(axis=1)

        # Create a new DataFrame with the summed values.
        df_cpu_sums_df = pd.DataFrame({'Utilization': df_cpu_sums})

        # display the resulting dataframe
        print(df_cpu.transpose())
        line, = ax.plot(df_cpu_sums_df.index, df_cpu_sums_df['Utilization'])
        ax.autoscale_view()
        plt.draw()
        plt.pause(3)

run_all()
