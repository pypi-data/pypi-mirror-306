import matplotlib.pyplot as plt

from .axes import AxisLabelParams, set_axis, set_axis_label
from .layouts import Layout, make_figure
from .styles import style

__all__ = [
    "make_figure",
    "style",
    "set_axis",
    "set_axis_label",
    "Layout",
    "AxisLabelParams",
]

plt.style.use("main")
