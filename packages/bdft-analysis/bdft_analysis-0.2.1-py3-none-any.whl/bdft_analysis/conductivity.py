# Warnning: None of the following has been tested,
# Its likey it doesnt even run properly
# How to exactly intergrate it with the above is also not fully worked out yet.

import numpy as np
from typing import Self

from bdft_analysis.immutiblenamespace import imns
# from plotting_utils import plt, plot_points

im = 0+1j


@imns
class KSpace:
    spacial_resolution: float = None

    kx: np.ndarray = None
    ky: np.ndarray = None

    wx: np.ndarray = None
    wy: np.ndarray = None

    DK: float = None
    Nx: int = None
    Ny: int = None

    mask: np.ndarray = None

    def ft(self, fk: np.ndarray) -> np.ndarray:
        return 2*np.pi * np.fft.fft(fk) / np.sqrt(self.kx.shape[0] * self.ky.shape[0])

    def ift(self, fw: np.ndarray) -> np.ndarray:
        return 2*np.pi * np.fft.ifft(fw) * np.sqrt(self.kx.shape[0] * self.ky.shape[0])

    # TODO: validate unitarity of FT
    def verify_unitarity_of_ft(self, test_function: np.ndarray):
        return test_function - self.ift(self.ft(test_function))

    def partial_kx(self, fk: np.ndarray) -> np.ndarray:
        return np.real(self.ift(
            np.einsum('ij,i->ij',
                      self.ft(fk),
                      self.wx * -im)))

    def partial_ky(self, fk: np.ndarray) -> np.ndarray:
        return np.real(self.ift(
            np.einsum('ij,j->ij',
                      self.ft(fk),
                      self.wy * -im)))

    def calculate_dule_space(self) -> Self:
        return self(
                wx = 2*np.pi*np.fft.fftfreq(self.kx.shape[0], 1/self.spacial_resolution[0]),
                wy = 2*np.pi*np.fft.fftfreq(self.ky.shape[0], 1/self.spacial_resolution[1]),
                )

    def calculate_LD(self) -> Self:
        Lx = self.kx[-1] - self.kx[0]
        Ly = self.ky[-1] - self.ky[0]
        dx = self.kx[1] - self.kx[0]
        dy = self.ky[1] - self.ky[0]
        Nx = self.kx.shape[0]
        Ny = self.ky.shape[0]
        return self(# Lx = Lx, Ly = Ly,
                    Nx = Nx, Ny = Ny,
                    DK = Lx*Ly / (Nx*Ny)**.5,
                    spacial_resolution=[dx, dy])

    def init_with_square_tile(self, delta: float = .5, tileing_number: int = 2,) -> Self:
        ky = np.arange(0, tileing_number * np.pi*4/3**.5, delta)
        kx = np.arange(0, tileing_number * np.pi*4/3*3,   delta)
        return self(kx = kx, ky = ky).calculate_LD().calculate_dule_space()

    def init_with_hex(self, dule_vectors: np.ndarray, N: int = 100):
        '''Given the primitive lattice vectors `dule_vectors` that define a triangular lattice,
        who's Wigner-Sitz cell is there for a hexagon, a space k-space will be initialised, along with a mask
        that selects points inside that Wigner-Sites hexagon.'''

        d1, d2 = dule_vectors
        B = 2/3*np.max(dule_vectors)
        linspace = np.linspace(-B, B, N)
        test_points = np.array(np.meshgrid(linspace, linspace)).transpose()

        control_points = [d1, d1 + d2, d2]
        mask = np.ones(test_points.shape[:-1], dtype=bool)

        for cp in control_points:
            mask *= np.abs(np.einsum('abi,i->ab', test_points, cp)) < np.dot(cp, cp)/2
            # | test_point dot control_point | < 1/2
            # control points are the nerist naobur cites of the triangular lattice
            # d1 

        return self(
                kx = linspace,
                ky = linspace,
                mask = mask,
                ).calculate_LD().calculate_dule_space()

    def integrate(self, integrand: np.ndarray) -> float:
        if self.mask is not None:
            integrand = integrand[self.mask]
        return self.DK * np.sum(integrand)

    def k_mesh(self) -> np.ndarray:
        return np.array(np.meshgrid(self.kx, self.ky)).transpose([2, 1, 0])

    def reshape_mesh_to_points(self, mesh: np.ndarray) -> np.ndarray:
        return mesh.reshape(self.Nx*self.Ny, -1)

    def reshape_points_to_mesh(self, points: np.ndarray) -> np.ndarray:
        return points.reshape(self.Nx, self.Ny, -1)

    def _check_reshapes(self) -> Self:
        mesh = self.k_mesh()
        assert np.all(mesh == self.reshape_points_to_mesh(self.reshape_mesh_to_points(mesh)))
        return self

    def _check_dimentions_of_kmesh(self) -> Self:
        assert self.k_mesh().shape == (self.Nx, self.Ny, 2)
        return self

    def plot_k_points(self, ax=None):
        if ax is None:
            import matplotlib.pyplot as plt
            _, ax = plt.subplots()

        ax.scatter(*self.k_mesh().transpose(), s=.2, label='points outside mask')
        ax.scatter(*self.k_mesh()[self.mask].transpose(), s=.3, label='points inside mask')

        ax.set_aspect(1)
        ax.set_title('K-points')
        ax.legend()

        return ax


