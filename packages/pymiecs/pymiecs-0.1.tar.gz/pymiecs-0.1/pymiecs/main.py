# Mie observables
# %%
import warnings

import numpy as np
from pymiecs.mie_coeff import core_shell_ab


def Q(
    k0,
    r_core,
    n_core,
    r_shell=None,
    n_shell=1,
    mu_core=1,
    mu_shell=1,
    n_env=1,
    mu_env=1,
    n_max="auto",
):
    k = k0 * n_env
    
    if r_shell is None:
        r_shell = r_core

    if len(np.shape(k)) == 0:
        k = np.array([k])
    if len(np.shape(k)) == 1:
        k = k[None, :]

    if n_max == "auto":
        # Wiscombe criterion for farfield
        ka = r_shell * k
        n_max = int(np.max(np.round(2 + ka + 4.05 * (ka ** (1 / 3)))))

    n = np.arange(1, n_max + 1)[:, None]

    a, b = core_shell_ab(
        k0=k0,
        r_core=r_core,
        n_core=n_core,
        r_shell=r_shell,
        n_shell=n_shell,
        mu_core=mu_core,
        mu_shell=mu_shell,
        n_env=n_env,
        mu_env=mu_env,
        n_max=n_max,
    )

    # geometric cross section
    cs_geo = np.pi * r_shell**2

    # scattering efficiencies
    prefactor = 2 / (k**2 * r_shell**2)
    qext = prefactor * np.sum((2 * n + 1) * (a.real + b.real), axis=0)
    qsca = prefactor * np.sum(
        (2 * n + 1) * (a.real**2 + a.imag**2 + b.real**2 + b.imag**2), axis=0
    )
    qabs = qext - qsca

    # separate multipole contributions
    qext_e = prefactor * (2 * n + 1) * (a.real)
    qsca_e = prefactor * (2 * n + 1) * (a.real**2 + a.imag**2)
    qext_m = prefactor * (2 * n + 1) * (b.real)
    qsca_m = prefactor * (2 * n + 1) * (b.real**2 + b.imag**2)
    qabs_e = qext_e - qsca_e
    qabs_m = qext_m - qsca_m

    # fw / bw scattering
    qback = (prefactor / 2) * (
        np.abs(np.sum((2 * n + 1) * ((-1) ** n) * (a - b), axis=0)) ** 2
    )
    qfwd = (prefactor / 2) * (np.abs(np.sum((2 * n + 1) * (a + b), axis=0)) ** 2)
    qratio = qback / qfwd

    return dict(
        qext=qext,
        qsca=qsca,
        qabs=qabs,
        qext_e=qext_e,
        qsca_e=qsca_e,
        qabs_e=qabs_e,
        qext_m=qext_m,
        qsca_m=qsca_m,
        qabs_m=qabs_m,
        qfwd=qfwd,
        qback=qback,
        qratio=qratio,
        cs_geo=cs_geo,
    )


def pi_tau(u, n_max):
    #  http://pymiescatt.readthedocs.io/en/latest/forward.html#MiePiTau
    p = np.zeros(int(n_max))
    t = np.zeros(int(n_max))
    p[0] = 1
    p[1] = 3 * u
    t[0] = u
    t[1] = 3.0 * np.cos(2 * np.arccos(u))
    for n in range(2, int(n_max)):
        p[n] = ((2 * n + 1) * (u * p[n - 1]) - (n + 1) * p[n - 2]) / n
        t[n] = (n + 1) * u * p[n] - (n + 2) * p[n - 1]
    return p, t


def S1_S2(
    k0,
    u,
    r_core,
    n_core,
    r_shell=None,
    n_shell=1,
    mu_core=1,
    mu_shell=1,
    n_env=1,
    mu_env=1,
    n_max="auto",
):
    k = k0 * n_env
    
    if r_shell is None:
        r_shell = r_core

    if len(np.shape(k)) == 0:
        k = np.array([k])
    if len(np.shape(k)) == 1:
        k = k[None, :]

    if n_max == "auto":
        # Wiscombe criterion for farfield
        ka = r_shell * k
        n_max = int(np.max(np.round(2 + ka + 4.05 * (ka ** (1 / 3)))))

    n = np.arange(1, n_max + 1)[:, None]

    a, b = core_shell_ab(
        k0=k0,
        r_core=r_core,
        n_core=n_core,
        r_shell=r_shell,
        n_shell=n_shell,
        mu_core=mu_core,
        mu_shell=mu_shell,
        n_env=n_env,
        mu_env=mu_env,
        n_max=n_max,
    )

    pi_n, tau_n = pi_tau(u, n_max)
    n2 = (2 * n + 1) / (n * (n + 1))
    pi_n = (pi_n[:, None] * n2)
    tau_n = (tau_n[:, None] * n2)
    S1 = np.sum(a * np.conjugate(pi_n), axis=0) + np.sum(
        b * np.conjugate(tau_n), axis=0
    )
    S2 = np.sum(a * np.conjugate(tau_n), axis=0) + np.sum(
        b * np.conjugate(pi_n), axis=0
    )

    return S1, S2


def angular(
    k0,
    r_core,
    n_core,
    r_shell=None,
    n_shell=1,
    mu_core=1,
    mu_shell=1,
    n_env=1,
    mu_env=1,
    n_max="auto",
    angular_range=[0, np.pi],
    angular_steps=180,
):
    k = k0 * n_env
    
    if n_env != 1.0:
        warnings.warn("tested only for n_env=1 !!")

    if r_shell is None:
        r_shell = r_core

    if len(np.shape(k)) == 0:
        k = np.array([k])
    if len(np.shape(k)) == 1:
        k = k[None, :]

    theta = np.linspace(*angular_range, angular_steps)
    SL = np.zeros((k.shape[1], angular_steps))
    SR = np.zeros((k.shape[1], angular_steps))
    SU = np.zeros((k.shape[1], angular_steps))
    
    # TODO !! This could be vectorized !!
    for j in range(angular_steps):
        u = np.cos(theta[j])
        S1, S2 = S1_S2(
            k0,
            u,
            r_core,
            n_core,
            r_shell,
            n_shell,
            mu_core,
            mu_shell,
            n_env,
            mu_env,
            n_max,
        )
        SL[:, j] = (np.conjugate(S1) * S1).real
        SR[:, j] = (np.conjugate(S2) * S2).real
        
        SU[:, j] = (SR[:, j] + SL[:, j]) / 2
    return theta, SL, SR, SU



def Q_scat_differential(
    k0,
    r_core,
    n_core,
    r_shell=None,
    n_shell=1,
    mu_core=1,
    mu_shell=1,
    n_env=1,
    mu_env=1,
    n_max="auto",
    angular_range=[0, np.pi],
    angular_steps=180,
):
    k = k0 * n_env
    
    if r_shell is None:
        r_shell = r_core
    
    theta, SL, SR, SU = angular(
    k0,
    r_core,
    n_core,
    r_shell,
    n_shell,
    mu_core=mu_core,
    mu_shell=mu_shell,
    n_env=n_env,
    mu_env=mu_env,
    n_max=n_max,
    angular_range=angular_range,
    angular_steps=angular_steps,
)
        
    return dict(qsca = (2 * SU * 2 / (k[:, None] ** 2 * r_shell**2)).mean(axis=1))

