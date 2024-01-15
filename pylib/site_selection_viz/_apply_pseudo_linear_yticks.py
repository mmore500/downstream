import warnings

from matplotlib import axes as mpl_axes

from ..round_to_one_sigfig import round_to_one_sigfig


def apply_pseudo_linear_yticks(ax: mpl_axes.Axes) -> mpl_axes.Axes:
    # Replace categorical y-axis labels with (pseudo) linear axis
    maxval = max(int(label.get_text()) for label in ax.get_yticklabels())
    precision = round_to_one_sigfig(maxval // 10)
    if precision == 0:
        warnings.warn("Precision is 0, aborting pseudo-linear y-axis labeling")
        return ax
    ax.set_yticklabels(
        [
            r"{:.1e}".format(
                (int(label.get_text()) // precision) * precision,
            )
            for label in ax.get_yticklabels()
        ],
    )

    # Get the current ticks and labels
    ticks = ax.get_yticks()
    labels = [label.get_text() for label in ax.get_yticklabels()]

    # Create a dictionary from ticks and labels.
    # This will automatically remove duplicates because keys in a dictionary
    # must be unique.
    unique_ticks_and_labels = dict(reversed([*zip(labels, ticks)]))
    assert len(unique_ticks_and_labels) <= len(labels)

    # Set the ticks and labels
    ax.set_yticks([*reversed([*unique_ticks_and_labels.values()])])
    ax.set_yticklabels([*reversed([*unique_ticks_and_labels.keys()])])
    return ax
