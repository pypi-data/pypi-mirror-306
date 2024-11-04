<h1 align="center">
<img src="https://github.com/janosh/pymatviz/raw/main/site/static/favicon.svg" alt="Logo" height="60px">
<br class="hide-in-docs">
pymatviz
</h1>

<h4 align="center" class="toc-exclude">

A toolkit for visualizations in materials informatics.

[![Tests](https://github.com/janosh/pymatviz/actions/workflows/test.yml/badge.svg)](https://github.com/janosh/pymatviz/actions/workflows/test.yml)
[![This project supports Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white)](https://python.org/downloads)
[![PyPI](https://img.shields.io/pypi/v/pymatviz?logo=pypi&logoColor=white)](https://pypi.org/project/pymatviz)
[![PyPI Downloads](https://img.shields.io/pypi/dm/pymatviz?logo=icloud&logoColor=white)](https://pypistats.org/packages/pymatviz)
[![Zenodo](https://img.shields.io/badge/DOI-10.5281/zenodo.10456384-blue?logo=Zenodo&logoColor=white)](https://zenodo.org/records/10456384)

</h4>

<slot name="how-to-cite">

> If you use `pymatviz` in your research, [see how to cite](#how-to-cite-pymatviz).

</slot>

## Installation

```sh
pip install pymatviz
```

## API Docs

See the [/api] page.

[/api]: https://janosh.github.io/pymatviz/api

## Usage

See the Jupyter notebooks under [`examples/`](examples) for how to use `pymatviz`. PRs with additional examples are welcome! 🙏

|                                                                                                                        |                                                                                                                                       |                                      |
| ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| [mlff_phonons.ipynb](https://github.com/janosh/pymatviz/blob/main/examples/mlff_phonons.ipynb)                         | [![Open in Google Colab]](https://colab.research.google.com/github/janosh/pymatviz/blob/main/examples/mlff_phonons.ipynb)             | [![Launch Codespace]][codespace url] |
| [matbench_dielectric_eda.ipynb](https://github.com/janosh/pymatviz/blob/main/examples/matbench_dielectric_eda.ipynb)   | [![Open in Google Colab]](https://colab.research.google.com/github/janosh/pymatviz/blob/main/examples/matbench_dielectric_eda.ipynb)  | [![Launch Codespace]][codespace url] |
| [mp_bimodal_e_form.ipynb](https://github.com/janosh/pymatviz/blob/main/examples/mp_bimodal_e_form.ipynb)               | [![Open in Google Colab]](https://colab.research.google.com/github/janosh/pymatviz/blob/main/examples/mp_bimodal_e_form.ipynb)        | [![Launch Codespace]][codespace url] |
| [matbench_perovskites_eda.ipynb](https://github.com/janosh/pymatviz/blob/main/examples/matbench_perovskites_eda.ipynb) | [![Open in Google Colab]](https://colab.research.google.com/github/janosh/pymatviz/blob/main/examples/matbench_perovskites_eda.ipynb) | [![Launch Codespace]][codespace url] |
| [mprester_ptable.ipynb](https://github.com/janosh/pymatviz/blob/main/examples/mprester_ptable.ipynb)                   | [![Open in Google Colab]](https://colab.research.google.com/github/janosh/pymatviz/blob/main/examples/mprester_ptable.ipynb)          | [![Launch Codespace]][codespace url] |

[Open in Google Colab]: https://colab.research.google.com/assets/colab-badge.svg
[Launch Codespace]: https://img.shields.io/badge/Launch-Codespace-darkblue?logo=github
[codespace url]: https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=340898532

## Periodic Table

See [`pymatviz/ptable/ptable_matplotlib.py`](pymatviz/ptable/ptable_matplotlib.py) and [`pymatviz/ptable/ptable_plotly.py`](pymatviz/ptable/ptable_plotly.py). `matplotlib` supports heatmaps, heatmap ratios, heatmap splits (multiple values per element), histograms, scatter plots and line plots. `plotly` currently only supports heatmaps (PRs to port over other `matplotlib` `ptable` variants to `plotly` are very welcome!). The `plotly` heatmap supports displaying additional data on hover or full interactivity through [Dash](https://plotly.com/dash).

|                    [`ptable_heatmap(compositions, log=True)`](pymatviz/ptable/ptable_matplotlib.py)                    |                   [`ptable_heatmap_ratio(comps_a, comps_b)`](pymatviz/ptable/ptable_matplotlib.py)                    |
| :--------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------: |
|                                                   ![ptable-heatmap]                                                    |                                                ![ptable-heatmap-ratio]                                                |
|                       [`ptable_heatmap_plotly(atomic_masses)`](pymatviz/ptable/ptable_plotly.py)                       |                [`ptable_heatmap_plotly(compositions, log=True)`](pymatviz/ptable/ptable_matplotlib.py)                |
|                                        ![ptable-heatmap-plotly-more-hover-data]                                        |                                             ![ptable-heatmap-plotly-log]                                              |
|                   [`ptable_hists(data, colormap="coolwarm")`](pymatviz/ptable/ptable_matplotlib.py)                    |                             [`ptable_lines(data)`](pymatviz/ptable/ptable_matplotlib.py)                              |
|                                                    ![ptable-hists]                                                     |                                                    ![ptable-lines]                                                    |
|                  [`ptable_scatters(data, colormap="coolwarm")`](pymatviz/ptable/ptable_matplotlib.py)                  |                 [`ptable_scatters(data, colormap="coolwarm")`](pymatviz/ptable/ptable_matplotlib.py)                  |
|                                               ![ptable-scatters-parity]                                                |                                              ![ptable-scatters-parabola]                                              |
| [`ptable_heatmap_splits(2_vals_per_elem, colormap="coolwarm", start_angle=135)`](pymatviz/ptable/ptable_matplotlib.py) | [`ptable_heatmap_splits(3_vals_per_elem, colormap="coolwarm", start_angle=90)`](pymatviz/ptable/ptable_matplotlib.py) |
|                                               ![ptable-heatmap-splits-2]                                               |                                              ![ptable-heatmap-splits-3]                                               |

[ptable-hists]: https://github.com/janosh/pymatviz/raw/main/assets/ptable-hists.svg
[ptable-lines]: https://github.com/janosh/pymatviz/raw/main/assets/homo-nuclear-mace-medium.svg
[ptable-scatters-parity]: https://github.com/janosh/pymatviz/raw/main/assets/ptable-scatters-parity.svg
[ptable-scatters-parabola]: https://github.com/janosh/pymatviz/raw/main/assets/ptable-scatters-parabola.svg
[ptable-heatmap-splits-2]: https://github.com/janosh/pymatviz/raw/main/assets/ptable-heatmap-splits-2.svg
[ptable-heatmap-splits-3]: https://github.com/janosh/pymatviz/raw/main/assets/ptable-heatmap-splits-3.svg

## Phonons

See [`examples/mlff_phonons.ipynb`](https://github.com/janosh/pymatviz/blob/main/examples/mlff_phonons.ipynb) for usage example.

|           [`phonon_bands(bands_dict)`](pymatviz/phonons.py)           |             [`phonon_dos(doses_dict)`](pymatviz/phonons.py)             |
| :-------------------------------------------------------------------: | :---------------------------------------------------------------------: |
|                            ![phonon-bands]                            |                              ![phonon-dos]                              |
| [`phonon_bands_and_dos(bands_dict, doses_dict)`](pymatviz/phonons.py) | [`phonon_bands_and_dos(single_bands, single_dos)`](pymatviz/phonons.py) |
|                    ![phonon-bands-and-dos-mp-2758]                    |                    ![phonon-bands-and-dos-mp-23907]                     |

[phonon-bands]: https://github.com/janosh/pymatviz/raw/main/assets/phonon-bands-mp-2758.svg
[phonon-dos]: https://github.com/janosh/pymatviz/raw/main/assets/phonon-dos-mp-2758.svg
[phonon-bands-and-dos-mp-2758]: https://github.com/janosh/pymatviz/raw/main/assets/phonon-bands-and-dos-mp-2758.svg
[phonon-bands-and-dos-mp-23907]: https://github.com/janosh/pymatviz/raw/main/assets/phonon-bands-and-dos-mp-23907.svg

### Dash app using `ptable_heatmap_plotly()`

See [`examples/mprester_ptable.ipynb`](https://github.com/janosh/pymatviz/blob/main/examples/mprester_ptable.ipynb).

<https://user-images.githubusercontent.com/30958850/181644052-b330f0a2-70fc-451c-8230-20d45d3af72f.mp4>

## Structure

See [`pymatviz/structure_viz/(mpl|plotly).py`](pymatviz/structure_viz/plotly.py). Currently structure plotting is only supported with `matplotlib` in 2d. 3d interactive plots (probably with `plotly`) are on the road map.

|       [`structure_2d(mp_19017)`](pymatviz/structure_viz/mpl.py)        |       [`structure_2d(mp_12712)`](pymatviz/structure_viz/mpl.py)        |
| :--------------------------------------------------------------------: | :--------------------------------------------------------------------: |
|        ![struct-2d-mp-19017-Li4Mn0.8Fe1.6P4C1.6O16-disordered]         |              ![struct-2d-mp-12712-Hf9Zr9Pd24-disordered]               |
| [`structure_2d_plotly(six_structs)`](pymatviz/structure_viz/plotly.py) | [`structure_3d_plotly(six_structs)`](pymatviz/structure_viz/plotly.py) |
|                ![matbench-phonons-structures-2d-plotly]                |                ![matbench-phonons-structures-3d-plotly]                |

[matbench-phonons-structures-2d-plotly]: https://github.com/janosh/pymatviz/raw/main/assets/matbench-phonons-structures-2d-plotly.svg
[matbench-phonons-structures-3d-plotly]: https://github.com/janosh/pymatviz/raw/main/assets/matbench-phonons-structures-3d-plotly.svg

## X-Ray Diffraction

See [`pymatviz/xrd.py`](pymatviz/xrd.py).

|             [`xrd_pattern(pattern)`](pymatviz/xrd.py)             |             [`xrd_pattern({key1: patt1, key2: patt2})`](pymatviz/xrd.py)              |
| :---------------------------------------------------------------: | :-----------------------------------------------------------------------------------: |
|                          ![xrd-pattern]                           |                                ![xrd-pattern-multiple]                                |
| [`xrd_pattern(struct_dict, stack="horizontal")`](pymatviz/xrd.py) | [`xrd_pattern(struct_dict, stack="vertical", title="Custom Title")`](pymatviz/xrd.py) |
|                  ![xrd-pattern-horizontal-stack]                  |                             ![xrd-pattern-vertical-stack]                             |

[xrd-pattern]: https://github.com/janosh/pymatviz/raw/main/assets/xrd-pattern.svg
[xrd-pattern-multiple]: https://github.com/janosh/pymatviz/raw/main/assets/xrd-pattern-multiple.svg
[xrd-pattern-horizontal-stack]: https://github.com/janosh/pymatviz/raw/main/assets/xrd-pattern-horizontal-stack.svg
[xrd-pattern-vertical-stack]: https://github.com/janosh/pymatviz/raw/main/assets/xrd-pattern-vertical-stack.svg

## Radial Distribution Functions

See [`pymatviz/rdf/plotly.py`](pymatviz/rdf/plotly.py).

| [`rdf_plot(rdf)`](pymatviz/rdf/plotly.py) | [`rdf_plot(rdf, rdf2)`](pymatviz/rdf/plotly.py) |
| :---------------------------------------: | :---------------------------------------------: |
|      ![element-pair-rdfs-Na8Nb8O24]       |    ![element-pair-rdfs-crystal-vs-amorphous]    |

[element-pair-rdfs-Na8Nb8O24]: https://github.com/janosh/pymatviz/raw/main/assets/element-pair-rdfs-Na8Nb8O24.svg
[element-pair-rdfs-crystal-vs-amorphous]: https://github.com/janosh/pymatviz/raw/main/assets/element-pair-rdfs-crystal-vs-amorphous.svg

## Coordination

See [`pymatviz/coordination/plotly.py`](pymatviz/coordination/plotly.py).

|             [`coordination_hist(struct_dict)`](pymatviz/coordination/plotly.py)              |     [`coordination_hist(struct_dict, by_element=True)`](pymatviz/coordination/plotly.py)     |
| :------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------: |
|                                 ![coordination-hist-single]                                  |                        ![coordination-hist-by-structure-and-element]                         |
| [`coordination_vs_cutoff_line(struct_dict, strategy=None)`](pymatviz/coordination/plotly.py) | [`coordination_vs_cutoff_line(struct_dict, strategy=None)`](pymatviz/coordination/plotly.py) |
|                               ![coordination-vs-cutoff-single]                               |                              ![coordination-vs-cutoff-multiple]                              |

[coordination-hist-single]: https://github.com/janosh/pymatviz/raw/main/assets/coordination-hist-single.svg
[coordination-hist-by-structure-and-element]: https://github.com/janosh/pymatviz/raw/main/assets/coordination-hist-by-structure-and-element.svg
[coordination-vs-cutoff-single]: https://github.com/janosh/pymatviz/raw/main/assets/coordination-vs-cutoff-single.svg
[coordination-vs-cutoff-multiple]: https://github.com/janosh/pymatviz/raw/main/assets/coordination-vs-cutoff-multiple.svg

## Sunburst

See [`pymatviz/sunburst.py`](pymatviz/sunburst.py).

| [`spacegroup_sunburst([65, 134, 225, ...])`](pymatviz/sunburst.py) | [`spacegroup_sunburst(["C2/m", "P-43m", "Fm-3m", ...])`](pymatviz/sunburst.py) |
| :----------------------------------------------------------------: | :----------------------------------------------------------------------------: |
|                        ![spg-num-sunburst]                         |                             ![spg-symbol-sunburst]                             |

## Rainclouds

See [`pymatviz/rainclouds.py`](pymatviz/rainclouds.py).

| [`rainclouds(two_key_dict)`](pymatviz/rainclouds.py) | [`rainclouds(three_key_dict)`](pymatviz/rainclouds.py) |
| :--------------------------------------------------: | :----------------------------------------------------: |
|                ![rainclouds-bimodal]                 |                 ![rainclouds-trimodal]                 |

[rainclouds-bimodal]: https://github.com/janosh/pymatviz/raw/main/assets/rainclouds-bimodal.svg
[rainclouds-trimodal]: https://github.com/janosh/pymatviz/raw/main/assets/rainclouds-trimodal.svg

## Sankey

See [`pymatviz/sankey.py`](pymatviz/sankey.py).

| [`sankey_from_2_df_cols(df_perovskites)`](pymatviz/sankey.py) | [`sankey_from_2_df_cols(df_space_groups)`](pymatviz/sankey.py) |
| :-----------------------------------------------------------: | :------------------------------------------------------------: |
|             ![sankey-spglib-vs-aflow-spacegroups]             |              ![sankey-crystal-sys-to-spg-symbol]               |

[sankey-spglib-vs-aflow-spacegroups]: https://github.com/janosh/pymatviz/raw/main/assets/sankey-spglib-vs-aflow-spacegroups.svg
[sankey-crystal-sys-to-spg-symbol]: https://github.com/janosh/pymatviz/raw/main/assets/sankey-crystal-sys-to-spg-symbol.svg

## Histograms

See [`pymatviz/histogram.py`](pymatviz/histogram.py).

| [`spacegroup_bar([65, 134, 225, ...], backend="matplotlib")`](pymatviz/histogram.py) | [`spacegroup_bar(["C2/m", "P-43m", "Fm-3m", ...], backend="matplotlib")`](pymatviz/histogram.py) |
| :----------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------: |
|                              ![spg-num-hist-matplotlib]                              |                                  ![spg-symbol-hist-matplotlib]                                   |
|   [`spacegroup_bar([65, 134, 225, ...], backend="plotly")`](pymatviz/histogram.py)   |   [`spacegroup_bar(["C2/m", "P-43m", "Fm-3m", ...], backend="plotly")`](pymatviz/histogram.py)   |
|                                ![spg-num-hist-plotly]                                |                                    ![spg-symbol-hist-plotly]                                     |
| [`elements_hist(compositions, log=True, bar_values='count')`](pymatviz/histogram.py) |             [`histogram({'key1': values1, 'key2': values2})`](pymatviz/histogram.py)             |
|                                   ![elements-hist]                                   |                                        ![histogram-ecdf]                                         |

[spg-symbol-hist-plotly]: https://github.com/janosh/pymatviz/raw/main/assets/spg-symbol-hist-plotly.svg
[spg-num-hist-plotly]: https://github.com/janosh/pymatviz/raw/main/assets/spg-num-hist-plotly.svg
[spg-num-hist-matplotlib]: https://github.com/janosh/pymatviz/raw/main/assets/spg-num-hist-matplotlib.svg
[spg-symbol-hist-matplotlib]: https://github.com/janosh/pymatviz/raw/main/assets/spg-symbol-hist-matplotlib.svg
[histogram-ecdf]: https://github.com/janosh/pymatviz/raw/main/assets/histogram-ecdf.svg

## Scatter Plots

See [`pymatviz/scatter.py`](pymatviz/scatter.py).

| [`density_scatter_plotly(df, x=x_col, y=y_col, ...)`](pymatviz/scatter.py) | [`density_scatter_plotly(df, x=x_col, y=y_col, ...)`](pymatviz/scatter.py) |
| :------------------------------------------------------------------------: | :------------------------------------------------------------------------: |
|                         ![density-scatter-plotly]                          |                      ![density-scatter-plotly-blobs]                       |
|           [`density_scatter(xs, ys, ...)`](pymatviz/scatter.py)            |      [`density_scatter_with_hist(xs, ys, ...)`](pymatviz/scatter.py)       |
|                             ![density-scatter]                             |                        ![density-scatter-with-hist]                        |
|            [`density_hexbin(xs, ys, ...)`](pymatviz/scatter.py)            |       [`density_hexbin_with_hist(xs, ys, ...)`](pymatviz/scatter.py)       |
|                             ![density-hexbin]                              |                        ![density-hexbin-with-hist]                         |

[density-scatter-plotly]: https://github.com/janosh/pymatviz/raw/main/assets/density-scatter-plotly.svg
[density-scatter-plotly-blobs]: https://github.com/janosh/pymatviz/raw/main/assets/density-scatter-plotly-blobs.svg
[density-hexbin-with-hist]: https://github.com/janosh/pymatviz/raw/main/assets/density-hexbin-with-hist.svg
[density-hexbin]: https://github.com/janosh/pymatviz/raw/main/assets/density-hexbin.svg
[density-scatter-with-hist]: https://github.com/janosh/pymatviz/raw/main/assets/density-scatter-with-hist.svg
[density-scatter]: https://github.com/janosh/pymatviz/raw/main/assets/density-scatter.svg

## Uncertainty

See [`pymatviz/uncertainty.py`](pymatviz/uncertainty.py).

|       [`qq_gaussian(y_true, y_pred, y_std)`](pymatviz/uncertainty.py)       |       [`qq_gaussian(y_true, y_pred, y_std: dict)`](pymatviz/uncertainty.py)       |
| :-------------------------------------------------------------------------: | :-------------------------------------------------------------------------------: |
|                             ![normal-prob-plot]                             |                           ![normal-prob-plot-multiple]                            |
| [`error_decay_with_uncert(y_true, y_pred, y_std)`](pymatviz/uncertainty.py) | [`error_decay_with_uncert(y_true, y_pred, y_std: dict)`](pymatviz/uncertainty.py) |
|                         ![error-decay-with-uncert]                          |                        ![error-decay-with-uncert-multiple]                        |

## Cumulative Metrics

See [`pymatviz/cumulative.py`](pymatviz/cumulative.py).

| [`cumulative_error(preds, targets)`](pymatviz/cumulative.py) | [`cumulative_residual(preds, targets)`](pymatviz/cumulative.py) |
| :----------------------------------------------------------: | :-------------------------------------------------------------: |
|                     ![cumulative-error]                      |                     ![cumulative-residual]                      |

## Classification

See [`pymatviz/relevance.py`](pymatviz/relevance.py).

| [`roc_curve(targets, proba_pos)`](pymatviz/relevance.py) | [`precision_recall_curve(targets, proba_pos)`](pymatviz/relevance.py) |
| :------------------------------------------------------: | :-------------------------------------------------------------------: |
|                       ![roc-curve]                       |                       ![precision-recall-curve]                       |

[cumulative-error]: https://github.com/janosh/pymatviz/raw/main/assets/cumulative-error.svg
[cumulative-residual]: https://github.com/janosh/pymatviz/raw/main/assets/cumulative-residual.svg
[error-decay-with-uncert-multiple]: https://github.com/janosh/pymatviz/raw/main/assets/error-decay-with-uncert-multiple.svg
[error-decay-with-uncert]: https://github.com/janosh/pymatviz/raw/main/assets/error-decay-with-uncert.svg
[elements-hist]: https://github.com/janosh/pymatviz/raw/main/assets/elements-hist.svg
[matbench-phonons-structures-2d]: https://github.com/janosh/pymatviz/raw/main/assets/matbench-phonons-structures-2d.svg
[normal-prob-plot-multiple]: https://github.com/janosh/pymatviz/raw/main/assets/normal-prob-plot-multiple.svg
[normal-prob-plot]: https://github.com/janosh/pymatviz/raw/main/assets/normal-prob-plot.svg
[precision-recall-curve]: https://github.com/janosh/pymatviz/raw/main/assets/precision-recall-curve.svg
[ptable-heatmap-plotly-log]: https://github.com/janosh/pymatviz/raw/main/assets/ptable-heatmap-plotly-log.svg
[ptable-heatmap-plotly-more-hover-data]: https://github.com/janosh/pymatviz/raw/main/assets/ptable-heatmap-plotly-more-hover-data.svg
[ptable-heatmap-ratio]: https://github.com/janosh/pymatviz/raw/main/assets/ptable-heatmap-ratio.svg
[ptable-heatmap]: https://github.com/janosh/pymatviz/raw/main/assets/ptable-heatmap.svg
[residual-vs-actual]: https://github.com/janosh/pymatviz/raw/main/assets/residual-vs-actual.svg
[roc-curve]: https://github.com/janosh/pymatviz/raw/main/assets/roc-curve.svg
[scatter-with-err-bar]: https://github.com/janosh/pymatviz/raw/main/assets/scatter-with-err-bar.svg
[spg-num-sunburst]: https://github.com/janosh/pymatviz/raw/main/assets/spg-num-sunburst.svg
[spg-symbol-sunburst]: https://github.com/janosh/pymatviz/raw/main/assets/spg-symbol-sunburst.svg
[struct-2d-mp-12712-Hf9Zr9Pd24-disordered]: https://github.com/janosh/pymatviz/raw/main/assets/struct-2d-mp-12712-Hf9Zr9Pd24-disordered.svg
[struct-2d-mp-19017-Li4Mn0.8Fe1.6P4C1.6O16-disordered]: https://github.com/janosh/pymatviz/raw/main/assets/struct-2d-mp-19017-Li4Mn0.8Fe1.6P4C1.6O16-disordered.svg

## How to cite `pymatviz`

See [`citation.cff`](citation.cff) or cite the [Zenodo record](https://zenodo.org/badge/latestdoi/340898532) using the following BibTeX entry:

```bib
@software{riebesell_pymatviz_2022,
  title = {Pymatviz: visualization toolkit for materials informatics},
  author = {Riebesell, Janosh and Yang, Haoyu and Goodall, Rhys and Baird, Sterling G.},
  date = {2022-10-01},
  year = {2022},
  doi = {10.5281/zenodo.7486816},
  url = {https://github.com/janosh/pymatviz},
  note = {10.5281/zenodo.7486816 - https://github.com/janosh/pymatviz},
  urldate = {2023-01-01}, % optional, replace with your date of access
  version = {0.8.2}, % replace with the version you use
}
```
