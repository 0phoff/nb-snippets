#
#   Matplotlib plotting functions notebooks
#   Tanguy Ophoff
#

def plot_tide(tide_series, *, errors_lim=None, fpfn_lim=None, no_zero=False, color=None, saturation=0.75, ax=None, **kwargs):
    """
    This function can plot the results of a `brambox.eval.TIDE` series with matplotlib.

    Args:
        tide_series (pd.Series): Series with tide values as returned by bb.eval.TIDE
        errors_lim (list): Axis limits for the errors barplot; Default None
        fpfn_lim (list): Axis limits for the fpfn barplot; Default None
        no_zero (bool): Remove errors if they are zero; Default False
        color (matplotlib color): hex, rgb-tuple or html color name for the barplots; Default None
        saturation (float): saturation value for the barplot colors; Default 0.75
        ax (matplotlib ax): Ax to draw the plots on; Default plt.gca()
        kwargs: Extra keyword arguments passed to the barplot functions

    Example:
        >>> tide = bb.eval.TIDE(det, anno).mdAP
        >>> plot_tide(tide)
    """
    import matplotlib.pyplot as plt
    try:
        import seaborn as sns
    except ImportError:
        sns = None

    # Set color
    if color is not None:
        if sns is None:
            kwargs['color'] = color
        else:
            kwargs['color'] = sns.desaturate(color, saturation)

    # Matplotlib handles
    ax = ax if ax is not None else plt.gca()
    fig = ax.figure
    gs = ax.get_subplotspec().subgridspec(3, 1, hspace=0.25)
    ax.axis('off')

    # Error plot
    rename = {
        'mdAP_localisation': 'LOC',
        'mdAP_classification': 'CLS',
        'mdAP_both': 'LOC+CLS',
        'mdAP_duplicate': 'DUPE',
        'mdAP_background': 'BKG',
        'mdAP_missed': 'MISS',
    }
    errors = tide_series[rename.keys()].rename(rename)
    if no_zero:
        errors = errors[errors > 0]

    error_ax = fig.add_subplot(gs[:-1])
    error_ax.bar(errors.index, errors.values, **kwargs)
    if errors_lim is not None:
        error_ax.set_ylim(errors_lim)

    # FPFN plot
    rename = {
        'mdAP_fp': 'FP',
        'mdAP_fn': 'FN',
    }
    fpfn = tide_series[rename.keys()].rename(rename)

    fpfn_ax = fig.add_subplot(gs[-1])
    fpfn_ax.barh(fpfn.index, fpfn.values, **kwargs)
    if fpfn_lim is not None:
        fpfn_ax.set_xlim(fpfn_lim)

    return ax
