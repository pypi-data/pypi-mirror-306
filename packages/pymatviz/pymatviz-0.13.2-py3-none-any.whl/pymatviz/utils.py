"""pymatviz utility functions."""

from __future__ import annotations

import re
import warnings
from collections.abc import Sequence
from contextlib import contextmanager
from functools import partial, wraps
from os.path import dirname
from typing import TYPE_CHECKING, Literal, TypeVar, cast, get_args

import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import scipy.stats
from matplotlib.colors import to_rgb
from matplotlib.offsetbox import AnchoredText
from matplotlib.ticker import FormatStrFormatter, PercentFormatter, ScalarFormatter
from pymatgen.core import Structure


if TYPE_CHECKING:
    from collections.abc import Callable, Generator
    from typing import Any, ParamSpec, TypeAlias

    from matplotlib.ticker import Formatter
    from numpy.typing import ArrayLike

    P = ParamSpec("P")  # generic type for function parameters
    R = TypeVar("R")  # generic type for return value

T = TypeVar("T")  # generic type for input validation

PKG_DIR = dirname(__file__)
ROOT = dirname(PKG_DIR)
TEST_FILES: str = f"{ROOT}/tests/files"
Backend: TypeAlias = Literal["matplotlib", "plotly"]
BACKENDS = MATPLOTLIB, PLOTLY = get_args(Backend)

AxOrFig: TypeAlias = plt.Axes | plt.Figure | go.Figure
VALID_FIG_TYPES = get_args(AxOrFig)
VALID_FIG_NAMES: str = " | ".join(
    f"{t.__module__}.{t.__qualname__}" for t in VALID_FIG_TYPES
)

CrystalSystem: TypeAlias = Literal[
    "triclinic",
    "monoclinic",
    "orthorhombic",
    "tetragonal",
    "trigonal",
    "hexagonal",
    "cubic",
]

elements_csv = f"{ROOT}/pymatviz/elements.csv"
df_ptable: pd.DataFrame = pd.read_csv(elements_csv, comment="#").set_index("symbol")
ElemValues: TypeAlias = dict[str | int, float] | pd.Series | Sequence[str]

atomic_numbers: dict[str, int] = {}
element_symbols: dict[int, str] = {}

for Z, symbol in enumerate(df_ptable.index, start=1):
    atomic_numbers[symbol] = Z
    element_symbols[Z] = symbol


class ExperimentalWarning(Warning):
    """Warning for experimental features."""


warnings.simplefilter("once", ExperimentalWarning)


def pretty_label(key: str, backend: Backend) -> str:
    """Map metric keys to their pretty labels."""
    if backend not in BACKENDS:
        raise ValueError(f"Unexpected {backend=}, must be one of {BACKENDS}")

    symbol_mapping = {
        "R2": {MATPLOTLIB: "$R^2$", PLOTLY: "R<sup>2</sup>"},
        "R2_adj": {
            MATPLOTLIB: "$R^2_{adj}$",
            PLOTLY: "R<sup>2</sup><sub>adj</sub>",
        },
    }

    return symbol_mapping.get(key, {}).get(backend, key)


def crystal_sys_from_spg_num(spg: float) -> CrystalSystem:
    """Get the crystal system for an international space group number."""
    # Ensure integer or float with no decimal part
    if not isinstance(spg, int | float) or spg != int(spg):
        raise TypeError(f"Expect integer space group number, got {spg=}")

    if not (1 <= spg <= 230):
        raise ValueError(f"Invalid space group number {spg}, must be 1 <= num <= 230")

    if 1 <= spg <= 2:
        return "triclinic"
    if spg <= 15:
        return "monoclinic"
    if spg <= 74:
        return "orthorhombic"
    if spg <= 142:
        return "tetragonal"
    if spg <= 167:
        return "trigonal"
    if spg <= 194:
        return "hexagonal"
    return "cubic"


