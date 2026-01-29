import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def simple_plot(ts_trace, outfilename):
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
