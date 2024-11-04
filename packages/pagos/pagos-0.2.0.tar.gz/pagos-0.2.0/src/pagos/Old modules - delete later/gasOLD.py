"""
Functions for calculating the properties of various gases.
"""
#TODO make a document in the README or something explaining all conventions we assume
# for example, that for us, STP = 0 degC 1 atm instead of 20 degC 1 atm.
from pint import Quantity
from pint import Unit
from uncertainties import unumpy as unp
from collections.abc import Iterable

from pagos._pretty_gas_wrappers import *
from pagos.core import u as _u
import pagos.core as _core
import pagos.constants as _con
from pagos import water as _water

@oneormoregases # TODO should we really have this @ here?? For instance, the schmidt number calculation can take in multiple gases, but processes each one individually - removing the need for this...
def hasgasprop(gas:str|Iterable[str], condition:str|list[str]) -> bool|list[bool]: #want to use union type but needs python 3.10 or newer for specification str|list
    """
    Returns True if the gas fulfils the condition specified by arguments condition and specific.

    :param str condition:
        Condition to be checked. Need not have an argument, e.g. condition='isstabletransient' takes no argument and
        only checks if the gas is a stable transient gas (e.g. SF6 or CFC12).
        possible conditions are 'spcis' (needs the species in specific), 'isnoble', 'isng', 'isstabletransient', 'isst'
    :return bool:
        Truth value of the condition.
    """
    if condition in ['isnoble', 'isng']:
        if gas in _con.NOBLEGASES:
            return True
        else:
            return False
    if condition in ['isstabletransient', 'isst']:
        if gas in _con.STABLETRANSIENTGASES:
            return True
        else:
            return False
    else: 
        raise ValueError("%s is not a valid condition." % (condition))
    
"""
GETTERS
"""
@oneormoregases
def jkc(gas:str|Iterable[str]) -> dict[float]|Iterable[dict[float]]:
    """Get a dictionary of the Jenkins 2019 solubility equation coefficients of the gas:
    {A1, A2, A3, A4, B1, B2, B3, C1}.

    :param gas: Gas whose Jenkins coefficients are to be returned.
    :type gas: str | Iterable[str]
    :raises AttributeError: If the given gas is not noble.
    :return: Dictionary of gas's Jenkins coefficients.
    :rtype: dict[float]|Iterable[dict[float]]
    """    
    if hasgasprop(gas, 'isnoble'):
        return _con.NG_JENKINS_19_COEFFS[gas]
    else:
        raise AttributeError("Only noble gases have the attribute jkc. This gas (%s) does not have the property "
                                "\"noble\"." % (gas))

@oneormoregases
def wkc(gas:str|Iterable[str]) -> dict[float]|Iterable[dict[float]]:
    """Get a dictionary of the Wanninkhof 1992 Schmidt number equation coefficients of the
    gas: {A, B, C, D}.
    NOTE: for xenon, the W92 formula has been estimated by fitting the Eyring diffusivity
    curve from Jähne et al. 1987 to the W92 formula and using the coefficients of best fit.

    :param gas: Gas whose Wanninkhof coefficients are to be returned.
    :type gas: str | Iterable[str]
    :return: Dictionary of gas's Wanninkhof coefficients.
    :rtype: dict[float]|Iterable[dict[float]]
    """
    return _con.WANNINKHOF_92_COEFFS[gas] #TODO implement exception for gases without Wanningkof coeffs

@oneormoregases
def erc(gas:str|Iterable[str]) -> dict[float]|Iterable[dict[float]]:
    """Get a dictionary of the Eyring 1936 coeffs {A, Ea} for the diffusivity. Noble gas
    coefficients from Jähne 1987, except argon, interpolated from Wanninkhof 1992. N2 is
    from Ferrel and Himmelblau 1967.

    :param gas: Gas whose Eyring coefficients are to be returned.
    :type gas: str | Iterable[str]
    :return: Dictionary of gas's Eyring coefficients.
    :rtype: dict[float]|Iterable[dict[float]]
    """    
    return _con.EYRING_36_COEFFS[gas] #TODO implement exception for gases without Eyring coeffs

@oneormoregases
def mv(gas:str|Iterable[str]) -> float|Iterable[float]:
    """Get the molar volume of the given gas at STP in cm3/mol.

    :param gas: Gas whose molar volume is to be returned.
    :type gas: str | Iterable[str]
    :return: STP molar volume of given gas in cm3/mol.
    :rtype: float|Iterable[float]
    """    
    return _con.MOLAR_VOLUMES[gas] #TODO implement exception for gases without molar volumes

