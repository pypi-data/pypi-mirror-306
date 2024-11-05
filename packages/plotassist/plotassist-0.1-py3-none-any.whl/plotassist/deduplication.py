# deduplication.py

# A function for deduplicating legend entries in Matplotlib.

from typing import Any
from matplotlib.axes import Axes


def deduplicate_legend(ax: Axes, **legend_kwargs: Any) -> None:
    """
    Deduplicate legend entries for the given Axes object.

    Parameters:
    ax (Axes): The Axes object to deduplicate legend entries for.
    **legend_kwargs: Additional keyword arguments to pass to ax.legend.
    """
    # get the current legend handles and labels
    handles, labels = ax.get_legend_handles_labels()

    # create a dictionary to deduplicate labels
    by_label = dict(zip(labels, handles))

    # set the legend with deduplicated entries
    ax.legend(by_label.values(), by_label.keys(), **legend_kwargs)
