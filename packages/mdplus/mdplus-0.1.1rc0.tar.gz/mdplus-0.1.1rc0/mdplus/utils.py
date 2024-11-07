# utils.py
# from mdplus.fast import rmsd_traj, fitted_traj, fitted_mean
import numpy as np
from scipy.spatial.transform import Rotation as R


def _rmsd_traj(traj, ref):
    """
    Calculate the rmsd between each frame in traj and ref

    """
    n_frames, n_atoms, _ = traj.shape
    rmsd = np.zeros(n_frames)
    lref = ref - ref.mean(axis=0)
    fac = np.sqrt(n_atoms)
    for i in range(n_frames):
        lf = traj[i] - traj[i].mean(axis=0)
        rot, rssd = R.align_vectors(lref, lf)
        rmsd[i] = rssd / fac
    return rmsd


def _fitted_traj(traj, ref):
    """
    return a copy of traj least-squares fitted to ref

    """
    n_frames = len(traj)
    fitted = np.zeros_like(traj)
    vref = ref.mean(axis=0)
    lref = ref - vref
    for i in range(n_frames):
        lf = traj[i] - traj[i].mean(axis=0)
        rot, rssd = R.align_vectors(lref, lf)
        fitted[i] = rot.apply(lf) + vref
    return fitted


def _fitted_mean(traj, ref):
    """
    Return the mean coordinates of traj fitted to ref

    """
    n_frames = len(traj)
    mean = np.zeros_like(ref)
    vref = ref.mean(axis=0)
    lref = ref - vref
    for i in range(n_frames):
        lf = traj[i] - traj[i].mean(axis=0)
        rot, rssd = R.align_vectors(lref, lf)
        mean += rot.apply(lf) + vref
    return mean / n_frames


def rmsd(traj, xref):
    """
    Calculate rmsd between coordinates in traj and xref)

    Args:
        traj: [n_atoms, 3] or [n_frames_n_atoms, 3] array
        xref: [n_atoms, 3] or [n_frames_n_atoms, 3] array

    Returns:
        float or vector or array depending on dhapes of traj and xref
    """
    traj = check_dimensions(traj)
    xref = check_dimensions(xref)
    rmsd = np.zeros((len(traj), len(xref)))
    for i, r in enumerate(xref):
        rmsd[:, i] = _rmsd_traj(traj, r)
    if rmsd.shape[1] == 1:
        rmsd = rmsd.flatten()
    if len(rmsd) == 1:
        rmsd = rmsd[0]
    return rmsd


def fit(traj, xref):
    """
    Least squares fit a trajectory to a reference structure

    Args:
        traj: [n_atoms, 3] or [n_frames_n_atoms, 3] array
        xref: [n_atoms, 3] or [n_frames_n_atoms, 3] array. if the latter,
              the first coordinate set is used for the fit.

    Returns:
        [n_frames, n_atoms, 3] array of fitted coordinates.f
    """
    traj = check_dimensions(traj)
    xref = check_dimensions(xref)

    fitted = _fitted_traj(traj, xref[0])

    return fitted


def check_dimensions(traj):
    """
    Check and regularize a trajectory array
    """
    if not isinstance(traj, np.ndarray):
        traj = np.array(traj)
    if len(traj.shape) < 2 or len(traj.shape) > 3 or traj.shape[-1] != 3:
        raise ValueError('Error: traj must be an [n_atoms, 3]' +
                         ' or [n_frames, n_atoms, 3] array')
    if len(traj.shape) == 2:
        traj = traj.reshape((1, -1, 3))
    return traj


class Procrustes(object):

    def __init__(self, max_its=10, drmsd=0.01):
        """
        Initialise a procrustes least-squares fitter.
        
        Args:
            max_its: int, maximum number of iterations
            drmsd: float, target rmsd between successive means for convergence
        """
        self.max_its = max_its
        self.drmsd = drmsd

    def fit(self, X):
        """
        Train the fitter.

        Args:
            X: [n_frames, n_atoms, 3] numpy array
        """
        X = check_dimensions(X)
        old_mean = X[0].copy()
        err = self.drmsd + 1.0
        it = 0
        while err > self.drmsd and it < self.max_its:
            it += 1
            new_mean = _fitted_mean(X, old_mean)
            err = rmsd(old_mean, new_mean)
            old_mean = new_mean

        self.converged = err <= self.drmsd
        self.mean = old_mean

    def transform(self, X):
        """
        Least-squares fit the coordinates in X.

        Args:
            X: [n_frames, n_atoms, 3] numpy array
        Returns:
            [n_frames, n_atoms, 3] numpy array of fitted coordinates
        """
        X = check_dimensions(X)
        return fit(X, self.mean)

    def fit_transform(self, X):
        """
        Train the fitter, and apply to X.

        Args:
            X: [n_frames, n_atoms, 3] numpy array
        Returns:
            [n_frames, n_atoms, 3] numpy array of fitted coordinates
        """
        self.fit(X)
        return self.transform(X)