def df_to_arrays(
    df: pd.DataFrame | None,
    *args: str | Sequence[str] | Sequence[ArrayLike],
    strict: bool = True,
) -> list[ArrayLike | dict[str, ArrayLike]]:
    """If df is None, this is a no-op: args are returned as-is. If df is a
    dataframe, all following args are used as column names and the column data
    returned as arrays (after dropping rows with NaNs in any column).

    Args:
        df (pd.DataFrame | None): Optional pandas DataFrame.
        *args (list[ArrayLike | str]): Arbitrary number of arrays or column names in df.
        strict (bool, optional): If True, raise TypeError if df is not pd.DataFrame
            or None. If False, return args as-is. Defaults to True.

    Raises:
        ValueError: If df is not None and any of the args is not a df column name.
        TypeError: If df is not pd.DataFrame and not None.

    Returns:
        list[ArrayLike | dict[str, ArrayLike]]: Array data for each column name or
            dictionary of column names and array data.
    """
    if df is None:
        if cols := [arg for arg in args if isinstance(arg, str)]:
            raise ValueError(f"got column names but no df to get data from: {cols}")
        # pass through args as-is
        return args  # type: ignore[return-value]

    if not isinstance(df, pd.DataFrame):
        if not strict:
            return args  # type: ignore[return-value]
        raise TypeError(f"df should be pandas DataFrame or None, got {type(df)}")

    if arrays := [arg for arg in args if isinstance(arg, np.ndarray)]:
        raise ValueError(
            "don't pass dataframe and arrays to df_to_arrays(), should be either or, "
            f"got {arrays}"
        )

    flat_args = []
    # tuple doesn't support item assignment
    args = list(args)  # type: ignore[assignment]

    for col_name in args:
        if isinstance(col_name, str | int):
            flat_args.append(col_name)
        else:
            flat_args.extend(col_name)

    df_no_nan = df.dropna(subset=flat_args)
    for idx, col_name in enumerate(args):
        if isinstance(col_name, str | int):
            args[idx] = df_no_nan[col_name].to_numpy()  # type: ignore[index]
        else:
            col_data = df_no_nan[[*col_name]].to_numpy().T
            args[idx] = dict(zip(col_name, col_data, strict=True))  # type: ignore[index]

    return args  # type: ignore[return-value]


def bin_df_cols(
    df_in: pd.DataFrame,
    bin_by_cols: Sequence[str],
    *,
    group_by_cols: Sequence[str] = (),
    n_bins: int | Sequence[int] = 100,
    bin_counts_col: str = "bin_counts",
    density_col: str = "",
    verbose: bool = True,
) -> pd.DataFrame:
    """Bin columns of a DataFrame.

    Args:
        df_in (pd.DataFrame): Input dataframe to bin.
        bin_by_cols (Sequence[str]): Columns to bin.
        group_by_cols (Sequence[str]): Additional columns to group by. Defaults to ().
        n_bins (int): Number of bins to use. Defaults to 100.
        bin_counts_col (str): Column name for bin counts. Defaults to "bin_counts".
        density_col (str): Column name for density values. Defaults to "".
        verbose (bool): If True, report df length reduction. Defaults to True.

    Returns:
        pd.DataFrame: Binned DataFrame with original index name and values.
    """
    # Create a copy of the input DataFrame to avoid modifying the original
    df_in = df_in.copy()

    if isinstance(n_bins, int):
        # broadcast integer n_bins to all bin_by_cols
        n_bins = [n_bins] * len(bin_by_cols)

    if len(bin_by_cols) != len(n_bins):
        raise ValueError(f"{len(bin_by_cols)=} != {len(n_bins)=}")

    cut_cols = [f"{col}_bins" for col in bin_by_cols]
    for col, bins, cut_col in zip(bin_by_cols, n_bins, cut_cols, strict=True):
        df_in[cut_col] = pd.cut(df_in[col].values, bins=bins)

    # Preserve the original index
    orig_index_name = df_in.index.name or "index"
    # Reset index so it participates in groupby. If the index name is already in the
    # columns, we it'll participate already and be set back to the index at the end.
    if orig_index_name not in df_in:
        df_in = df_in.reset_index()

    group = df_in.groupby(by=[*cut_cols, *group_by_cols], observed=True)

    df_bin = group.first().dropna()
    df_bin[bin_counts_col] = group.size()
    df_bin = df_bin.reset_index()

    if verbose:
        print(  # noqa: T201
            f"{1 - len(df_bin) / len(df_in):.1%} sample reduction from binning: from "
            f"{len(df_in):,} to {len(df_bin):,}"
        )

    if density_col:
        # compute kernel density estimate for each bin
        values = df_in[bin_by_cols].dropna().T
        gaussian_kde = scipy.stats.gaussian_kde(values.astype(float))

        xy_binned = df_bin[bin_by_cols].T
        density = gaussian_kde(xy_binned.astype(float))
        df_bin[density_col] = density / density.sum() * len(values)

    # Set the index back to the original index name
    return df_bin.set_index(orig_index_name)


