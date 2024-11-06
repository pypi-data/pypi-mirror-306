"""
Define parameters of figure axes.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Callable, Literal

from matplotlib import transforms
from matplotlib.axes import Axes
from matplotlib.text import Text


def set_axis(
    ax: Axes,
    axis_name: str,
    major_ticks: Sequence | None = None,
    minor_ticks: Sequence | None = None,
    limits: tuple | None = None,
    spine_bounds: tuple | None = None,
):
    """
    Set ticks and bounds of axis.

    If spine_bounds is not set, the spine will extend to the first and last
    ticks, if they are set, otherwise to the axis limits.
    """
    # Set relevant methods depending on choice of x or y axis
    if axis_name == "x":
        set_ticks = ax.set_xticks
        set_limits = ax.set_xlim
        get_limits = ax.get_xlim
        convert_units = _make_mapping_function(ax.convert_xunits)
        spine_locations = ["bottom", "top"]
    elif axis_name == "y":
        set_ticks = ax.set_yticks
        set_limits = ax.set_ylim
        get_limits = ax.get_ylim
        convert_units = _make_mapping_function(ax.convert_yunits)
        spine_locations = ["left", "right"]
    else:
        raise ValueError("Axis name {} is not valid, should be x or y.")

    # Convert all units to axis units (floats)
    # This avoids problems with dates, for instance
    major_ticks = convert_units(major_ticks)
    minor_ticks = convert_units(minor_ticks)
    limits = convert_units(limits)
    spine_bounds = convert_units(spine_bounds)

    # Define minimal limits based on ticks
    if major_ticks or minor_ticks:
        min_candidates = []
        max_candidates = []
        if major_ticks:
            min_candidates.append(major_ticks[0])
            max_candidates.append(major_ticks[-1])
        if minor_ticks:
            min_candidates.append(minor_ticks[0])
            max_candidates.append(minor_ticks[-1])
        minimal_limits = min(min_candidates), max(max_candidates)
    else:
        minimal_limits = None

    # Define axis limits
    if limits is None:
        if minimal_limits is not None:
            limits = minimal_limits
        else:
            limits = get_limits()

    # Define spine bounds
    if spine_bounds is None:
        # If ticks are set, extend to first and last tick
        if minimal_limits is not None:
            spine_bounds = minimal_limits
        else:
            spine_bounds = limits

    # Set ticks
    if major_ticks is not None:
        set_ticks(major_ticks)
    if minor_ticks is not None:
        set_ticks(minor_ticks, minor=True)

    # Set spine bounds
    for loc in spine_locations:
        ax.spines[loc].set_bounds(*spine_bounds)

    # Set plotting limits
    set_limits(limits)


def _make_mapping_function(func) -> Callable[[Sequence | None], list | None]:
    def map_function(series: Sequence | None) -> list | None:
        if series is None:
            return
        return [func(x) for x in series]

    return map_function


@dataclass
class AxisLabelParams:
    """
    Define parameters for axis label position.

    The attribute `transform` is the coordinate system in which the label is placed,
    by the axis method `set_label_coords`.
    """

    verticalalignment: str
    horizontalalignment: str
    rotation: str
    rotation_mode: str
    x: Callable[[float], float]
    y: Callable[[float], float]
    transform: Callable[[Axes], transforms.Transform]

    def __call__(self, ax: Axes, label_pad: float) -> dict[str, Any]:
        return {
            "horizontalalignment": self.horizontalalignment,
            "verticalalignment": self.verticalalignment,
            "rotation": self.rotation,
            "rotation_mode": self.rotation_mode,
            "x": self.x(label_pad),
            "y": self.y(label_pad),
            "transform": self.transform(ax),
        }


def move_to_ax_origin(ax: Axes):
    return transforms.ScaledTranslation(0, 0, ax.transAxes)


def move_to_top_yaxis(ax: Axes):
    return transforms.ScaledTranslation(0, 1, ax.transAxes)


def move_to_ax_top(ax: Axes):
    return transforms.ScaledTranslation(0.5, 1, ax.transAxes)


label_preset_library = {
    "x": {
        "center": AxisLabelParams(
            verticalalignment="baseline",
            horizontalalignment="center",
            rotation="horizontal",
            rotation_mode="anchor",
            transform=lambda ax: transforms.blended_transform_factory(
                ax.transAxes,
                getattr(ax.get_figure(), "trans_unit_to_display")
                + move_to_ax_origin(ax),
            ),
            x=lambda label_pad: 0.5,
            y=lambda label_pad: -label_pad,
        ),
        "right": AxisLabelParams(
            verticalalignment="baseline",
            horizontalalignment="right",
            rotation="horizontal",
            rotation_mode="anchor",
            transform=lambda ax: transforms.blended_transform_factory(
                ax.transAxes,
                getattr(ax.get_figure(), "trans_unit_to_display")
                + move_to_ax_origin(ax),
            ),
            x=lambda label_pad: 1,
            y=lambda label_pad: -label_pad,
        ),
    },
    "y": {
        "center": AxisLabelParams(
            verticalalignment="baseline",
            horizontalalignment="center",
            rotation="vertical",
            rotation_mode="anchor",
            transform=lambda ax: transforms.blended_transform_factory(
                getattr(ax.get_figure(), "trans_unit_to_display")
                + move_to_ax_origin(ax),
                ax.transAxes,
            ),
            x=lambda label_pad: -label_pad,
            y=lambda label_pad: 0.5,
        ),
        "side": AxisLabelParams(
            verticalalignment="center",
            horizontalalignment="right",
            rotation="horizontal",
            rotation_mode="anchor",
            transform=lambda ax: transforms.blended_transform_factory(
                getattr(ax.get_figure(), "trans_unit_to_display")
                + move_to_ax_origin(ax),
                ax.transAxes,
            ),
            x=lambda label_pad: -label_pad,
            y=lambda label_pad: 0.5,
        ),
        "top": AxisLabelParams(
            verticalalignment="baseline",
            horizontalalignment="right",
            rotation="vertical",
            rotation_mode="anchor",
            transform=lambda ax: getattr(ax.get_figure(), "trans_unit_to_display")
            + move_to_top_yaxis(ax),
            x=lambda label_pad: -label_pad,
            y=lambda label_pad: 0,
        ),
        "above": AxisLabelParams(
            verticalalignment="baseline",
            horizontalalignment="center",
            rotation="horizontal",
            rotation_mode="anchor",
            transform=lambda ax: getattr(ax.get_figure(), "trans_unit_to_display")
            + move_to_top_yaxis(ax),
            x=lambda label_pad: 0,
            y=lambda label_pad: label_pad,
        ),
        "above_center": AxisLabelParams(
            verticalalignment="baseline",
            horizontalalignment="center",
            rotation="horizontal",
            rotation_mode="anchor",
            transform=lambda ax: getattr(ax.get_figure(), "trans_unit_to_display")
            + move_to_ax_top(ax),
            x=lambda label_pad: 0,
            y=lambda label_pad: label_pad,
        ),
        "above_right": AxisLabelParams(
            verticalalignment="baseline",
            horizontalalignment="left",
            rotation="horizontal",
            rotation_mode="anchor",
            transform=lambda ax: getattr(ax.get_figure(), "trans_unit_to_display")
            + move_to_top_yaxis(ax),
            x=lambda label_pad: 0,
            y=lambda label_pad: label_pad,
        ),
        "above_left": AxisLabelParams(
            verticalalignment="baseline",
            horizontalalignment="right",
            rotation="horizontal",
            rotation_mode="anchor",
            transform=lambda ax: getattr(ax.get_figure(), "trans_unit_to_display")
            + move_to_top_yaxis(ax),
            x=lambda label_pad: 0,
            y=lambda label_pad: label_pad,
        ),
        "above_side": AxisLabelParams(
            verticalalignment="center",
            horizontalalignment="left",
            rotation="horizontal",
            rotation_mode="anchor",
            transform=lambda ax: getattr(ax.get_figure(), "trans_unit_to_display")
            + move_to_top_yaxis(ax),
            x=lambda label_pad: label_pad,
            y=lambda label_pad: 0,
        ),
        "top_right": AxisLabelParams(
            verticalalignment="center",
            horizontalalignment="left",
            rotation="horizontal",
            rotation_mode="anchor",
            transform=lambda ax: getattr(ax.get_figure(), "trans_unit_to_display")
            + move_to_top_yaxis(ax),
            x=lambda label_pad: label_pad,
            y=lambda label_pad: 0,
        ),
        "top_left": AxisLabelParams(
            verticalalignment="center",
            horizontalalignment="right",
            rotation="horizontal",
            rotation_mode="anchor",
            transform=lambda ax: getattr(ax.get_figure(), "trans_unit_to_display")
            + move_to_top_yaxis(ax),
            x=lambda label_pad: -label_pad,
            y=lambda label_pad: 0,
        ),
    },
}
"""
Library of axis label presets.
"""


def set_axis_label(
    ax: Axes,
    axis_name: Literal["x", "y"],
    text: str,
    preset: str | AxisLabelParams,
    label_pad: float,
) -> Text:
    """
    Set axis label and position.

    :param ax: Axes object.
    :param axis_name: 'x' or 'y'.
    :param text: Text of the label.
    :param preset: An AxisLabelParams object, or the name of a label preset available in
        the library.
    :param label_pad: number of base units to offset the text by. The base unit is
        defined at figure creation, and a transform is saved in the Figure object.
    :returns: The label object.
    """
    if axis_name == "x":
        axis = ax.xaxis
    elif axis_name == "y":
        axis = ax.yaxis
    else:
        raise ValueError(f"Axis name {axis_name} is not valid.")

    # Retrieve parameters for label position
    if isinstance(preset, str):
        preset = label_preset_library[axis_name][preset]
    args = preset(ax, label_pad)

    axis.set_label_coords(args["x"], args["y"], transform=args["transform"])
    text_args = [
        "verticalalignment",
        "horizontalalignment",
        "rotation",
        "rotation_mode",
    ]
    label = axis.set_label_text(text, **{k: args[k] for k in text_args})

    return label
