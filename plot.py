#
#   Matplotlib plotting functions for notebooks
#   Tanguy Ophoff
#

def plot_images(*images, nrows=None, ncols=None, titles=None, normalize=True):
    """
    This function can plot images in a grid with matplotlib.

    Args:
        *images (PIL.Image, torch.Tensor, np.ndarray): Images to plot (numpy arrays are expected to be BGR from opencv)
        nrows (int, optional): Number of rows in the grid (takes precedence over `ncols`); Default: None
        ncols (int, optional): Number of columns in the grid; Default: None
        titles (list[str], optional): Title strings for the different images; Default: None
        normalize (bool, optional): Whether to rescale the image data from min-max to 0-255; Default: True

    Returns:
        (matplotlib.figure.Figure): Matplotlib figure handle

    Libraries:
        matplotlib
        numpy
        torch (optional)
        PIL (optional)

    Example:
        >>> plot_images(img1, img2, img3, img4, rows=2)
        >>> plt.show()
    """
    import math
    import numpy as np
    import matplotlib.pyplot as plt
    try:
        import torch
    except ImportError:
        torch = None
    try:
        from PIL import Image
    except ImportError:
        Image = None

    def image_to_array(img):
        if torch is not None and isinstance(img, torch.Tensor):
            return np.transpose(img.cpu().detach().numpy(), (1, 2, 0))
        if Image is not None and isinstance(img, Image.Image):
            return np.asarray(img)
        if isinstance(img, np.ndarray) and img.ndim == 3:
            return img[..., ::-1]
        return np.asarray(img)

    images = tuple(image_to_array(img) for img in images)
    avg_ratio = sum(img.shape[0] for img in images) / sum(img.shape[1] for img in images)
    if nrows is not None:
        ncols = math.ceil(len(images) / nrows)
    elif ncols is not None:
        nrows = math.ceil(len(images) / ncols)
    else:
        nrows = 1
        ncols = len(images)        
    fig, axes = plt.subplots(nrows, ncols, figsize=(4*ncols, 4*avg_ratio*nrows), constrained_layout=True)
    axes = axes.flatten()

    for idx, (ax, img) in enumerate(zip(axes, images)):
        if normalize:
            ax.imshow(img, cmap='gray')
        else:
            ax.imshow(img, vmin=0, vmax=255 if img.max() > 1 else 1, cmap='gray')
        
        ax.grid(False)
        ax.tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False) 
        ax.spines['bottom'].set(edgecolor='black', lw=1)
        ax.spines['top'].set(edgecolor='black', lw=1)
        ax.spines['left'].set(edgecolor='black', lw=1)
        ax.spines['right'].set(edgecolor='black', lw=1)
        if titles is not None and len(titles) > idx:
            ax.set_title(titles[idx])

    return fig

def plot_tide(tide_series, *, errors_lim=None, fpfn_lim=None, no_zero=False, color=None, saturation=0.75, ax=None, **kwargs):
    """
    This function can plot the results of a `brambox.eval.TIDE` series with matplotlib.

    Args:
        tide_series (pd.Series): Series with tide values as returned by bb.eval.TIDE
        errors_lim (list): Axis limits for the errors barplot; Default None
        fpfn_lim (list): Axis limits for the fpfn barplot; Default None
        no_zero (bool): Remove errors if they are zero; Default False
        color (matplotlib color): hex, rgb-tuple or html color name for the barplots; Default None
        saturation (float): saturation value for the barplot colors (only works if seaborn is installed); Default 0.75
        ax (matplotlib ax): Ax to draw the plots on; Default plt.gca()
        kwargs: Extra keyword arguments passed to the barplot functions

    Returns:
        (matplotlib.figure.Figure): Matplotlib figure handle

    Required Libraries:
        matplotlib
        seaborn (optional)

    Example:
        >>> tide = bb.eval.TIDE(det, anno).mdAP
        >>> plot_tide(tide)
        >>> plt.show()
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

    return fig


if __name__ == '__main__':
    print('functions: plot_images, plot_tide')