@oneormoregases
def wwc(gas:str|Iterable[str]) -> dict[float]|Iterable[dict[float]]:
    """Get a dictionary of the Warner and Weiss 1985 equation coefficients of the gas:
    {a1, a2, a3, a4, b1, b2, b3}.

    :param gas: Gas whose Warner/Weiss coefficients are to be returned.
    :type gas: str | Iterable[str]
    :return: Dictionary of gas's Warner/Weiss coefficients.
    :rtype: dict[float]|Iterable[dict[float]]
    """    
    return _con.CFC_WARNERWEISS_85_COEFFS[gas] #TODO implement exception for gases without warner/weiss coefficients

@oneormoregases
def abn(gas:str|Iterable[str]) -> float|Iterable[float]:
    """Get the atmospheric abundance of the given gas.

    :param gas: Gas whose abundance is to be returned.
    :type gas: str | Iterable[str]
    :return: Atmospheric abundance of given gas.
    :rtype: float|Iterable[float]
    """    
    return _con.ABUNDANCES[gas] #TODO implement exception for gases without abundances

@oneormoregases
def blc(gas:str|Iterable[str]) -> dict[float]|Iterable[dict[float]]:
    """Get a dictionary of the Bullister 2002 equation coefficients of the gas:
    {a1, a2, a3, b1, b2, b3}.

    :param gas: Gas whose Bullister coefficients are to be returned.
    :type gas: str | Iterable[str]
    :return: Dictionary of gas's Bullister coefficients.
    :rtype: dict[float]|Iterable[dict[float]]
    """    
    return _con.SF6_BULLISTER_02_COEFFS[gas] #TODO implement exception for gases without Bullister coeffs.

@oneormoregases
def hec(gas:str|Iterable[str]) -> dict[float]|Iterable[dict[float]]:
    """Get a dictionary of the Hamme and Emerson 2004 equation coefficients of the gas:
    {A0, A1, A2, A3, B0, B1, B2}.

    :param gas: Gas whose Hamme/Emerson coefficients are to be returned
    :type gas: str | Iterable[str]
    :return: Dictionary of gas's Hamme/Emerson coefficients.
    :rtype: dict[float]|Iterable[dict[float]]
    """    
    return _con.ArNeN2_HAMMEEMERSON_04[gas] #TODO implement exception for gases without Hamme/Emerson coeffs.

@oneormoregases
def ice(gas:str|Iterable[str]) -> float|Iterable[float]:
    """
    Get the ice fractionation coefficient of the given gas from Loose et al. 2020.

    :param gas: Gas whose ice fractionation coefficient is to be returned.
    :type gas: str | Iterable[str]
    :return: Ice fractionation coefficient of given gas.
    :rtype: float|Iterable[float]
    """
    return _con.ICE_FRACTIONATION_COEFFS[gas] #TODO implement exception for gases without ice fractionation coeffs.


