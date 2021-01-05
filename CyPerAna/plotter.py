from collections.abc import KeysView, ValuesView
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt

color_maps = {"orange": ["orangered", "darkorange", "orange"],
             "red": ["darkred", "red", "orangered"],
             "blue":  ["midnightblue", "darkblue", "royalblue"],
             "green": ["darkgreen", "green", "limegreen"],
             "sky": ["navy", "darkcyan", "aquamarine"],
             "sunset": ["darkcyan", "mediumslateblue", "deeppink"]}

rescale = lambda scale: (scale - np.min(scale)) / (np.max(scale) - np.min(scale))


def uniform_colormap(color, scale):
    color_list = color_maps[color]
    return LinearSegmentedColormap.from_list("", color_list)(rescale(scale))


def x_bar(x_container):
    if isinstance(x_container, KeysView):
        return list(x_container)


def y_bar(y_container):
    if isinstance(y_container, ValuesView):
        return list(y_container)


class Plotter:

    def __init__(self, figsize=(16, 9)):
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.fig.set_size_inches(figsize[0], figsize[1], forward=True)
        self.ax.grid(axis="y")
        self.xlabelsize = None
        self.ticksize = None

    def configure_parameters(self, **kwargs):
        self.xlabelsize = kwargs.get("xlabelsize", 16)
        self.ticksize = kwargs.get("ticksize", 14)

    def plot_bar(self, x, y, color, xlabel):
        self.ax.barh(x, y, color=uniform_colormap(color, y), alpha=0.85)
        self.ax.set_axisbelow(True)
        self.ax.set_xlabel(xlabel, size=self.xlabelsize)
        self.ax.tick_params(size=self.ticksize)

    def show(self):
        plt.show()
