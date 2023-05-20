import pandas as pd
import psutil
import time
import threading
import numpy as np
import matplotlib.pyplot as plt

i = 0
time_window = 30
refresh_interval = 2
window_closed = False

def on_close(event):
    # Set the flag to True when the window is closed
    global window_closed
    window_closed = True
def run_all():

    def get_cpu_utilization():
        global i
        cpu_percent = psutil.cpu_percent(percpu=True)
        cpu_cores = range(len(cpu_percent))
        # df = pd.DataFrame({'Utilization': cpu_percent}, index=cpu_cores)
        df = pd.DataFrame({f'Utilization{i}': cpu_percent}, index=cpu_cores)
        if i >= time_window - 1:
            i = 0
        else:
            i += 1
        return df

    def update_dataframe(df_cpu):
        new_df = get_cpu_utilization()
        if df_cpu.shape[1] >= time_window:
            print("Removing a row")
            print(str(df_cpu.shape[1]))
            df_cpu = df_cpu.drop(df_cpu.columns[0], axis=1)  # Remove the first row
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
    fig = plt.figure(num='CPU Utilization Graph', figsize=(8, 6))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('CPU Utilization (%)')
    ax.set_title('CPU Utilization over Time')

    # Register the event handler for the window close event
    fig.canvas.mpl_connect('close_event', on_close)

    # Initialize a variable to keep track of the number of rows
    num_rows = 0
    x_values = range(1, time_window+1)

    while not window_closed:
        print(df_cpu)
        df_cpu = update_dataframe(df_cpu)

        # Convert the DataFrame to a NumPy array.
        df_cpu_array = df_cpu.to_numpy()

        # Sum each row of the NumPy array.
        df_cpu_sums = df_cpu_array.mean(axis=0)

        # Pad df_cpu_sums with zeros at the beginning if its length is less than 5
        padding_width = max(0, time_window - len(df_cpu_sums))
        df_cpu_sums = np.pad(df_cpu_sums, (padding_width, 0), mode='constant')

        # Clear the previous plot.
        ax.clear()

        # Plot the sum of utilization values for each row as a line and shade the area below the line.
        ax.fill_between(x_values, df_cpu_sums, color='skyblue', alpha=0.3)
        ax.plot(x_values, df_cpu_sums, color='blue')

        ax.relim()
        ax.autoscale_view()

        # Set the x and y axis labels
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('CPU Utilization (%)')

        # Increment the number of rows
        num_rows += len(df_cpu_sums)

        plt.draw()
        plt.pause(refresh_interval)


run_all()
