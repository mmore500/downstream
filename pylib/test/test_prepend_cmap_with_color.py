from matplotlib import colors as mpl_colors

import pylib


def test_prepend_cmap_with_color():
    augmented_colormap = pylib.prepend_cmap_with_color("viridis", "red")

    # Check the type of the returned colormap
    assert isinstance(augmented_colormap, mpl_colors.ListedColormap)

    # Check if the first color in the colormap is the one we prepended
    # 'red' should be approximately (1, 0, 0, 1) in RGBA
    assert (augmented_colormap.colors[0] == [1.0, 0.0, 0.0, 1.0]).all()