@contextmanager
def patch_dict(
    dct: dict[Any, Any], *args: Any, **kwargs: Any
) -> Generator[dict[Any, Any], None, None]:
    """Context manager to temporarily patch the specified keys in a dictionary and
    restore it to its original state on context exit.

    Useful e.g. for temporary plotly fig.layout mutations:

        with patch_dict(fig.layout, showlegend=False):
            fig.write_image("plot.pdf")

    Args:
        dct (dict): The dictionary to be patched.
        *args: Only first element is read if present. A single dictionary containing the
            key-value pairs to patch.
        **kwargs: The key-value pairs to patch, provided as keyword arguments.

    Yields:
        dict: The patched dictionary incl. temporary updates.
    """
    # if both args and kwargs are passed, kwargs will overwrite args
    updates = {**args[0], **kwargs} if args and isinstance(args[0], dict) else kwargs

    # save original values as shallow copy for speed
    # warning: in-place changes to nested dicts and objects will persist beyond context!
    patched = dct.copy()

    # apply updates
    patched.update(updates)

    yield patched


def luminance(color: str | tuple[float, float, float]) -> float:
    """Compute the luminance of a color as in https://stackoverflow.com/a/596243.

    Args:
        color (tuple[float, float, float]): RGB color tuple with values in [0, 1].

    Returns:
        float: Luminance of the color.
    """
    # raises ValueError if color invalid
    red, green, blue = matplotlib.colors.to_rgb(color)
    return 0.299 * red + 0.587 * green + 0.114 * blue


def pick_bw_for_contrast(
    color: tuple[float, float, float] | str,
    text_color_threshold: float = 0.7,
) -> Literal["black", "white"]:
    """Choose black or white text color for a given background color based on luminance.

    Args:
        color (tuple[float, float, float] | str): RGB color tuple with values in [0, 1].
        text_color_threshold (float, optional): Luminance threshold for choosing
            black or white text color. Defaults to 0.7.

    Returns:
        "black" | "white": depending on the luminance of the background color.
    """
    if isinstance(color, str):
        color = to_rgb(color)

    light_bg = luminance(cast(tuple[float, float, float], color)) > text_color_threshold
    return "black" if light_bg else "white"


def si_fmt(
    val: float,
    *,
    fmt: str = ".1f",
    sep: str = "",
    binary: bool = False,
    decimal_threshold: float = 0.01,
) -> str:
    """Convert large numbers into human readable format using SI prefixes.

    Supports binary (1024) and metric (1000) mode.

    https://nist.gov/pml/weights-and-measures/metric-si-prefixes

    Args:
        val (int | float): Some numerical value to format.
        binary (bool, optional): If True, scaling factor is 2^10 = 1024 else 1000.
            Defaults to False.
        fmt (str): f-string format specifier. Configure precision and left/right
            padding in returned string. Defaults to ".1f". Can be used to ensure leading
            or trailing whitespace for shorter numbers. See
            https://docs.python.org/3/library/string.html#format-specification-mini-language.
        sep (str): Separator between number and postfix. Defaults to "".
        decimal_threshold (float): abs(value) below 1 but above this threshold will be
            left as decimals. Only below this threshold is a greek suffix added (milli,
            micro, etc.). Defaults to 0.01. i.e. 0.01 -> "0.01" while
            0.0099 -> "9.9m". Setting decimal_threshold=0.1 would format 0.01 as "10m"
            and leave 0.1 as is.

    Returns:
        str: Formatted number.
    """
    factor = 1024 if binary else 1000
    _scale = ""

    if abs(val) >= 1:
        # 1, Kilo, Mega, Giga, Tera, Peta, Exa, Zetta, Yotta
        for _scale in ("", "K", "M", "G", "T", "P", "E", "Z", "Y"):
            if abs(val) < factor:
                break
            val /= factor
    elif val != 0 and abs(val) < decimal_threshold:
        # milli, micro, nano, pico, femto, atto, zepto, yocto
        for _scale in ("", "m", "μ", "n", "p", "f", "a", "z", "y"):
            if abs(val) >= 1:
                break
            val *= factor

    return f"{val:{fmt}}{sep}{_scale}"


