from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap, to_rgba
import numpy as np
import seaborn as sns


def prepend_cmap_with_color(
    cmap_name: str,
    color_name: str,
) -> ListedColormap:
    cmap = plt.cm.get_cmap(cmap_name, 256)
    cmap_colors = cmap(np.linspace(0, 1, 256))
    color = to_rgba(color_name)
    augmented_colors = np.vstack((color, cmap_colors))
    augmented_colormap = ListedColormap(augmented_colors)
    return augmented_colormap
