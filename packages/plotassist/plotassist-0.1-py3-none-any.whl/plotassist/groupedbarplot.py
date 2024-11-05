# groupedbarplot.py

# A class for creating a grouped bar plot in Matplotlib.

# imports
from typing import Any
import matplotlib as mpl
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.colors import Colormap


class GroupedBarPlot:
    """
    A class to create grouped bar plots using Matplotlib.

    Attributes:
    -----------
    df : pd.DataFrame
        The dataframe containing the data to plot.
    group_key : object
        The key to group the data by.
    colormap : Union[str, Colormap]
        The colormap to use for the bars.
    label_dict : Dict[object, str], optional
        A dictionary mapping column names to labels for the legend.

    Methods:
    --------
    calc_axis_params() -> Dict[str, float]:
        Calculate default axis parameters for the plot.
    create_plot(ax: Axes, axis_param_dict: Dict[str, float] = None, **bar_kwargs: Any) -> None:
        Create the grouped bar plot on the given Axes object.
    """

    def __init__(self, df: pd.DataFrame, colormap: str | Colormap = 'tab10', label_dict: dict[object, str] = None):
        """
        Initialize the GroupedBarPlot class.

        Parameters:
        -----------
        df : pd.DataFrame
            The dataframe containing the data to plot.
        group_key : object
            The key to group the data by.
        colormap : Union[str, Colormap], optional
            The colormap to use for the bars. Default is 'tab10'.
        label_dict : Dict[object, str], optional
            A dictionary mapping column names to labels for the legend.
        """
        # check that the dataframe has at least two columns
        if len(df.columns) < 2:
            raise ValueError("Dataframe must have at least two columns.")

        # check that each entry to index is unique
        if not df.index.is_unique:
            raise ValueError("Index of DataFrame must be unique.")

        # load the colormap
        if isinstance(colormap, str):
            self.colormap = mpl.colormaps[colormap]
        elif isinstance(colormap, Colormap):
            self.colormap = colormap
        else:
            raise ValueError("Colormap must be a string in mpl.colormaps or a matplotlib Colormap object.")

        # save variables
        self.df = df
        self.label_dict = label_dict


    def calc_axis_params(self) -> dict[str, float]:
        """
        Calculate default axis parameters for the plot.

        Returns:
        --------
        Dict[str, float]
            A dictionary containing default axis parameters.
        """
        # get the number of groups and list of categories
        group_num = self.df.index.nunique()
        categories = self.df.columns
        cat_num = len(categories)

        # define values for horizontal scaling
        min_x = 0
        max_x = 1

        group_padding = 0.2 / cat_num
        ax_padding = 1 / group_num

        group_width = ((max_x - min_x) / (group_num-1)) - group_padding
        bar_width = (group_width / cat_num)
        x_ticks = np.linspace(min_x, max_x, group_num)

        # create and return the dictionary of axis parameters
        return {
            'group_num': group_num,
            'categories': categories,
            'cat_num': cat_num,
            'min_x': min_x,
            'max_x': max_x,
            'group_padding': group_padding,
            'ax_padding': ax_padding,
            'group_width': group_width,
            'bar_width': bar_width,
            'x_ticks': x_ticks,
        }


    def create_plot(self, ax: Axes, axis_param_dict: dict[str, float] = None, **bar_kwargs: Any) -> None:
        """
        Create the grouped bar plot on the given Axes object.

        Parameters:
        -----------
        ax : Axes
            The Axes object to create the plot on.
        axis_param_dict : Dict[str, float], optional
            A dictionary containing axis parameters. If not provided, default parameters will be used.
        **bar_kwargs : Any
            Additional keyword arguments to pass to the ax.bar method.
        """
        # get the number of groups and list of categories
        categories = self.df.columns
        cat_num = len(categories)

        # get the param dict and ensure all keys are available
        if axis_param_dict:
            default_params = self.calc_axis_params()
            missing_keys = set(default_params.keys()) - set(axis_param_dict.keys())
            axis_param_dict.update({key: default_params[key] for key in missing_keys})
        else:
            axis_param_dict = self.calc_axis_params()

        # set horizontal labels
        x_ticks = axis_param_dict['x_ticks']
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(self.df.index)

        # set horizontal limits
        min_x = axis_param_dict['min_x']
        max_x = axis_param_dict['max_x']
        ax_padding = axis_param_dict['ax_padding']
        ax.set_xlim(min_x - ax_padding, max_x + ax_padding)

        # calculate the bar position offsets in each group
        group_width = axis_param_dict['group_width']
        bar_offsets = np.linspace(-group_width/2, group_width/2, len(categories))

        # iterate over the dataframe
        bar_width = axis_param_dict['bar_width']
        for i, (_, row_series) in enumerate(self.df.iterrows()):
            # get the horizontal placement of the group
            x_group = x_ticks[i]

            # iterate over the categories
            for j, category in enumerate(categories):
                # get the value from row_series
                value = row_series[category]

                # attempt to get the label from the label dict
                label = category
                if self.label_dict:
                    label = self.label_dict.get(category, category)

                # get the color and handle errors
                try:
                    color = self.colormap(j)
                except ValueError as e:
                    raise ValueError(f"Colormap must have at least {cat_num} colors.") from e

                # calculate the x position of the bar
                x_pos = x_group + bar_offsets[j]/2
                ax.bar(
                    x_pos,
                    value,
                    width=bar_width,
                    color=color,
                    label=label,
                    **bar_kwargs
                )
