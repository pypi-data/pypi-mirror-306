"""
Decorators wrapping functions used in `gas.py`, for pretty code.
"""

import numpy as np
from pagos.core import u as _u

def oneormoregases(func):
    """Wraps function with a gas argument so that an list of gases can be passed instead.

    :param func: Function to wrap.
    :type func: function
    """
    def wrapper_oomt(gas, *args, **kwargs):
        if type(gas) == str:
            return func(gas, *args, **kwargs)
        else:
            ret = np.array([func(g, *args, **kwargs) for g in gas], dtype=object) # TODO exception thrown if dtype argument not included: perhaps investigate this further?
            # if ret has structure like [Quantity(val1, unit), Quantity(val2, unit), Quantity(val3, unit), ...]
            # change to Quantity([val1, val2, val3, ...], unit), which makes further calculations easier later
            if [type(elt) for elt in ret] == [_u.Quantity for elt in ret]:  #\
                if len(set([elt.units for elt in ret])) == 1:               #/ -- these check for above-mentioned structure 
                    ret = _u.Quantity([elt.magnitude for elt in ret], ret[0].units)
            return ret
    return wrapper_oomt


def defaultTSpunits(func):
    """NOTE: this decorator should ONLY be used for functions with signature (gas, T, S,
    p, *args, **kwargs)!
    Wraps function with arguments T, S, p so that, if they are not provided with units
    (i.e. as Quantity objects), they are given units, either specified by a keyword
    argument TSp_units in the function call or set as °C, permille and atm by default.

    :param func: Function to wrap.
    :type func: function
    """
    def wrapper_dTSpu(gas, T, S, p, *args, **kwargs):
        # if all TSp arguments are of type Quantity
        if [type(q) == _u.Quantity for q in [T, S, p]] == [True, True, True]:
            return func(gas, T, S, p, *args, **kwargs)
        else:
            # check for kwarg TSp_units; act as if TSp_units=None was given if kwarg is not given
            if 'TSp_units' in kwargs.keys():
                TSp_u = kwargs['TSp_units']
            else:
                TSp_u = None
            # set default TSp units as degrees C, permille and atmospheres
            if TSp_u in [None, 'default']:
                TSp_u = ['degC', 'permille', 'atm']
            # return function of same structure but with Quantity inputs rather than non-Quantity inputs with TSp_units argument (or assumed default TSp_units=None)
            TSp_qs = []
            for i, q in enumerate([T, S, p]):
                # TODO make this None protection part of the core.Q() function, and replace this
                if q is not None:
                    TSp_qs.append(_u.Quantity(q, TSp_u[i]))
                else:
                    TSp_qs.append(None)
            return func(gas, TSp_qs[0], TSp_qs[1], TSp_qs[2], *args, **kwargs)
    return wrapper_dTSpu

# TODO I think this is now obsolete, perhaps we can delete get rid of this for speed?
def magnitudeonlypossible(func):
    """NOTE: this decorator should ONLY be used for functions that return Quantity type
    objects!
    Wraps a function that usually returns a Quantity object q, such that an optional
    keyword argument mag_only can be used in its call. If mag_only has value 1 or 2, it
    returns q.magnitude or q.magnitude.nominal_value, the latter for when q.magnitude is a
    ufloat object from the uncertainties package.

    :param func: Function to wrap.
    :type func: function
    """
    def wrapper_mop(*args, **kwargs):
        if 'mag_only' in kwargs.keys():
            if kwargs['mag_only'] == 1:
                # return magnitude, with uncertainty if present
                return func(*args, **kwargs).magnitude
            if kwargs['mag_only'] == 2:
                # return magnitude, nominal value only
                return func(*args, **kwargs).magnitude.nominal_value
        else:
            return func(*args, **kwargs)
    return wrapper_mop