"""
PROPERTY CALCULATIONS
"""
@oneormoregases
@magnitudeonlypossible
def calc_Sc(gas:str|Iterable[str], T:Quantity, S:Quantity, method:str='auto', **kwargs) -> float|Iterable[float]:
    """Calculates the Schmidt number Sc of given gas in seawater. There are three methods
    of calculation:
        - 'HE17'
            - Hamme and Emerson 2017, combination of various methods.
            - Based off of Roberta Hamme's Matlab scripts, available at
              https://oceangaseslab.uvic.ca/download.html.
        - 'W92'
            - Wanninkhof 1992
            - Threshold between fresh and salty water chosen to be S = 5 g/kg, but isn't
              well defined, so this method is best used only for waters with salinities
              around 34 g/kg.
        - 'auto':
            - Default to HE17
            - Transient stable gases (CFCs and SF6) use W92 because required data for HE17
              with these gases are not available.

    :param gas: Gas for which Sc should be calculated.
    :type gas: str | Iterable[str]
    :param T: Temperature.
    :type T: Quantity
    :param S: Salinity.
    :type S: Quantity
    :param method: Specification of which method of Sc-calculation to use, defaults to 'auto'
    :type method: str, optional
    :raises ValueError: If S < 0.
    :raises ValueError: If method is not 'auto', 'HE17' or 'W92'.
    :return: Schmidt number Sc of given gas.
    :rtype: float|Iterable[float]
    """

    if method == 'auto':
        if hasgasprop(gas, 'isst'):
            method = 'W92'
        else:
            method = 'HE17'
            
    # convert temperature to K, and subtract 273.15 K instead of converting to degC (because celsius is multiplicatively ambiguous)
    T = _core.sto(T, 'K')
    T_C = T - _con.TPW

    # Wanninkhof 1992 method
    if method == 'W92':
        # salt factor for if the water is salty or not. Threshold is low, therefore this method is only recommended
        # for waters with salinity approx. equal to 34 g/kg.
        if S > 5:
            saltfactor = (1.052 + 1.3e-3*_u('K^-1')*T_C + 5e-6*_u('K^-2')*T_C**2 - 5e-7*_u('K^-3')*T_C**3)/0.94
        elif 0 <= S <= 5:
            saltfactor = 1
        else:
            raise ValueError("S must be a number >= 0.")
        #changed it: instead of going to the list, it uses the properties
        (A, B, C, D) = (wkc(gas)[s] for s in ["A", "B", "C", "D"])
        Sc = saltfactor*(A - B*T_C + C*T_C**2 - D*T_C**3)
    # Hamme & Emerson 2017 method
    if method == 'HE17':
        # Eyring diffusivity calculation
        (A_coeff, activation_energy)  = (erc(gas)[s] for s in ["A", "Ea"])
        D0 = A_coeff * _core.safeexp(-activation_energy/(_con.MGC * T))
        # Saltwater correction used by R. Hamme in her Matlab script (https://oceangaseslab.uvic.ca/download.html)
        D = D0 * (1 - 0.049 * S / (35.5*_u('permille'))) #PSS78 as Salinity
        # Kinematic viscosity calculation
        nu_sw = _water.calc_kinvisc(T, S)
        Sc = _core.sto(nu_sw / D, 'dimensionless')
    else:
        raise ValueError("%s is not a valid method. Try 'auto', 'HE17' or 'W92'" % (method))
    return Sc


def calc_Cstar(gas:str, T:Quantity, S:Quantity) -> Quantity:
    """Calculate the moist atmospheric equilibrium concentration C* of a given gas at
    temperature T and salinity S. C* = waterside gas concentration when the total water
    vapour-saturated atmospheric pressure is 1 atm (see Solubility of Gases in Water, W.
    Aeschbach-Hertig, Jan. 2004).

    :param gas: Gas for which C* should be calculated.
    :type gas: str
    :param T: Temperature.
    :type T: Quantity
    :param S: Salinity
    :type S: Quantity
    :return: Moist atmospheric equilibrium concentration C* of the given gas.
    :rtype: Quantity
    """
    # convert temperature to K, and subtract 273.15 K instead of converting to degC (because celsius is multiplicatively ambiguous)
    T = _core.sto(T, 'K')
    T_C = T - _con.TPW

    # calculation of C*
    if hasgasprop(gas, 'isnoble'):
        A1, A2, A3, A4, B1, B2, B3, C1 = jkc(gas).values() #needs S in PSS78
        # C*, concentration calculated from Jenkins et al. 2019
        # units mol/kg
        Cstar = _core.safeexp(A1 + A2*(100*_u('K')/T) + A3*unp.log(T/(100*_u('K'))) + A4*(T/(100*_u('K')))
                        + S*(B1 + B2 * T/(100*_u('K')) + B3 * (T/(100*_u('K')))**2)
                        + C1*S**2) * _u('mol/kg')
    elif gas in ['CFC11', 'CFC12']:
        a1, a2, a3, a4, b1, b2, b3 = wwc(gas).values() #needs S in parts per thousand
        #TODO adopt for absolute salinity??
        # abundance
        ab = abn(gas)
        # C* = F*abundance, concentration calculated from Warner and Weiss 1985
        Cstar = _core.safeexp(a1 + a2*(100*_u('K')/T) + a3*unp.log(T/(100*_u('K'))) + a4*(T/(100*_u('K')))**2
                        + S*(b1 + b2*T/(100*_u('K')) + b3*(T/(100*_u('K')))**2)
                        ) * ab * _u('mol/kg')
    elif gas == 'SF6':
        a1, a2, a3, b1, b2, b3 = blc(gas).values() #don't know salinity unit
        # abundance
        ab = abn(gas)
        # C* = F*abundance, concentration calculated from Bullister et al. 2002
        Cstar = _core.safeexp(a1 + a2*(100*_u('K')/T) + a3*unp.log(T/(100*_u('K')))
                        + S*(b1 + b2*T/(100*_u('K')) + b3*(T/(100*_u('K')))**2)
                        ) * ab * _u('mol/kg')
    elif gas == 'N2':
        A0, A1, A2, A3, B0, B1, B2 = hec(gas).values() #PSS salinity
        # T_s, temperature expression used in the calculation of C*
        T_s = unp.log((298.15*_u('K') - T_C)/T)
        # C*, concentration calculated from Hamme and Emerson 2004. Multiplication by 10^-6 to have units of mol/kg
        Cstar = _core.safeexp(A0 + A1*T_s + A2*T_s**2 + A3*T_s**3 + S*(B0 + B1*T_s + B2*T_s**2)) * 1e-6 * _u('mol/kg')
    return Cstar


