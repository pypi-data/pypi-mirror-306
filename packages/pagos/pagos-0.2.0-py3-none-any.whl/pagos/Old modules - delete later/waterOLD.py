"""
Functions for calculating the properties of water.
- `calc_dens()`: density
- `calc_vappres()`: vapour pressure
- `calc_kinvisc()`: kinematic viscosity
"""
from pint import Quantity
from collections.abc import Iterable

from pagos.core import u as _u
import pagos.core as _core
from pagos import constants as gcon


# TODO is Iterable[ufloat] here the best way, or should it specify that they have to be numpy arrays?
def calc_dens(T:Quantity|Iterable[Quantity], S:Quantity|Iterable[Quantity]) -> Quantity|Iterable[Quantity]:
    """Calculate density of seawater at a given temperature and salinity according to Gill 1982.

    :param T: Temperature.
    :type T: Quantity | Iterable[Quantity]
    :param S: Salinity.
    :type S: Quantity | Iterable[Quantity]
    :return: Density.
    :rtype: Quantity | Iterable[Quantity]
    """

    a0, a1, a2, a3, a4, a5, b0, b1, b2, b3, b4, c0, c1, c2, d0 = gcon.GILL_82_COEFFS.values()
    # convert temperature to K, and subtract 273.15 K instead of converting to degC (because celsius is multiplicatively ambiguous)
    T_C = _core.sto(T, 'K') - 273.15*_u.K

    rho0 = a0 + a1*T_C + a2*T_C**2 + a3*T_C**3 + a4*T_C**4 + a5*T_C**5
    ret = rho0 + S*(b0 + b1*T_C + b2*T_C**2 + b3*T_C**3 + b4*T_C**4) + \
          (S**(3/2))*(c0 + c1*T_C + c2*T_C**2) + \
          d0*S**2
    return ret


# TODO is Iterable[ufloat] here the best way, or should it specify that they have to be numpy arrays?
def calc_vappres(T:Quantity|Iterable[Quantity]) -> Quantity|Iterable[Quantity]:
    """Calculate vapour pressure over water at a given temperature, according to Dyck and
    Peschke 1995.

    :param T: Temperature.
    :type T: Quantity | Iterable[Quantity]
    :return: Vapour pressure.
    :rtype: Quantity | Iterable[Quantity]
    """

    # convert temperature to K, and subtract 273.15 K instead of converting to degC (because celsius is multiplicatively ambiguous)
    T_C = _core.sto(T, 'K') - 273.15*_u.K

    pv = 6.1078 * 10 ** ((7.567 * T_C) / (T_C + 239.7*_u.K)) * _u.mbar
    return pv


# TODO is Iterable[ufloat] here the best way, or should it specify that they have to be numpy arrays?
def calc_kinvisc(T:Quantity|Iterable[Quantity], S:Quantity|Iterable[Quantity]) -> Quantity|Iterable[Quantity]:
    """Calculate kinematic viscosity of seawater at a given temperature and salinity according
    to Sharqawy 2010.

    :param T: Temperature.
    :type T: Quantity | Iterable[Quantity]
    :param S: Salinity.
    :type S: Quantity | Iterable[Quantity]
    :return: Kinematic viscosity
    :rtype: Quantity | Iterable[Quantity]
    """
    # convert temperature to K, and subtract 273.15 K instead of converting to degC (because celsius is multiplicatively ambiguous)
    T_C = _core.sto(T, 'K') - 273.15*_u.K
    # Density of the water
    rho = calc_dens(T, S) 
    # Adapt salinity to reference composition salinity in kg/kg (Sharqawy 2010)
    S_R = 1.00472*_core.sto(S, 'kg/kg')
    # Viscosity calculated following Sharqawy 2010
    mu_fw = (4.2844e-5 + (1*_u('K^2'))/(0.157*(T_C + 64.993*_u('K'))**2 - 91.296*_u('K^2')))*_u('kg/m/s') #would need ITS-90 as temperature
    A = 1.541 + 0.01998*_u('K^-1') * T_C - 9.52e-5*_u('K^-2') * T_C ** 2
    B = 7.974 - 0.07561*_u('K^-1') * T_C + 4.724e-4*_u('K^-2') * T_C ** 2
    # saltwater dynamic viscosity
    mu_sw = mu_fw * (1 + A * S_R + B * S_R ** 2)
    # saltwater kinematic viscosity
    nu_sw = mu_sw / rho
    
    return nu_sw