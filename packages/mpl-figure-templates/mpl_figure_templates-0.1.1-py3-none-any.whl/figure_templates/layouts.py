"""
Define layout of figures and subplots.
"""

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import yaml
from matplotlib import transforms
from matplotlib.figure import Figure

from .axes import AxisLabelParams, set_axis_label
from .config import find_config_directories


@dataclass
class Layout:
    """
    Figure layout parameters.
    """

    num_rows: int
    num_cols: int
    fig_width: float
    fig_height: float
    margin_top: float
    margin_bottom: float
    margin_left: float
    margin_right: float
    hsep: float
    vsep: float
    is_framed: bool
    spine_shift: float
    base_unit: int
    xlabel_preset: str | AxisLabelParams
    xlabel_pad: float
    ylabel_preset: str | AxisLabelParams
    ylabel_pad: float

    @classmethod
    def from_yml(cls, path: Path):
        """
        Initialize layout from a YAML file.
        """
        with open(path) as f:
            parameters = yaml.safe_load(f)

        return cls(**parameters)

    def asdict(self) -> dict[str, Any]:
        return asdict(self)


def in2pt(x: float) -> int:
    return round(x * 72)


def _make_figure(
    num_rows: int = 1,
    num_cols: int = 1,
    fig_width: float = 6.0,
    fig_height: float = 4.0,
    margin_top: float = 0.2,
    margin_bottom: float = 0.5,
    margin_left: float = 1.0,
    margin_right: float = 0.2,
    hsep: float = 1.0,
    vsep: float = 1.0,
    is_framed: bool = True,
    spine_shift: float = 0.2,
    base_unit: int = 72,
    xlabel_preset: str | AxisLabelParams = "center",
    xlabel_pad: float = 0.5,
    ylabel_preset: str | AxisLabelParams = "top_right",
    ylabel_pad: float = 0.5,
) -> Figure:
    units_by_inch = 72 / base_unit

    # Convert measures to inches
    fig_width /= units_by_inch
    fig_height /= units_by_inch
    margin_top /= units_by_inch
    margin_bottom /= units_by_inch
    margin_left /= units_by_inch
    margin_right /= units_by_inch
    hsep /= units_by_inch
    vsep /= units_by_inch
    spine_shift /= units_by_inch

    # Set axes size
    ax_width = (
        fig_width - margin_left - margin_right - (num_cols - 1) * hsep
    ) / num_cols
    ax_height = (
        fig_height - margin_top - margin_bottom - (num_rows - 1) * vsep
    ) / num_rows

    # Create figure
    fig = plt.figure(figsize=(fig_width, fig_height))

    # Add transformation from coordinates in base units
    trans_unit_to_inches = transforms.BboxTransformTo(
        transforms.Bbox([[0, 0], [base_unit / 72, base_unit / 72]])
    )
    fig.trans_unit_to_display = trans_unit_to_inches + fig.dpi_scale_trans

    num_axes = num_cols * num_rows
    for n_ax in range(num_axes):
        n_row = 1 + n_ax // num_cols
        n_col = 1 + n_ax % num_cols

        # Set axes position
        ax_left = margin_left + spine_shift + (n_col - 1) * (ax_width + hsep)
        ax_bottom = (
            fig_height
            - margin_top
            + spine_shift
            - n_row * ax_height
            - (n_row - 1) * vsep
        )
        rect = (
            ax_left / fig_width,
            ax_bottom / fig_height,
            (ax_width - spine_shift) / fig_width,
            (ax_height - spine_shift) / fig_height,
        )

        # Add axes
        ax = fig.add_axes(rect, frameon=is_framed)
        set_axis_label(ax, "x", "", xlabel_preset, xlabel_pad)
        set_axis_label(ax, "y", "", ylabel_preset, ylabel_pad)

        # Shift spines. Note that shifting is not supposed to be used when
        # top and right spines are visible.
        for loc in ["left", "bottom"]:
            ax.spines[loc].set_position(("outward", in2pt(spine_shift)))

    return fig


def make_figure(
    template: str | Layout,
    num_rows: int | None = None,
    num_cols: int | None = None,
    fig_width: float | None = None,
    fig_height: float | None = None,
    margin_top: float | None = None,
    margin_bottom: float | None = None,
    margin_left: float | None = None,
    margin_right: float | None = None,
    hsep: float | None = None,
    vsep: float | None = None,
    is_framed: bool | None = None,
    spine_shift: float | None = None,
    base_unit: int | None = None,
    xlabel_preset: str | AxisLabelParams | None = None,
    xlabel_pad: float | None = None,
    ylabel_preset: str | AxisLabelParams | None = None,
    ylabel_pad: float | None = None,
) -> Figure:
    """
    Create a figure with the specified layout.

    :param template: Layout template name or Layout object.
    :param num_rows: Number of axis rows.
    :param num_cols: Number of axis columns.
    :param fig_width: Figure width in inches.
    :param fig_height: Figure height in inches.
    :param margin_top: Top margin in base units.
    :param margin_bottom: Bottom margin in base units.
    :param margin_left: Left margin in base units.
    :param margin_right: Right margin in base units.
    :param hsep: Horizontal separation between axes in base units.
    :param vsep: Vertical separation between axes in base units.
    :param is_framed: Whether axes are framed.
    :param spine_shift: Shift of axis spines in base units.
    :param base_unit: Base unit in points.
    :param xlabel_preset: The name of an X-axis label preset, or an AxisLabelParams
        object.
    :param xlabel_pad: Padding between the X-axis and its label.
    :param ylabel_preset: The name of a Y-axis label preset, or an AxisLabelParams
        object.
    :param ylabel_pad: Padding between the Y-axis and its label.

    :return: Figure object.
    """
    if isinstance(template, Layout):
        parameters = template.asdict()
    else:
        parameters = library[template].asdict()

    optional_args = {
        "num_rows": num_rows,
        "num_cols": num_cols,
        "fig_width": fig_width,
        "fig_height": fig_height,
        "margin_top": margin_top,
        "margin_bottom": margin_bottom,
        "margin_left": margin_left,
        "margin_right": margin_right,
        "hsep": hsep,
        "vsep": vsep,
        "is_framed": is_framed,
        "spine_shift": spine_shift,
        "base_unit": base_unit,
        "xlabel_preset": xlabel_preset,
        "xlabel_pad": xlabel_pad,
        "ylabel_preset": ylabel_preset,
        "ylabel_pad": ylabel_pad,
    }
    args_with_value = {
        arg: value for arg, value in optional_args.items() if value is not None
    }

    parameters.update(args_with_value)

    return _make_figure(**parameters)


def read_layout_directory(layout_dir: Path) -> dict[str, Layout]:
    """
    Return dictionary of layouts defined in *layout_dir*.
    """
    layouts = dict()
    for path in Path(layout_dir).glob("*.yml"):
        layouts[path.stem] = Layout.from_yml(path)

    return layouts


def reload_layouts():
    """
    Load layouts
    """
    # Clear the library, caching the layout objects
    library.clear()

    # Populate the library with the layouts found in the config directories
    layout_dirs = find_config_directories("layouts")
    for path in layout_dirs:
        layouts_in_directory = read_layout_directory(path)
        library.update(layouts_in_directory)


library: dict[str, Layout] = {}
"""
Library of layout templates.
"""

reload_layouts()