si_fmt_int = partial(si_fmt, fmt=".0f")


def get_cbar_label_formatter(
    *,
    cbar_label_fmt: str,
    values_fmt: str,
    values_show_mode: Literal["value", "fraction", "percent", "off"],
    sci_notation: bool,
    default_decimal_places: int = 1,
) -> Formatter:
    """Generate colorbar tick label formatter.

    Work differently for different values_show_mode:
        - "value/fraction" mode: Use cbar_label_fmt (or values_fmt) as is.
        - "percent" mode: Get number of decimal places to keep from fmt
            string, for example 1 from ".1%".

    Args:
        cbar_label_fmt (str): f-string option for colorbar tick labels.
        values_fmt (str): f-string option for tile values, would be used if
            cbar_label_fmt is "auto".
        values_show_mode (str): The values display mode:
            - "off": Hide values.
            - "value": Display values as is.
            - "fraction": As a fraction of the total (0.10).
            - "percent": As a percentage of the total (10%).
        sci_notation (bool): Whether to use scientific notation for values and
            colorbar tick labels.
        default_decimal_places (int): Default number of decimal places
            to use if above fmt is invalid.

    Returns:
        PercentFormatter or FormatStrFormatter.
    """
    cbar_label_fmt = values_fmt if cbar_label_fmt == "auto" else cbar_label_fmt

    if values_show_mode == "percent":
        if match := re.search(r"\.(\d+)%", cbar_label_fmt):
            decimal_places = int(match[1])
        else:
            warnings.warn(
                f"Invalid {cbar_label_fmt=}, use {default_decimal_places=}",
                stacklevel=2,
            )
            decimal_places = default_decimal_places
        return PercentFormatter(xmax=1, decimals=decimal_places)

    if sci_notation:
        formatter = ScalarFormatter(useMathText=False)
        formatter.set_powerlimits((0, 0))
        return formatter

    return FormatStrFormatter(f"%{cbar_label_fmt}")


def html_tag(text: str, tag: str = "span", style: str = "", title: str = "") -> str:
    """Wrap text in a span with custom style.

    Style defaults to decreased font size and weight e.g. to display units
    in plotly labels and annotations.

    Args:
        text (str): Text to wrap in span.
        tag (str, optional): HTML tag name. Defaults to "span".
        style (str, optional): CSS style string. Defaults to "". Special keys:
            "small": font-size: 0.8em; font-weight: lighter;
            "bold": font-weight: bold;
            "italic": font-style: italic;
            "underline": text-decoration: underline;
        title (str | None, optional): Title attribute which displays additional
            information in a tooltip. Defaults to "".

    Returns:
        str: HTML string with tag-wrapped text.
    """
    style = {
        "small": "font-size: 0.8em; font-weight: lighter;",
        "bold": "font-weight: bold;",
        "italic": "font-style: italic;",
        "underline": "text-decoration: underline;",
    }.get(style, style)
    attr_str = f" {title=}" if title else ""
    if style:
        attr_str += f" {style=}"
    return f"<{tag}{attr_str}>{text}</{tag}>"