@imns
class Classical_Conductivity:
    Energy: np.ndarray = None
    hbar: float = 1
    e: float = 1
    kspace: KSpace = None
    tau: float = 100
    EField: np.ndarray = lambda: np.array([1, 0])
    kernel_factor: np.ndarray = None
    sigma: np.ndarray = None

    def init_kspace(self, **kwargs) -> Self:
        return self(
                kspace = (KSpace(**kwargs)
                          .calculate_LD()
                          .calculate_dule_space()
                          )
                )

    def calculate_kernel_factor(self) -> Self:
        ''' Z(wx, wy) = 1/(1+1im*(τ*e/hbar)*(wx*Efield_x + wy*Efield_y))
            kernel_factor(wx, wy) = 1im*(e^2 * τ)/(hbar^2) .* (Z.(wx, wy)).^2 '''

        Zinv = 1 + im * (self.tau * self.e / self.hbar) * (
                (self.kspace.wx * self.EField[0])[:, np.newaxis] +
                (self.kspace.wy * self.EField[1])[np.newaxis, :]
                ) # indicies read [x][y]

        kf = im * self.e**2 * self.tau * self.hbar**-2 * Zinv**-2

        return self(kernel_factor = kf)

    def calculate_conductivity(self) -> Self:
        ''' ∂Ekx = ∂kx(E.(kx, ky))
            ∂Eky = ∂ky(E.(kx, ky))

            KF = kernel_factor.(wx, wy)
            KF_kx = KF .* wx |> ift
            KF_ky = KF .* wy |> ift

            σ_11 = -1*Δk*sum( ∂Ekx .* KF_kx )
            σ_12 = -1*Δk*sum( ∂Ekx .* KF_ky )
            σ_21 = -1*Δk*sum( ∂Eky .* KF_kx )
            σ_22 = -1*Δk*sum( ∂Eky .* KF_ky )

            return [σ_11 σ_21; σ_12 σ_22]'''

        partial_Ekx = self.kspace.partial_kx(self.Energy)
        partial_Eky = self.kspace.partial_ky(self.Energy)

        KF_kx = self.kspace.ift(np.einsum('xy,x -> xy', self.kernel_factor, self.kspace.wx))
        KF_ky = self.kspace.ift(np.einsum('xy,y -> xy', self.kernel_factor, self.kspace.wy))

        sigma = np.zeros((2, 2))
        sigma[0, 0] = -1 * self.kspace.integrate(partial_Ekx * KF_kx)
        sigma[0, 1] = -1 * self.kspace.integrate(partial_Ekx * KF_ky)
        sigma[1, 0] = -1 * self.kspace.integrate(partial_Eky * KF_kx)
        sigma[1, 1] = -1 * self.kspace.integrate(partial_Eky * KF_ky)

        return self(sigma = sigma)