# TODO is Iterable[Quantity] here the best way, or should it specify that they have to be numpy arrays?
# TODO is instead a dict output the best choice for the multi-gas option? All other multi-gas functionalities in this program just spit out arrays... i.e., prioritise clarity or consistency? 
@oneormoregases
@defaultTSpunits
@magnitudeonlypossible # TODO I think this stacking of decorators might be causing slow fitting in lmfit. Perhaps define some underscored decorators that combine however many are necessary for each purpose?
def calc_Ceq(gas:str|Iterable[str], T:Quantity|float, S:Quantity|float, p:Quantity|float, Ceq_unit:str, **kwargs) -> Quantity|Iterable[Quantity]:
    """Calculate the waterside equilibrium concentration Ceq of a given gas at water
    temperature T, salinity S and airside pressure p.

    :param gas: Gas for which Ceq should be calculated.
    :type gas: str | Iterable[str]
    :param T: Temperature of the water.
    :type T: Quantity | float
    :param S: Salinity of the water.
    :type S: Quantity | float
    :param p: Pressure over the water.
    :type p: Quantity | float
    :param Ceq_unit: Units in which Ceq should be expressed.
    :type Ceq_unit: str
    :raises ValueError: If the units given in Ceq_unit are unimplemented.
    :return: Waterside equilibrium concentration Ceq of the given gas.
    :rtype: Quantity|Iterable[Quantity]
    """
    # convert temperature to K
    T = _core.sto(T, 'K')
    mvol = mv(gas)
    # vapour pressure over the water, calculated according to Dyck and Peschke 1995
    e_w = _water.calc_vappres(T)
    # density of the water
    rho = _water.calc_dens(T, S)

    # calculation of C*, the gas solubility/water-side concentration expressed in units of mol/kg
    Cstar = calc_Cstar(gas, T, S)
    # factor to account for pressure and using g instead of kg
    pref = (p - e_w) / (_con.PAT - e_w)
    # return equilibrium concentration with desired units
    # TODO reformulate this using CONTEXTS (see pint Github)
    if not type(Ceq_unit) == Unit:                  # create pint.Unit object from unit string argument
        Ceq_unit = _u.Unit(Ceq_unit) 
    if Ceq_unit.is_compatible_with('mol/g'):        # amount gas / mass water
        ret = pref * Cstar
    elif Ceq_unit.is_compatible_with('mol/cc'):     # amount gas / volume water
        ret =  pref * rho * Cstar
    elif Ceq_unit.is_compatible_with('cc/g'):       # volume gas / mass water
        ret = pref * mvol * Cstar
    else:                                       # TODO implement vol/amount, mass/vol and mass/amount
        raise ValueError("Invalid/unimplemented value for unit. Try something like \"mol/g\", \"mol/cc\" or \"cc/g\".")
    
    return _core.sto(ret, Ceq_unit)


