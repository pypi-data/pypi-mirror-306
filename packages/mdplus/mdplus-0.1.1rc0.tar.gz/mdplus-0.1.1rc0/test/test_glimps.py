import os
import numpy as np
import pytest
try:
    import sklearn
except ImportError as e:
    pytest.skip("Scikit-learn not available", allow_module_level=True)
from mdplus import multiscale
from mdplus.utils import rmsd

rootdir = os.path.dirname(os.path.abspath('__file__'))
ncfile = os.path.join(rootdir, 'examples/test.nc')
pdbfile = os.path.join(rootdir, 'examples/test.pdb')
pczfile = os.path.join(rootdir, 'examples/test.pcz')
pczfile_dm = os.path.join(rootdir, 'examples/test_dm.pcz')
npyfile = os.path.join(rootdir, 'examples/test.npy')
npycafile = os.path.join(rootdir, 'examples/test_ca.npy')

@pytest.fixture(scope="module")
def cg_traj():
    return np.load(npycafile)

@pytest.fixture(scope="module")
def fg_traj():
    return np.load(npyfile)

def test_fit(cg_traj, fg_traj):
    g = multiscale.GLIMPS(x_valence=2)
    g.fit(cg_traj, fg_traj)

def test_fit_transform(cg_traj, fg_traj):
    g = multiscale.GLIMPS(x_valence=2)
    g.fit(cg_traj, fg_traj)
    ref = fg_traj[0]
    cg = cg_traj[0]
    fg = g.transform(cg)
    assert rmsd(ref, fg) < 0.2
