import matplotlib.pyplot as plt
import numpy as np


def plot_data(
    dfs,
    x_col,
    y_col,
    yerr=None,
    xlabel=None,
    ylabel=None,
    title=None,
    labels=None,
    colors=None,
    savepath=None,
    show=True,

    # ---- style controls (preserved) ----
    title_fontsize=16,
    axis_label_fontsize=14,
    tick_fontsize=12,
    legend_fontsize=11,
    figure_dpi=100,
    figure_size=(10, 7),
    grid_alpha=0.2,
    legend_loc='best',
    show_legend = True,
    negative_values = False
):
    """
    Pure plotting function with full style control.
    No model computation.
    """

    # ---------- normalize input ----------
    if not isinstance(dfs, list):
        dfs = [dfs]
    n = len(dfs)

    if labels is None:
        labels = [f'Data {i+1}' for i in range(n)]
    if len(labels) != n:
        raise ValueError("labels length mismatch")

    if colors is None:
        colors = plt.cm.tab10(np.linspace(0, 1, n))
    if len(colors) != n:
        raise ValueError("colors length mismatch")

    # ---------- error parser ----------
    def parse_err_for_df(df, err_spec):
        if err_spec is None:
            return None
        if isinstance(err_spec, str):
            return df[err_spec].to_numpy(dtype=float)
        if np.isscalar(err_spec):
            return np.full(len(df), float(err_spec))
        arr = np.asarray(err_spec, dtype=float)
        if len(arr) != len(df):
            raise ValueError("Error array length mismatch")
        return arr

    # ---------- figure ----------
    fig, ax = plt.subplots(
        figsize=figure_size,
        dpi=figure_dpi
    )
    fig.patch.set_facecolor('white')

    # ---------- styling ----------
    ax.set_xlabel(xlabel or x_col, fontsize=axis_label_fontsize)
    ax.set_ylabel(ylabel or y_col, fontsize=axis_label_fontsize)

    if title is not None:
        ax.set_title(title, fontsize=title_fontsize, pad=12)

    ax.tick_params(
        axis='both',
        labelsize=tick_fontsize,
        direction='in',
        length=5,
        width=1.1
    )

    for spine in ax.spines.values():
        spine.set_linewidth(1.1)

    ax.grid(alpha=grid_alpha, linestyle=':', linewidth=0.8)

    # ---------- plot data ----------
    for df, lab, col in zip(dfs, labels, colors):
        x = df[x_col].to_numpy(dtype=float)
        y = df[y_col].to_numpy(dtype=float)
        cur_yerr = parse_err_for_df(df, yerr)

        ax.errorbar(
            x, y,
            yerr=cur_yerr,
            fmt='o',
            capsize=3,
            color=col,
            alpha=0.85,
            markersize=5,
            elinewidth=1.1,
            capthick=1.1,
            label=lab
        )

    if show_legend:
        # ---------- legend ----------
        ax.legend(
            loc=legend_loc,
            fontsize=legend_fontsize,
            frameon=True,
            fancybox=False,
            edgecolor='black'
        )

    if not negative_values:
        ax.set_ylim(0, ax.get_ylim()[1])

    fig.tight_layout()

    # ---------- output ----------
    if savepath:
        fig.savefig(savepath, dpi=figure_dpi, bbox_inches='tight', facecolor='white')

    if show:
        plt.show()

    return fig