@oneormoregases
@defaultTSpunits
@magnitudeonlypossible
def calc_dCeq_dT(gas:str, T:Quantity|Iterable[Quantity], S:Quantity|Iterable[Quantity], p:Quantity|Iterable[Quantity], dCeq_dT_unit:str, **kwargs) -> Quantity|Iterable[Quantity]|dict[Iterable[Quantity]]:
    """Calculate the temperature-derivative dCeq_dT of the waterside equilibrium
    concentration of a given gas at water temperature T, salinity S and airside pressure p.

    :param gas: Gas for which dCeq_dT should be calculated.
    :type gas: str
    :param T: Temperature of the water.
    :type T: Quantity | Iterable[Quantity]
    :param S: Salinity of the water.
    :type S: Quantity | Iterable[Quantity]
    :param p: Pressure over the water.
    :type p: Quantity | Iterable[Quantity]
    :param dCeq_dT_unit: Units in which dCeq_dT should be expressed.
    :type dCeq_dT_unit: str
    :raises ValueError: If the units given in dCeq_dT_unit are unimplemented.
    :return: Waterside equilibrium concentration temperature derivative dCeq_dT of the given gas.
    :rtype: Quantity|Iterable[Quantity]|dict[Iterable[Quantity]]
    """    
    # convert temperature to K, and subtract 273.15 K instead of converting to degC (because celsius is multiplicatively ambiguous)
    T = _core.sto(T, 'K')
    T_C = T - _con.TPW   
    mvol = mv(gas)
    # vapour pressure over the water, calculated according to Dyck and Peschke 1995
    e_w = _water.calc_vappres(T)
    # density of the water
    rho = _water.calc_dens(T, S)
    # factor to account for pressure and using g instead of kg
    pref = (p - e_w) / (_con.PAT - e_w)
    # calculation of C*, the gas solubility/water-side concentration expressed in units of mol/kg
    Cstar = calc_Cstar(gas, T, S)
    # calculation of d(C*)/dT at the given T, S, p
    # TODO why is numerical differentiation not okay here? i.e. dCstar_dT = _core.deriv(Cstar, T)
    if hasgasprop(gas, 'isnoble'):
        A1, A2, A3, A4, B1, B2, B3, C1 = jkc(gas).values() #needs S in PSS78
        dCstar_dT = (S*(B3*T/(5000*_u('K^2')) + B2/(100*_u('K'))) + A3/T - 100*A2*_u('K')/(T**2) + A4/(100*_u('K')))*Cstar
    elif gas in ['CFC11', 'CFC12']:
        a1, a2, a3, a4, b1, b2, b3 = wwc(gas).values() #needs S in parts per thousand
        #TODO adopt for absolute salinity??
        dCstar_dT = (S*(b3*T/(5000*_u('K^2')) + b2/(100*_u('K'))) + a3/T - 100*a2*_u('K')/(T**2) + a4*T/(5000*_u('K^2')))*Cstar
    elif gas == 'SF6':
        a1, a2, a3, b1, b2, b3 = blc(gas).values() #don't know salinity unit
        dCstar_dT = (S*(b3*T/(5000*_u('K^2')) + b2/(100*_u('K'))) + a3/T - 100*a2*_u('K')/(T**2))*Cstar
    elif gas == 'N2':
        A0, A1, A2, A3, B0, B1, B2 = hec(gas).values() #PSS salinity
        # T_s, temperature expression used in the calculation of C*
        T_s = unp.log((298.15*_u('K') - T_C)/T)
        # TODO check that this formula is correct
        dCstar_dT = Cstar * 25*_u('K')/((T-25*_u('K'))*T) * (A1 + S*B1 + 2*(A2 + S*B2)*T_s + 3*A3*T_s**2) * 1e-6

    #TODO check if this numerical differentiation is fine, or if we have to explicitly write analytic derivatves for rho and e_W
    drho_dT = _core.deriv(rho, T)
    de_w_dT = _core.deriv(e_w, T)
    dCeq_dT_molg = pref * dCstar_dT + (p - _con.PAT)/((e_w - _con.PAT)**2) * de_w_dT * Cstar
    # TODO ^ i think strictly this is mol/kg/K, not mol/g/K - rename?

    # TODO reformulate this using CONTEXTS? (see pint Github)
    if not type(dCeq_dT_unit) == Unit:                  # create pint.Unit object from unit string argument
        dCeq_dT_unit = _u.Unit(dCeq_dT_unit) 
    if dCeq_dT_unit.is_compatible_with('mol/g/K'):        # amount gas / mass water
        ret = dCeq_dT_molg
    elif dCeq_dT_unit.is_compatible_with('mol/cc/K'):     # amount gas / volume water
        ret = dCeq_dT_molg * rho + pref * Cstar * drho_dT
    elif dCeq_dT_unit.is_compatible_with('cc/g/K'):       # volume gas / mass water
        ret = dCeq_dT_molg * mvol
    else:                                       # TODO implement vol/amount, mass/vol and mass/amount
        raise ValueError("Invalid/unimplemented value for unit. Try something like \"mol/g/K\", \"mol/cc/K\" or \"cc/g/K\".")
    return _core.sto(ret, dCeq_dT_unit)