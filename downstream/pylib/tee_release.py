from hstrat import _auxiliary_lib as hstrat_aux
from matplotlib import pyplot as plt
from teeplot import teeplot as tp


def tee_release(*args, **kwargs):
    res = tp.tee(*args, **kwargs)
    plt.show()
    hstrat_aux.release_cur_mpl_fig()
    return res
