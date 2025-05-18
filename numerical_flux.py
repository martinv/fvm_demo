import math
import numpy as np


# Mach number interpolation polynomials
def m1_minus(ma: float) -> float:
    """Interpolation polynomial for interface Mach number and pressure"""
    # return 0.5 * (ma - abs(ma))
    return 0.0 if ma > 0.0 else ma


def m1_plus(ma: float) -> float:
    """Interpolation polynomial for interface Mach number and pressure"""
    # return 0.5 * (ma + abs(ma))
    return ma if ma > 0.0 else 0.0


def m2_minus(ma: float) -> float:
    """Interpolation polynomial for interface Mach number and pressure"""
    abs_ma = abs(ma)
    if abs_ma <= 1.0:
        return -0.25 * (ma - 1.0) * (ma - 1.0)
    else:
        return 0.5 * (ma - abs_ma)


def m2_plus(ma: float) -> float:
    """Interpolation polynomial for interface Mach number and pressure"""
    abs_ma = abs(ma)
    if abs_ma <= 1.0:
        return 0.25 * (ma + 1.0) * (ma + 1.0)
    else:
        return 0.5 * (ma + abs_ma)


def p3_minus(ma: float) -> float:
    """Interpolation polynomial for interface Mach number and pressure"""
    if abs(ma) <= 1.0:
        return -m2_minus(ma) * (2.0 + ma)
    else:
        return m1_minus(ma) / ma


def p3_plus(Ma: float) -> float:
    """Interpolation polynomial for interface Mach number and pressure"""
    if abs(Ma) <= 1.0:
        return m2_plus(Ma) * (2.0 - Ma)
    else:
        return m1_plus(Ma) / Ma


def AUSM_flux(u_L: np.array, u_R: np.array, normal: np.array) -> np.array:
    """Riemann solver"""
    gamma = 1.4

    # LEFT STATE
    # pressure
    p_L = (gamma - 1) * (u_L[3] - 0.5 * (u_L[1] * u_L[1] + u_L[2] * u_L[2]) / u_L[0])
    # local speed of sound
    a_L = math.sqrt(gamma * p_L / u_L[0])
    # normal speed
    v_L_n = (u_L[1] * normal[0] + u_L[2] * normal[1]) / u_L[0]
    # normal 'Mach number'
    M_L = v_L_n / a_L

    # RIGHT STATE
    # pressure
    p_R = (gamma - 1) * (u_R[3] - 0.5 * (u_R[1] * u_R[1] + u_R[2] * u_R[2]) / u_R[0])
    # local speed of sound
    a_R = math.sqrt(gamma * p_R / u_R[0])
    # normal speed
    v_R_n = (u_R[1] * normal[0] + u_R[2] * normal[1]) / u_R[0]
    # normal 'Mach number'
    M_R = v_R_n / a_R

    # interpolated Mach number and pressure at cell interface
    M_half = m2_plus(M_L) + m2_minus(M_R)
    p_half = p_L * p3_plus(M_L) + p_R * p3_minus(M_R)

    # Upwinding for convective flux
    f_p = np.array([0, p_half * normal[0], p_half * normal[1], 0])
    if M_half >= 0.0:
        f_c_L = np.array(
            [u_L[0] * a_L, u_L[1] * a_L, u_L[2] * a_L, (u_L[3] + p_L) * a_L]
        )
        return M_half * f_c_L + f_p
    else:
        f_c_R = np.array(
            [u_R[0] * a_R, u_R[1] * a_R, u_R[2] * a_R, (u_R[3] + p_R) * a_R]
        )
        return M_half * f_c_R + f_p
