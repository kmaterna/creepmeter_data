import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def simple_plot(ts_trace, outfilename):
    """
    :param ts_trace: single time series of type ts_obj
    :param outfilename: string
    """
    fig, ax = plt.subplots(figsize=(10, 3), dpi=300)
    ax.scatter(ts_trace.t, ts_trace.slip_mm, s=1)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M\n%d-%b-%Y'))
    ax.set_ylabel('Displacement (mm)', fontsize=15)
    fig.tight_layout()
    ax.tick_params(axis='x', which='major', labelsize=15)
    ax.tick_params(axis='y', which='major', labelsize=15)
    ax.set_title(ts_trace.station + ": " + ts_trace.network)
    fig.savefig(outfilename, bbox_inches="tight")
    plt.close(fig)
    return


def simple_velocity_plot(ts_trace, outfilename):
    """
    Plot the velocity of a creep event snippet

    :param ts_trace: single time series of type ts_obj
    :param outfilename: string
    """
    fig, ax = plt.subplots(2, 1, figsize=(10, 6), dpi=300, sharex=True)
    plotting_function = ts_trace.slip_mm
    ax[0].plot(ts_trace.t, plotting_function, linewidth=0.40)
    ax[0].set_ylabel('Displacement (mm)', fontsize=15)
    tvel, vel = ts_trace.get_velocity()
    ax[1].plot(tvel, vel, linewidth=0.40)
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M\n%d-%b-%Y'))
    ax[1].set_ylabel('Velocity (m/s)', fontsize=15)
    fig.tight_layout()
    ax[1].tick_params(axis='x', which='major', labelsize=15)
    ax[1].tick_params(axis='y', which='major', labelsize=15)
    ax[0].set_title(ts_trace.station + ": " + ts_trace.network)
    fig.savefig(outfilename, bbox_inches="tight")
    plt.close(fig)
    return


def plot_many_traces(list_of_traces, outfile, normalized=False, logx=False, logy=False,
                     title=None, xmin=None, xmax=None):
    """
    Take a list of traces that you'd like to plot, and plot many of them on top of each other.
    This is intended for many events at a single station, or many events at many stations

    :return:
    """
    fig, ax = plt.subplots(figsize=(10, 3), dpi=300)
    if not title:  # if there's no title provided, we create one by default.
        title = list_of_traces[0].station + ":" + list_of_traces[0].network + ', n='+str(len(list_of_traces))
    for trace in list_of_traces:
        timedeltas = trace.t - trace.t[0]
        seconds = timedeltas.total_seconds()
        plotting_function = trace.slip_mm-trace.slip_mm[0]
        t_hours = seconds / 3600
        time_axis = t_hours
        total_displacement = max(plotting_function)
        if normalized:
            plotting_function = plotting_function / total_displacement
        # Mask to avoid log(0), negatives, and NaNs for log plotting
        m = np.isfinite(time_axis) & np.isfinite(plotting_function) & (time_axis > 0) & (plotting_function > 0)
        ax.plot(time_axis[m], plotting_function[m], label=trace.station, linewidth=0.40)
        ax.set_xlabel('Time since start (hr)')
        if xmin is not None:
            ax.set_xlim([xmin, xmax])
        else:
            pass
        if normalized:
            ax.set_ylabel('Normalized Displacement')
        else:
            ax.set_ylabel('Displacement (mm)')
        ax.set_title(title)
        if logx:
            ax.set_xscale('log')
        if logy:
            ax.set_yscale('log')
    fig.savefig(outfile, bbox_inches="tight")
    plt.close(fig)
    return


def plot_many_velocities(list_of_traces, outfilename, xmin=None, xmax=None):
    """
    Plot the velocity of many creep event snippets

    :param list_of_traces: many time series of type ts_obj
    :param outfilename: string
    :param xmin: default None.
    :param xmax: default None.
    """
    fig, ax = plt.subplots(2, 1, figsize=(10, 6), dpi=300, sharex=True)
    for trace in list_of_traces:
        timedeltas = trace.t - trace.t[0]
        seconds = timedeltas.total_seconds()
        plotting_function = trace.slip_mm-trace.slip_mm[0]
        t_hours = seconds / 3600
        time_axis = t_hours
        ax[0].plot(time_axis, plotting_function, linewidth=0.40)
        ax[0].set_ylabel('Displacement (mm)', fontsize=15)

        tvel, vel = trace.get_velocity()

        ax[1].plot(time_axis[0:-1], vel, linewidth=0.40)
        ax[1].set_ylabel('Velocity (m/s)', fontsize=15)
        fig.tight_layout()
        ax[1].tick_params(axis='x', which='major', labelsize=15)
        ax[1].tick_params(axis='y', which='major', labelsize=15)
        ax[1].set_xlabel('Time since start (hr)', fontsize=15)
        ax[1].set_yscale('log')
    ax[0].set_title(list_of_traces[0].station + ": " + list_of_traces[0].network)
    if xmin is not None:
        ax[1].set_xlim([xmin, xmax])
    fig.savefig(outfilename, bbox_inches="tight")
    plt.close(fig)
    return
