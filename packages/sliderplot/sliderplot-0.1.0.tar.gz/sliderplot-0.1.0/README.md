# sliderplot

![PyPI - Downloads](https://img.shields.io/pypi/dm/sliderplot)

Turn a function into an interactive plot with a single line of code.

It is very similar to [Holoviews DynamicMap](https://holoviews.org/reference/containers/bokeh/DynamicMap.html) but with
multiple lines and
plots capabilities, and with only sliders as interactive elements.

```
pip install sliderplot
```

# Demo

<p align="center">
    <img src="https://github.com/ngripon/sliderplot/raw/main/demo.gif" width="800" alt="demo" />
</p>

``` python
from sliderplot import sliderplot
import numpy as np


def f(amplitude=1, frequency=np.pi, phase=np.pi / 2):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return x, y, "Hey"


sliderplot(
    f,
    params_bounds=((0, 1),),
    titles=("Minimal example",),
    page_title="Minimal example",
)
```

# Features

- [Single line](#single-line)
- [Multiple lines](#multiple-lines)
- [Multiple subplots](#multiple-subplots)
- [Line labels](#line-labels)
- [Initial slider position](#initial-slider-position)
- [Slider bounds settings](#slider-bounds-settings)
- [Axes labels](#axes-labels)
- [Plot title](#plot-title)
- [Web page title](#web-page-title)

## Single line

To create a sliderplot with a single line, pass into `sliderplot()` a function that returns same-length `x` and `y`
vectors.

### Example

``` python
def f(amplitude, frequency, phase):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return x, y


sliderplot(f)
```

## Multiple lines

To create a sliderplot with multiple lines, pass into `sliderplot()` a function that returns multiple pairs of
same-length `x` and `y` vectors.

### Example

``` python
def f(amplitude, frequency, phase):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return (x, y), (x, 2 * y), (x, 3 * y)


sliderplot(f)
```

## Multiple subplots

To create a sliderplot with multiple subplots, pass into `sliderplot()` a function that returns a list with the
following levels, top to bottom:

1. List of subplots.
2. List of lines.
3. Line: `(x, y)` pair of same-length vectors, or `(x, y, label: str)` to add a line label.

### Example

``` python
def f(amplitude, frequency, phase):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return ((x, y), (x, 2 * y)), ((x, 3 * y),)


sliderplot(f)
```

## Line labels

To add a label to a line that will be displayed in the plot legend, return the line data with the following format:

`(x, y, label: str)`

### Example

``` python
def f(amplitude, frequency, phase):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return (x, y, "First"), (x, 2 * y), (x, 3 * y, "Third")


sliderplot(f)
```

## Initial slider position

To set the slider initial value for a parameter, simply add a default argument to the function.

### Example

In the following example, the initial slider values are:

- `amplitude = 1`
- `frequency = np.pi`
- `phase = np.pi / 2`

``` python
def f(amplitude=1, frequency=np.pi, phase=np.pi / 2):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return x, y


sliderplot(f)
```

## Slider bounds settings

Use the `param_bounds` argument of the `sliderplot()` function to specify the slider bounds of each parameter. It takes
a list of pairs of `(min_value, max_value)`.

The first pair contains the bounds of the first argument, the second pair
contains the bounds of the second argument, etc...

### Example

In the following example, the slider bounds are:

- `amplitude = (0, 1)`
- `frequency = (1, 1000)`
- `phase = (0, np.pi)`

``` python
def f(amplitude, frequency, phase):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return x, y


sliderplot(f, params_bounds=((0, 1), (1, 1000), (0, np.pi)))
```

## Axes labels

To add axes labels to the subplots, set the `axes_labels` argument with a sequence of `(x_label, y_label)` pair of
strings. The first
pair will set the axis labels of the first subplot, the second pair the axis labels of the second subplot, etc...

### Example

``` python
def f(amplitude, frequency, phase):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return ((x, y), (x, 2 * y)), ((x, 3 * y),)


sliderplot(f, axes_labels=(("x1", "y1"), ("x2", "y2")))
```

## Plot title

To add plot titles to subplots, set the `titles` argument with a sequence of strings. The first
string will be the title of the first subplot, the second string the title of the second subplot, etc...

### Example

``` python
def f(amplitude, frequency, phase):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return ((x, y), (x, 2 * y)), ((x, 3 * y),)


sliderplot(f, titles=("Subplot 1", "Subplot2"))
```

## Web page title

To set the title of the web page that show the sliderplot, use the `page_title` argument.

``` python
def f(amplitude=1, frequency=np.pi, phase=np.pi / 2):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return x, y


sliderplot(f, page_title="Page title")
```
