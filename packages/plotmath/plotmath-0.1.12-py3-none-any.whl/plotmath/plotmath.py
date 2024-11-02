import pathlib

import numpy as np
import matplotlib.pyplot as plt


import warnings

# Attempt to enable LaTeX rendering
try:
    plt.rc("text", usetex=True)
    # Test rendering a simple LaTeX expression
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, r"$E=mc^2$", fontsize=12)
    plt.close(fig)  # Close the figure as it's only for testing
except (FileNotFoundError, RuntimeError):
    plt.rc("text", usetex=False)
    # warnings.warn(
    #     "LaTeX is not available. Falling back to Matplotlib's default text rendering.",
    #     UserWarning,
    # )

colors = ["#029386", "#C875C4", "#E50000", "blue", "purple", "orange"]
# colors = np.random.permutation(colors)
plt.rcParams["axes.prop_cycle"] = plt.cycler(color=colors)


def show():
    plt.show()


def _get_figure_and_axis():
    fig, ax = plt.subplots()
    ax.spines["left"].set_position("zero")
    ax.spines["right"].set_color("none")
    ax.spines["bottom"].set_position("zero")
    ax.spines["top"].set_color("none")

    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

    ax.set_xlabel(r"$x$", fontsize=16, loc="right")
    ax.set_ylabel(r"$y$", fontsize=16, loc="top", rotation="horizontal")

    return fig, ax


def _set_ticks(xmin, xmax, ymin, ymax):

    xticks = list(np.arange(xmin + 1, xmax, 1))
    if len(xticks) > 10:
        if xmin % 2 == 0:
            xmin = xmin + 1
        if xmax % 2 == 0:
            xmax = xmax - 1

        n_step = 1
        while len(xticks) > 11:
            n_step *= 2
            xticks = list(np.arange(xmin + 1, xmax, n_step))

    if 0 in xticks:
        xticks.remove(0)
    plt.xticks(xticks, fontsize=16)

    yticks = list(np.arange(ymin + 1, ymax, 1))
    if len(yticks) > 11:
        if ymin % 2 == 0:
            ymin = ymin + 1
        if ymax % 2 == 0:
            ymax = ymax - 1

        n_step = 1
        while len(yticks) > 10:
            n_step *= 2
            yticks = list(np.arange(ymin + 1, ymax, n_step))

    if 0 in yticks:
        yticks.remove(0)
    plt.yticks(yticks, fontsize=16)

    return None


def plot(
    functions,
    fn_labels=True,
    xmin=-5,
    xmax=5,
    ymin=-5,
    ymax=5,
    ticks=True,
    alpha=0.7,
    grid=True,
    domain=None,
):
    fig, ax = _get_figure_and_axis()

    if ticks:
        _set_ticks(xmin, xmax, ymin, ymax)
    else:
        plt.xticks([])
        plt.yticks([])

    # If domain is provided
    if domain:
        a, b = domain
        try:
            tmp = [f(a) for f in functions]
            tmp = [f(b) for f in functions]
        except:
            raise ValueError(
                f"One of the provided functions is not defined on the provided domain: {domain}"
            )
    else:
        a = -50
        b = 50
        try:
            tmp = [f(a) for f in functions]
            tmp = [f(b) for f in functions]
        except:
            raise ValueError(
                f"One of the provided functions is not defined on the default domain: {[a, b]}. Provide an approriate domain"
            )

    x = np.linspace(a, b, 1024)

    if isinstance(fn_labels, bool) and fn_labels:  # If True, automatically set labels
        fn_labels = [f"${fn.__name__}$" for fn in functions]
    elif isinstance(fn_labels, bool) and not fn_labels:  # If False, disable labels
        fn_labels = None
    # Otherwise the code will apply user-specified labels

    if fn_labels is not None:
        for f, label in zip(functions, fn_labels):
            ax.plot(x, f(x), lw=2, alpha=alpha, label=label)

        ax.legend(fontsize=16)

    else:
        for f in functions:
            ax.plot(x, f(x), lw=2, alpha=alpha)

    plt.ylim(ymin, ymax)
    plt.xlim(xmin, xmax)

    if grid:
        plt.grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()

    return fig, ax


def savefig(dirname, fname):
    dir = pathlib.Path(dirname)
    dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(f"{dir}/{fname}")

    return None
