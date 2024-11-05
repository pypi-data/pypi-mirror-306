#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3rd party imports
import numpy as np
import xarray as xr

from .dot import dot

# Local imports
from .resample import resample

__author__ = "Louis Richard"
__email__ = "louisr@irfu.se"
__copyright__ = "Copyright 2020-2023"
__license__ = "MIT"
__version__ = "2.4.2"
__status__ = "Prototype"


def dec_par_perp(inp, b_bgd, flag_spin_plane: bool = False):
    r"""Decomposes a vector into par/perp to B components. If flagspinplane
    decomposes components to the projection of ``b0`` into the XY plane.
    ``alpha`` gives the angle between ``b0`` and the XY. plane.

    Parameters
    ----------
    inp : xarray.DataArray
        Time series of the field to decompose.
    b_bgd : xarray.DataArray
        Time series of the background magnetic field.
    flag_spin_plane : bool, Optional
        Flag if True gives the projection in XY plane.

    Returns
    -------
    a_para : xarray.DataArray
        Time series of the input field parallel to the background magnetic
        field.
    a_perp : xarray.DataArray
        Time series of the input field perpendicular to the background
        magnetic field.
    alpha : xarray.DataArray
        Time series of the angle between the background magnetic field and
        the XY plane.

    Examples
    --------
    >>> from pyrfu import mms, pyrf

    Time interval

    >>> tint = ["2019-09-14T07:54:00.000", "2019-09-14T08:11:00.000"]

    Spacecraft index

    >>> mms_id = 1

    Load magnetic field (FGM) and electric field (EDP)

    >>> b_xyz = mms.get_data("B_gse_fgm_brst_l2", tint, mms_id)
    >>> e_xyz = mms.get_data("E_gse_edp_brst_l2", tint, mms_id)

    Decompose e_xyz into parallel and perpendicular to b_xyz components

    >>> e_para, e_perp, _ = pyrf.dec_par_perp(e_xyz, b_xyz)

    """

    # Check arguments types
    assert isinstance(inp, xr.DataArray), "inp must be an xarray.DataArray"
    assert isinstance(b_bgd, xr.DataArray), "b_bgd must be an xarray.DataArray"
    assert isinstance(flag_spin_plane, bool), "flag_spin_plane must be boolean"

    # Check inp and b_bgd shapes
    assert inp.ndim == 2 and inp.shape[1], "inp must be a vector"
    assert b_bgd.ndim == 2 and b_bgd.shape[1], "b_bgd must be a vector"

    if not flag_spin_plane:
        b_mag = np.linalg.norm(b_bgd, axis=1, keepdims=True)

        indices = np.where(b_mag < 1e-3)[0]

        if indices.size > 0:
            b_mag[indices] = np.ones((len(indices), 1)) * 1e-3

        b_hat = b_bgd / b_mag
        b_hat = resample(b_hat, inp)

        a_para = dot(b_hat, inp)
        a_perp = inp - (b_hat.data * np.tile(a_para.data[:, np.newaxis], (1, 3)))
        alpha = []
    else:
        b_bgd = resample(b_bgd, inp)
        b_tot = np.sqrt(b_bgd[:, 0] ** 2 + b_bgd[:, 1] ** 2)
        b_bgd /= b_tot.data[:, np.newaxis]

        a_para = inp[:, 0] * b_bgd[:, 0] + inp[:, 1] * b_bgd[:, 1]
        a_perp = inp[:, 0] * b_bgd[:, 1] - inp[:, 1] * b_bgd[:, 0]
        alpha = np.arctan2(b_bgd[:, 2], b_tot)

    return a_para, a_perp, alpha
