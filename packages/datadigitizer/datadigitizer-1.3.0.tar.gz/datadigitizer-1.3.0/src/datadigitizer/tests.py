r"""
Tests module.
"""
import pathlib
import unittest
import numpy as np
import matplotlib.pyplot as plt
from .settings import CFG_FOLDER


def test_linear() -> pathlib.Path:
    r"""
    Generate the linear plot and data.

    Returns
    -------
    fpath: Path object
        Path to the linear plot.
    """
    x = np.arange(0, 10, 1)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    y = 1*x+1
    ax.plot(x, y, 'k+')
    m = np.vstack((x, y)).transpose()
    name = 'linear'
    ext = '.txt'
    fpath = pathlib.Path(CFG_FOLDER) / (str(name) + ext)
    np.savetxt(fpath, X=m, header='x\ty', delimiter='\t')
    ext = '.png'
    fpath = pathlib.Path(CFG_FOLDER) / (str(name) + ext)
    fig.savefig(fpath, dpi=100, format='png')

    return fpath


def test_ylog() -> pathlib.Path:
    r"""
    Generate the semi-log plot and data.

    Returns
    -------
    fpath: Path object
        Path to the semi-log plot.
    """
    x = np.arange(0, 10, 1)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    y = 10**x
    ax.plot(x, y, 'k+')
    ax.set_yscale('log')
    m = np.vstack((x, y)).transpose()
    name = 'ylog'
    ext = '.txt'
    fpath = pathlib.Path(CFG_FOLDER) / (str(name) + ext)
    np.savetxt(fpath, X=m, header='x\ty', delimiter='\t')
    ext = '.png'
    fpath = pathlib.Path(CFG_FOLDER) / (str(name) + ext)
    fig.savefig(fpath, dpi=100, format='png')

    return fpath


def test_xlog() -> pathlib.Path:
    r"""
    Generate the semi-log plot and data.

    Returns
    -------
    fpath: Path object
        Path to the semi-log plot.
    """
    x = np.arange(0, 10, 1)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    y = 10**x
    ax.plot(y, x, 'k+')
    ax.set_xscale('log')
    m = np.vstack((x, y)).transpose()
    name = 'xlog'
    ext = '.txt'
    fpath = pathlib.Path(CFG_FOLDER) / (str(name) + ext)
    np.savetxt(fpath, X=m, header='x\ty', delimiter='\t')
    ext = '.png'
    fpath = pathlib.Path(CFG_FOLDER) / (str(name) + ext)
    fig.savefig(fpath, dpi=100, format='png')

    return fpath


def test_loglog() -> pathlib.Path:
    r"""
    Generate the log-log plot and data.

    Returns
    -------
    fpath: Path object
        Path to the log-log plot.
    """
    x = np.arange(0, 10, 1)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    y = 10**x
    ax.plot(y, y, 'k+')
    ax.loglog()
    m = np.vstack((x, y)).transpose()
    name = 'loglog'
    ext = '.txt'
    fpath = pathlib.Path(CFG_FOLDER) / (str(name) + ext)
    np.savetxt(fpath, X=m, header='x\ty', delimiter='\t')
    ext = '.png'
    fpath = pathlib.Path(CFG_FOLDER) / (str(name) + ext)
    fig.savefig(fpath, dpi=100, format='png')

    return fpath

class TestPlotData(unittest.TestCase):
    r"""Test and generate test plots."""

    def test_linear(self):
        r"""Test linear plot."""
        fpath = test_linear()
        self.assertTrue(isinstance(fpath, pathlib.Path))
    
    def test_ylog(self):
        r"""Test y semi-log plot."""
        fpath = test_ylog()
        self.assertTrue(isinstance(fpath, pathlib.Path))
    
    def test_xlog(self):
        r"""Test x semi-log plot."""
        fpath = test_xlog()
        self.assertTrue(isinstance(fpath, pathlib.Path))
    
    def test_loglog(self):
        r"""Test log-log plot."""
        fpath = test_loglog()
        self.assertTrue(isinstance(fpath, pathlib.Path))