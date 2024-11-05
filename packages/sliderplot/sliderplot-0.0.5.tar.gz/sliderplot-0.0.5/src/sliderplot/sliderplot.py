import enum
import itertools
from collections.abc import Sequence
from numbers import Number

import numpy as np
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, HoverTool, LegendItem, Legend
from bokeh.plotting import figure
from bokeh.palettes import d3

_SLIDER_HEIGHT = 0.05
_BOTTOM_PADDING = (0.03, 0.1)


class _PlotMode(enum.Enum):
    LINE_X = 0
    LINE_XY = 1
    MULTI_LINE = 2
    MULTI_PLOT = 3


def _get_plot_mode(output_data) -> _PlotMode:
    plot_mode_map = {0: _PlotMode.LINE_X, 1: _PlotMode.LINE_XY, 2: _PlotMode.MULTI_LINE, 3: _PlotMode.MULTI_PLOT}
    depth = _compute_depth(output_data)
    if depth in plot_mode_map.keys():
        return plot_mode_map[depth]
    else:
        raise Exception("Failed to transform the output data of the function into plots. "
                        "Please look at the documentation for correct data formatting.")


def _compute_depth(data) -> int:
    if not hasattr(data[0], "__len__"):
        return 0
    to_visit = [(data, 0)]
    depth_list = []
    while len(to_visit):
        current_el, current_depth = to_visit.pop()
        for child_el in current_el:
            if hasattr(child_el[0], "__len__") and not isinstance(child_el[0], str):
                to_visit.append((child_el, current_depth + 1))
            else:
                depth_list.append(current_depth + 1)
    if not all(depth == depth_list[0] for depth in depth_list):
        raise ValueError(
            "Wrong output format for the given function.\n"
            f"All elements must have the same depth, but elements have the following depths: {depth_list}.\n"
            "Please check the documentation for correct format examples.")
    return depth_list[0]


def _create_bokeh_plot(outputs, titles=(), labels_list=()):
    lines_source = []
    plot_mode = _get_plot_mode(outputs)
    if plot_mode is _PlotMode.MULTI_PLOT:
        figs = []
        for subplot_idx, subplot_data in enumerate(outputs):
            # Manage aesthetics
            title = titles[subplot_idx] if subplot_idx < len(titles) else None
            labels = labels_list[subplot_idx] if subplot_idx < len(labels_list) else ()
            # Create lines
            sub_fig, sub_line_sources = _create_bokeh_multiline_figure(subplot_data, title, labels)
            lines_source.extend(sub_line_sources)
            figs.append(sub_fig)
        fig = column(*figs)
    else:
        title = titles[0] if len(titles) else None
        labels = labels_list[0] if len(labels_list) else ()
        if plot_mode is _PlotMode.MULTI_LINE:
            fig, lines_source = _create_bokeh_multiline_figure(outputs, title=title, labels=labels)
        elif plot_mode is _PlotMode.LINE_XY:
            legend = outputs[2] if len(outputs) > 2 else None
            fig, line_source, legend_item = _create_bokeh_figure(outputs[0], outputs[1], title=title, labels=labels,
                                                                 legend=legend)
            if legend_item is not None:
                fig.add_layout(Legend(items=[legend_item], click_policy="mute"))
            lines_source.append(line_source)
        elif plot_mode is _PlotMode.LINE_X:
            x = np.arange(len(outputs))
            fig, line_source, legend_item = _create_bokeh_figure(x, outputs, title=title, labels=labels)
            lines_source.append(line_source)
        else:
            raise Exception(f"This mode is not supported: {plot_mode}")
    return fig, lines_source, plot_mode


def _create_bokeh_multiline_figure(data: Sequence[tuple[Number, Number, str]], title: str, labels: tuple[str, str]):
    fig = None
    lines_sources = []
    legend_items = []
    colors = itertools.cycle(d3["Category20"][19])
    # Create lines
    for line_data in data:
        x, y = line_data[:2]
        legend = line_data[2] if len(line_data) > 2 else None
        fig, line_source, legend_item = _create_bokeh_figure(x, y, colors, fig=fig, title=title,
                                                             labels=labels, legend=legend)
        lines_sources.append(line_source)
        if legend_item is not None:
            legend_items.append(legend_item)
    fig.add_layout(Legend(items=legend_items, click_policy="mute"))
    return fig, lines_sources


TOOLTIPS = [
    ("x", "@x"),
    ("y", "@y")
]


def _create_bokeh_figure(x, y, colors=None, fig=None, title: str = None, labels: tuple[str, str] = (),
                         legend: str = None):
    line_source = ColumnDataSource(data=dict(x=x, y=y))
    if fig is None:
        fig = figure(tools="pan,reset,save, box_zoom,wheel_zoom", sizing_mode="stretch_both")
        fig.add_tools(HoverTool(tooltips=TOOLTIPS))
        if title is not None:
            fig.title.text = title
        for axis_idx, axis_label in enumerate(labels):
            if axis_label is None:
                continue
            if axis_idx == 0:
                fig.xaxis[0].axis_label = axis_label
            elif axis_idx == 1:
                fig.yaxis[0].axis_label = axis_label
            else:
                break
    r = fig.line('x', 'y', source=line_source, line_width=3)
    if colors:
        r.glyph.line_color = next(colors)
        _ = next(colors)  # Trick to use last the uneven colors of the palette
    legend_item = LegendItem(label=legend, renderers=[r]) if legend is not None else None
    return fig, line_source, legend_item


def _get_lines(outputs, plot_mode: _PlotMode):
    if plot_mode is _PlotMode.MULTI_LINE:
        return (x[:2] for x in outputs)
    elif plot_mode is _PlotMode.LINE_XY:
        return ((outputs[0], outputs[1]),)
    elif plot_mode is _PlotMode.LINE_X:
        x = np.arange(len(outputs))
        return ((x, outputs),)
    elif plot_mode is _PlotMode.MULTI_PLOT:
        formatted_outputs = map(lambda l: [x[:2] for x in l], outputs)
        return np.concatenate((*formatted_outputs,))
    else:
        raise Exception("Invalid plot_mode argument.")
