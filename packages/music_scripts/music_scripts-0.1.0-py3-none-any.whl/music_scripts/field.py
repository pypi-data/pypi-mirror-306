from __future__ import annotations

import typing

import numpy as np
from matplotlib import colors
from pymusic.plotting import Plot

from .figure import SinglePlotFigure
from .fort_pp import Contour, ContourPlot, ContourSphericalPlot
from .musicdata import MusicData
from .plots import SameAxesPlot, ScalarPlot, SphericalVectorPlot

if typing.TYPE_CHECKING:
    from typing import List, Sequence

    from .config import Config, Field
    from .musicdata import Snap


def plot_field(
    snap: Snap,
    conf_field: Field,
    no_rmarks: bool = False,
) -> Sequence[Plot]:
    cmap = conf_field.cmap
    if conf_field.perturbation and cmap is None:
        cmap = "RdBu_r"

    normr = not conf_field.full_r
    mdat = snap.mdat

    try:
        rtot = mdat.prof1d.params["rad_surf"] if normr else None
        renv = mdat.prof1d.params["renv/rtot" if normr else "renv"]
        rcore = mdat.prof1d.params["rcore/rtot" if normr else "rcore"]
    except RuntimeError:
        rtot = None
        renv = 0.0
        rcore = 0.0
    rschwarz = [rad for rad in (renv, rcore) if rad > 0.0]
    if no_rmarks:
        rschwarz = []

    plots: List[Plot] = [
        ScalarPlot(
            snap=snap,
            var=conf_field.plot,
            cmap=cmap,
            norm=(
                None
                if not conf_field.perturbation
                else colors.SymLogNorm(linthresh=1e-6)
            ),
            costh=conf_field.costh,
            rbounds=(conf_field.rmin, conf_field.rmax),
            vbounds=(conf_field.vmin, conf_field.vmax),
            normalize_r=rtot,
            perturbation=conf_field.perturbation,
        ),
    ]
    if conf_field.velarrow:
        plots.append(
            SphericalVectorPlot(
                snap=snap,
                vec_r="vel_1",
                vec_t="vel_2",
            )
        )
    contours = [
        Contour(
            "rschwarz",
            np.full_like(theta := snap.grid.grids[1].cell_centers(), rad),
            theta if not conf_field.costh else np.cos(theta),
        )
        for rad in rschwarz
    ]
    if conf_field.costh:
        plots.extend(ContourPlot(ctr) for ctr in contours)
    else:
        plots.extend(ContourSphericalPlot(ctr) for ctr in contours)
    return plots


def cmd(conf: Config) -> None:
    conf.core.figdir.mkdir(parents=True, exist_ok=True)

    var = conf.field.plot
    mdat = MusicData(conf.core.path)

    for snap in mdat[conf.core.dumps]:
        plots = plot_field(snap, conf.field, conf.plotting.no_rmarks)
        SinglePlotFigure(
            plot=SameAxesPlot(plots=plots, legend=False),
        ).save_to(conf.core.figdir / f"{var}_{snap.idump:08d}.png")
