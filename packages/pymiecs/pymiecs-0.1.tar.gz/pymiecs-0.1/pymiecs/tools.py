# Mie observables
# %%
import warnings

import numpy as np
from pymiecs.mie_coeff import core_shell_ab

def get_plot_axis_existing_or_new():
    import matplotlib.pyplot as plt

    if len(plt.get_fignums()) == 0:
        show = True
        ax = plt.subplot()
    else:
        show = False
        ax = plt.gca()
    return ax, show