def validate_fig(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator to validate the type of fig keyword argument in a function. fig MUST be
    a keyword argument, not a positional argument.
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        # TODO use typing.ParamSpec to type wrapper once py310 is oldest supported
        fig = kwargs.get("fig")
        if fig is not None and not isinstance(fig, plt.Axes | plt.Figure | go.Figure):
            raise TypeError(
                f"Unexpected type for fig: {type(fig).__name__}, must be one of None, "
                f"{VALID_FIG_NAMES}"
            )
        return func(*args, **kwargs)

    return wrapper


def annotate(text: str | Sequence[str], fig: AxOrFig, **kwargs: Any) -> AxOrFig:
    """Annotate a matplotlib or plotly figure. Supports faceted plots plotly figure with
    trace with empty strings skipped.

    Args:
        text (str): The text to use for annotation. If fig is plotly faceted, text can
            be a list of strings to annotate each subplot.
        fig (plt.Axes | plt.Figure | go.Figure | None, optional): The matplotlib Axes,
            Figure or plotly Figure to annotate.
        **kwargs: Additional arguments to pass to matplotlib's AnchoredText or plotly's
            fig.add_annotation().

    Returns:
        plt.Axes | plt.Figure | go.Figure: The annotated figure.

    Raises:
        TypeError: If fig is not a Matplotlib or Plotly figure.
    """
    color = kwargs.pop("color", get_font_color(fig))

    if isinstance(fig, plt.Figure | plt.Axes):
        ax = fig if isinstance(fig, plt.Axes) else plt.gca()
        defaults = dict(frameon=False, loc="upper left", prop=dict(color=color))
        text_box = AnchoredText(text, **(defaults | kwargs))
        ax.add_artist(text_box)
    elif isinstance(fig, go.Figure):
        defaults = dict(
            x=0.02,
            y=0.96,
            showarrow=False,
            font=dict(size=16, color=color),
            align="left",
        )

        # Annotate all subplots or main plot if not faceted
        if any(
            getattr(trace, "xaxis", None) not in (None, "x") for trace in fig.data
        ):  # Faceted plot
            for idx, trace in enumerate(fig.data):
                # if text is str, use it for all subplots though we might want to
                # warn since this will likely rarely be intended
                sub_text = text if isinstance(text, str) else text[idx]
                # skip traces for which no annotations were provided
                if not sub_text:
                    continue

                subplot_idx = trace.xaxis[1:] or ""  # e.g., 'x2' -> '2', 'x' -> ''
                xref = f"x{subplot_idx} domain" if subplot_idx else "x domain"
                yref = f"y{subplot_idx} domain" if subplot_idx else "y domain"
                fig.add_annotation(
                    text=sub_text,
                    **(dict(xref=xref, yref=yref) | defaults | kwargs),
                )
        else:  # Non-faceted plot
            if not isinstance(text, str):
                text_type = type(text).__name__
                raise ValueError(
                    f"Unexpected {text_type=} for non-faceted plot, must be str"
                )
            fig.add_annotation(
                text=text, **(dict(xref="paper", yref="paper") | defaults | kwargs)
            )
    else:
        raise TypeError(f"Unexpected {fig=}")

    return fig


@validate_fig
def get_fig_xy_range(
    fig: go.Figure | plt.Figure | plt.Axes, trace_idx: int = 0
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Get the x and y range of a plotly or matplotlib figure.

    Args:
        fig (go.Figure | plt.Figure | plt.Axes): plotly/matplotlib figure or axes.
        trace_idx (int, optional): Index of the trace to use for measuring x/y limits.
            Defaults to 0. Unused if kaleido package is installed and the figure's
            actual x/y-range can be obtained from fig.full_figure_for_development().

    Returns:
        tuple[float, float, float, float]: The x and y range of the figure in the format
            (x_min, x_max, y_min, y_max).
    """
    if fig is None:
        fig = plt.gcf()
    if isinstance(fig, plt.Figure | plt.Axes):  # handle matplotlib
        ax = fig if isinstance(fig, plt.Axes) else fig.gca()

        return ax.get_xlim(), ax.get_ylim()

    # If kaleido is missing, try block raises ValueError: Full figure generation
    # requires the kaleido package. Install with: pip install kaleido
    # If so, we resort to manually computing the xy data ranges which are usually are
    # close to but not the same as the axes limits.
    try:
        # https://stackoverflow.com/a/62042077
        dev_fig = fig.full_figure_for_development(warn=False)
        xaxis_type = dev_fig.layout.xaxis.type
        yaxis_type = dev_fig.layout.yaxis.type

        x_range = dev_fig.layout.xaxis.range
        y_range = dev_fig.layout.yaxis.range

        # Convert log range to linear if necessary
        if xaxis_type == "log":
            x_range = [10**val for val in x_range]
        if yaxis_type == "log":
            y_range = [10**val for val in y_range]

    except ValueError:
        trace = fig.data[trace_idx]
        df_xy = pd.DataFrame({"x": trace.x, "y": trace.y}).dropna()

        # Determine ranges based on the type of axes
        if fig.layout.xaxis.type == "log":
            x_range = [10**val for val in (min(df_xy.x), max(df_xy.x))]
        else:
            x_range = [min(df_xy.x), max(df_xy.x)]

        if fig.layout.yaxis.type == "log":
            y_range = [10**val for val in (min(df_xy.y), max(df_xy.y))]
        else:
            y_range = [min(df_xy.y), max(df_xy.y)]

    return x_range, y_range


def get_font_color(fig: AxOrFig) -> str:
    """Get the font color used in a Matplotlib figure/axes or a Plotly figure.

    Args:
        fig (plt.Figure | plt.Axes | go.Figure): A Matplotlib or Plotly figure object.

    Returns:
        str: The font color as a string (e.g., 'black', '#000000').

    Raises:
        TypeError: If fig is not a Matplotlib or Plotly figure.
    """
    if isinstance(fig, go.Figure):
        return _get_plotly_font_color(fig)
    if isinstance(fig, plt.Figure | plt.Axes):
        return _get_matplotlib_font_color(fig)
    raise TypeError(f"Input must be {VALID_FIG_NAMES}, got {type(fig)=}")


def _get_plotly_font_color(fig: go.Figure) -> str:
    """Get the font color used in a Plotly figure.

    Args:
        fig (go.Figure): A Plotly figure object.

    Returns:
        str: The font color as a string (e.g., 'black', '#000000').
    """
    if fig.layout.font and fig.layout.font.color:
        return fig.layout.font.color

    if (
        fig.layout.template
        and fig.layout.template.layout
        and fig.layout.template.layout.font
        and fig.layout.template.layout.font.color
    ):
        return fig.layout.template.layout.font.color

    template = pio.templates.default
    if isinstance(template, str):
        template = pio.templates[template]
    if template.layout and template.layout.font and template.layout.font.color:
        return template.layout.font.color

    return "black"


def _get_matplotlib_font_color(fig: plt.Figure | plt.Axes) -> str:
    """Get the font color used in a Matplotlib figure/axes.

    Args:
        fig (plt.Figure | plt.Axes): A Matplotlib figure or axes object.

    Returns:
        str: The font color as a string (e.g., 'black', '#000000').
    """
    ax = fig if isinstance(fig, plt.Axes) else fig.gca()

    # Check axes text color
    for text_element in (ax.xaxis.label, ax.yaxis.label, ax.title):
        text_color = text_element.get_color()
        if text_color != "auto":
            return text_color

    # Check tick label color
    x_labels = ax.xaxis.get_ticklabels()
    tick_color = x_labels[0].get_color() if x_labels else None
    if tick_color is not None and tick_color != "auto":
        return tick_color

    # Check rcParams
    return plt.rcParams.get("text.color", "black")


def normalize_to_dict(
    inputs: T | Sequence[T] | dict[str, T],
    cls: type[T] = Structure,
    key_gen: Callable[[T], str] = lambda obj: getattr(
        obj, "formula", type(obj).__name__
    ),
) -> dict[str, T]:
    """Normalize any kind of object or dict/list/tuple of them into to a dictionary.

    Args:
        inputs: A single object, a sequence of objects, or a dictionary of objects.
        cls (type[T], optional): The class of the objects to normalize. Defaults to
            pymatgen.core.Structure.
        key_gen (Callable[[T], str], optional): A function that generates a key for
            each object. Defaults to using the object's formula, assuming the objects
            are pymatgen.core.(Structure|Molecule).

    Returns:
        A dictionary of objects with keys as object formulas or given keys.

    Raises:
        TypeError: If the input format is invalid.
    """
    if isinstance(inputs, cls):
        return {"": inputs}

    if (
        isinstance(inputs, list | tuple)
        and all(isinstance(obj, cls) for obj in inputs)
        and len(inputs) > 0
    ):
        out_dict: dict[str, T] = {}
        for obj in inputs:
            key = key_gen(obj)
            idx = 1
            while key in out_dict:
                key += f" {idx}"
                idx += 1
            out_dict[key] = obj
        return out_dict
    if isinstance(inputs, dict):
        return inputs
    if isinstance(inputs, pd.Series):
        return inputs.to_dict()

    cls_name = cls.__name__
    raise TypeError(
        f"Invalid {inputs=}, expected {cls_name} or dict/list/tuple of {cls_name}"
    )
