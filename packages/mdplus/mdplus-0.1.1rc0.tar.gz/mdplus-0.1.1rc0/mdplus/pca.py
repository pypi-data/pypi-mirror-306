# pca.py - PCA routines for MD trajectory data.

# from mdplus import fast
from mdplus.utils import Procrustes, check_dimensions
# from mdplus.compression import zigzag_encode, zigzag_decode, squeeze, stretch
# from sklearn.decomposition import PCA as skPCA
# import zlib
# import xdrlib
import numpy as np

'''
def pcazipsave(xyz, filename, explained_variance=0.75, residual_scale=200,
               eigenvector_scale=100):
    p = PCA(n_components=explained_variance)
    scores = p.fit_transform(xyz)
    evecs = p._pca.components_
    mean = p.mean
    n_frames, n_atoms, _ = xyz.shape
    n_vecs = p.n_components
    if residual_scale > 0:
        xfitted = fit(xyz, mean.reshape((n_atoms, 3)))
        residuals = xfitted - p.inverse_transform(scores)
        iresiduals = (residuals * residual_scale).astype(np.int32)
    iscores = (scores * 1000).astype(np.int32)
    ievecs = (evecs * eigenvector_scale *
     np.sqrt(n_atoms)).astype(np.int32).flatten()
    imean = (mean * 1000).astype(np.int32).flatten()
    magic = np.frombuffer(bytearray('PCZX', 'utf-8'), dtype=np.int32)[0]
    metadata = np.array([magic, n_frames, n_atoms, n_vecs, residual_scale,
     eigenvector_scale], dtype=np.int32)
    header = np.concatenate([metadata, imean, ievecs])
    pa = xdrlib.Packer()
    with open(filename, 'wb') as f:
        pa.pack_bytes(squeeze(header))
        if residual_scale > 0:
            for i, r in zip(iscores, iresiduals):
                pa.pack_bytes(squeeze(np.concatenate((i, r.flatten()))))
                f.write(pa.get_buffer())
                pa.reset()
        else:
            for i in iscores:
                pa.pack_bytes(squeeze(i))
                f.write(pa.get_buffer())
                pa.reset()


def pcazipload(filename):
    with open(filename, 'rb') as f:
        u = xdrlib.Unpacker(f.read())
        header = stretch(u.unpack_bytes())
        magic = header[0].tobytes()
        if magic != b'PCZX':
            raise TypeError('Error, unrecognised file type' +
             ' (magic={})'.format(magic))
        (n_frames, n_atoms, n_vecs, residual_scale,
         eigenvector_scale) = header[1:6]
        meanoff = 6
        evecoff = meanoff + 3 * n_atoms
        mean = header[meanoff:evecoff].astype(np.float32) / 1000
        evecs = header[evecoff:].astype(np.float32).reshape((n_vecs, 3*n_atoms)
         ) / (eigenvector_scale * np.sqrt(n_atoms))
        xyz = np.zeros((n_frames, n_atoms, 3), dtype=np.float32)
        for i in range(n_frames):
            data = stretch(u.unpack_bytes())
            scores = data[:n_vecs].astype(np.float32) / 1000
            if residual_scale > 0:
                residuals = data[n_vecs:].astype(np.float32) / residual_scale
                x = mean + np.dot(scores, evecs) + residuals
            else:
                x = mean + np.dot(scores, evecs)

            xyz[i] = x.reshape((n_atoms, 3))
    return xyz
'''


class PCA(object):
    """
    PCA for MD trajectory data, with an API like scikit-learn PCA

    With a [n_frames, n_atoms, 3] array of coordinates:

        pca = PCA()
        pca.fit(X)
        scores = pca.transform(X)

    Attributes:
        n_atoms: int, number of atoms
        n_components: int, number of PCA components
        mean: [n_atoms, 3] array, mean structure
        eigenvalues: [n_components] array

    """
    def __init__(self, n_components=None):
        self.n_components = n_components

    def fit(self, traj):
        """
        Build the PCA model.

        Args:
            traj: [n_frames, n_atoms, 3] numpy array of coordinates.
        """
        traj = check_dimensions(traj)
        n_frames = traj.shape[0]
        self.n_atoms = traj.shape[1]
        

        if self.n_components is not None:
            if (self.n_components > 1 and
               self.n_components > min(n_frames, 3 * self.n_atoms)):
                raise ValueError(
                    'Error: cannot find' +
                    ' {} principal components'.format(self.n_components) +
                    ' from a trajectory of {}'.format(n_frames) +
                    ' frames of {} atoms'.format(self.n_atoms))
        else:
            self.n_components = min(n_frames, 3*self.n_atoms)

        self._fitter = Procrustes()
        fitted_traj = self._fitter.fit_transform(traj)
        covariance_matrix = np.cov(fitted_traj.reshape((n_frames, -1)).T)
        eigen_values, eigen_vectors = np.linalg.eigh(covariance_matrix)
        self.eigenvalues = eigen_values[::-1]
        self.eigenvectors = eigen_vectors[:, ::-1]
        if self.n_components < 1:
            total_variance = self.eigenvalues.sum()
            nc = 0
            ev = 0.0
            while ev < total_variance * self.n_components:
                nc += 1
                ev += self.eigenvalues[nc-1]
            self.n_components = nc
        self.eigenvalues = self.eigenvalues[:self.n_components]
        self.eigenvectors = self.eigenvectors[:, :self.n_components]
        self.mean = self._fitter.mean

    def transform(self, traj):
        """
        Transform the trajectory frames into the PCA space.

        Args:
            traj: [n_frames, n_atoms, 3] numpy array of coordinates.

        Returns:
            An [n_frames, n_components)
        """
        traj = check_dimensions(traj)
        n_atoms = traj.shape[1]
        if n_atoms != self.n_atoms:
            raise ValueError('Error: trajectory has {} atoms'.format(n_atoms) +
                             ' but the model requires {}'.format(self.n_atoms))
        traj = self._fitter.transform(traj) - self.mean
        n_frames = traj.shape[0]
        traj = traj.reshape((n_frames, -1))
        scores = np.zeros((n_frames, self.n_components))
        for i in range(n_frames):
            scores[i] = traj[i].dot(self.eigenvectors)
        return scores

    def inverse_transform(self, traj):
        """
        Transform frames back from PCA space to Cartesian space

        Args:
            traj: an [n_components] or [n_frames, n_components] array

        Returns:
            an [n_frames, n_atoms, 3] array
        """
        traj = np.array(traj)
        if len(traj.shape) > 2 or traj.shape[-1] != self.n_components:
            raise ValueError('Error: traj must be a vector of' +
                             ' length {}'.format(self.n_components) +
                             ' or an array of shape' +
                             ' [any,{}]'.format(self.n_components))
        if len(traj.shape) == 1:
            traj = traj.reshape((1, -1))
        n_frames = len(traj)
        crds = np.zeros((n_frames, self.n_atoms * 3))
        for i in range(n_frames):
            crds[i] = traj[i].dot(self.eigenvectors.T)
        crds = crds.reshape((n_frames, self.n_atoms, 3)) + self.mean
        
        return crds

    def fit_transform(self, traj):
        """
        Fit the PCA model and return the transformed data

        Args:
            traj: [n_frames, n_atoms, 3] numpy array of coordinates.

        Returns:
            An [n_frames, n_components] array
        """
        traj = check_dimensions(traj)
        self.fit(traj)
        return self.transform(traj)
