import typing as tp

import matplotlib.pylab as plt
import seaborn as sns

from vizdata.generator import pair_generator
from vizdata.utils import get_grid_size


def plot_pair_numeric_eda(
        *,
        df,
        columns: tp.List[str],
        one_graph_size: int,
        max_n_cols: int,
        color: str,
        cmap: str,
        style: str) -> tp.Optional[plt.Figure]:
    numeric_pairs = list(pair_generator(columns))
    if not numeric_pairs:
        return
    n_cols, n_rows = get_grid_size(len(numeric_pairs), max_n_cols)
    fig = plt.figure(figsize=(one_graph_size * n_cols, one_graph_size * n_rows))
    fig.subplots_adjust(top=1.05)

    for index, (col1, col2) in enumerate(numeric_pairs, start=1):
        ax = fig.add_subplot(n_rows, n_cols, index)
        x, y = df[col1], df[col2]
        if style == "kde":
            sns.kdeplot(
                x=x,
                y=y,
                ax=ax,
                cmap=cmap,
                warn_singular=False,
                color=color,
                fill=True,
            )
        elif style == "scatter":
            sns.scatterplot(x=x, y=y, s=3)
        else:
            sns.histplot(x=x, y=y, cmap=cmap)

    plt.tight_layout()
    return fig
