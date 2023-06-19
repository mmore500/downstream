from matplotlib import axes as mpl_axes
import numpy as np


def apply_pseudo_log_yticks(ax: mpl_axes.Axes) -> mpl_axes.Axes:
    # Replace categorical y-axis labels with (pseudo) log axis
    ax.set_yticklabels(
        [
            "$10^{{{}}}$".format(int(np.log10(float(label.get_text()))))
            for label in ax.get_yticklabels()
        ],
    )

    # Get the current ticks and labels
    ticks = ax.get_yticks()
    labels = [label.get_text() for label in ax.get_yticklabels()]

    # Create a dictionary from ticks and labels.
    # This will automatically remove duplicates because keys in a dictionary must be unique.
    unique_ticks_and_labels = dict(reversed([*zip(labels, ticks)]))
    assert len(unique_ticks_and_labels) < len(labels)

    # Set the ticks and labels
    ax.set_yticks([*reversed([*unique_ticks_and_labels.values()])])
    ax.set_yticklabels([*reversed([*unique_ticks_and_labels.keys()])])
    return ax
