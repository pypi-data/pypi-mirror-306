"""
Built-in gas exchange models for PAGOS.
"""
from pint import Quantity
from collections.abc import Iterable
from pagos.modelling import gas_exchange_model
from pagos.gas import abn, ice, calc_Ceq, calc_dCeq_dT

@gas_exchange_model(din=('degC', 'permille', 'atm', 'dimensionless', 'cc/g'), dout='cc/g')
def ua_tim_r_taylor(gas:str|Iterable[str], T_r:float|Quantity, S:float|Quantity, p:float|Quantity, R:float|Quantity, A:float|Quantity) -> Quantity|Iterable[Quantity]:
    """Unfractionated excess air injection before freezing, then fractionation of gases upon freezing. Taylor
    expansion of concentration equation with fractionation during freezing yields:
    * C = [1 - R·(κ-1)] · [Cₑ(T_r, S, p) + Aχ].
        * R = small remaining ice fraction after melting
        * κ = ice fractionation coefficient of the given gas
        * Cₑ(T_r, S, p) = equilibrium concentration at water recharge temperature T_r, salinity S and air pressure p
        * A = excess air in same units as Cₑ
        * χ = atmospheric abundance of given gas
    See Chiara Hubner's Master Thesis (2024) for more info.

    :param gas: Gas(es) whose concentration should be calculated
    :type gas: str | Iterable[str]
    :param T_r: Recharge temperature of the water
    :type T_r: float | Quantity
    :param S: In-situ salinity of the water
    :type S: float | Quantity
    :param p: Air pressure over the water during recharge
    :type p: float | Quantity
    :param R: Remaining ice fraction after melting
    :type R: float | Quantity
    :param A: Excess air
    :type A: float | Quantity
    :return: Concentration of gas(es) calculated with the model
    :rtype: Quantity | Iterable[Quantity]
    """
    chi = abn(gas)
    kappa = ice(gas)
    Ceq = calc_Ceq(gas, T_r, S, p, 'cc/g')
    # C calculations
    C = (1 - R * (kappa - 1)) * (Ceq + A*chi)
    return C


@gas_exchange_model(din=('degC', 'permille', 'atm', 'dimensionless', 'cc/g'), dout='cc/g')
def ua_tim_rd_taylor(gas:str|Iterable[str], T_r:float|Quantity, S:float|Quantity, p:float|Quantity, R:float|Quantity, A:float|Quantity) -> Quantity|Iterable[Quantity]:
    """Unfractionated excess air injection before freezing, then fractionation of gases upon freezing. Taylor
    expansion of concentration equation with fractionation during freezing AND melting yields:
    * C = [1 - R·(κ²-1)] · [Cₑ(T_r, S, p) + Aχ].
        * R = small remaining ice fraction after melting
        * κ = ice fractionation coefficient of the given gas
        * Cₑ(T_r, S, p) = equilibrium concentration at water recharge temperature T_r, salinity S and air pressure p.
        * A = excess air in same units as Cₑ
        * χ = atmospheric abundance of given gas
    See Chiara Hubner's Master Thesis (2024) for more info.

    :param gas: Gas(es) whose concentration should be calculated.
    :type gas: str | Iterable[str]
    :param T_r: Recharge temperature of the water.
    :type T_r: float | Quantity
    :param S: In-situ salinity of the water.
    :type S: float | Quantity
    :param p: Air pressure over the water during recharge.
    :type p: float | Quantity
    :param R: Remaining ice fraction after melting.
    :type R: float | Quantity
    :param A: Excess air.
    :type A: float | Quantity
    :return: Concentration of gas(es) calculated with the model.
    :rtype: Quantity | Iterable[Quantity]
    """
    chi = abn(gas)
    kappa = ice(gas)
    Ceq = calc_Ceq(gas, T_r, S, p, 'cc/g')
    # C calculations
    C = (1 - R * (kappa**2 - 1)) * (Ceq + A*chi)
    return C


@gas_exchange_model(din=('degC', 'permille', 'atm', 'cc/g', 'dimensionless'), dout='cc/g')
def mr_fmb_m_nd(gas:str|Iterable[str], T_r:float|Quantity, S:float|Quantity, p:float|Quantity, zeta:float|Quantity, omega:float|Quantity) -> Quantity|Iterable[Quantity]:
    """Steady-state mixed reactor including a full mass balance and no diffusion. Equation reads:
    * C = 1/[1 + ω·(κ-1)] · [Cₑ(T_r, S, p) + ζχ]
        * ω = net freeze-to-flush rates ratio
        * κ = ice fractionation coefficient of the given gas
        * Cₑ(T_r, S, p) = equilibrium concentration at water recharge temperature T_r, salinity S and air pressure p.
        * ζ = net diffusion + excess air parameter
        * χ = atmospheric abundance of given gas
    See Chiara Hubner's Master Thesis (2024) for more info

    :param gas: Gas(es) whose concentration should be calculated.
    :type gas: str | Iterable[str]
    :param T_r: Recharge temperature of the water.
    :type T_r: float | Quantity
    :param S: In-situ salinity of the water.
    :type S: float | Quantity
    :param p: Air pressure over the water during recharge.
    :type p: float | Quantity
    :param zeta: Net diffusion + excess air parameter.
    :type zeta: float | Quantity
    :param omega: Net freeze-to-flush rates ratio.
    :type omega: float | Quantity
    :return: Concentration of gas(es) calculated with the model.
    :rtype: Quantity | Iterable[Quantity]
    """
    chi = abn(gas)
    kappa = ice(gas)
    Ceq = calc_Ceq(gas, T_r, S, p, 'cc/g')
    # C calculation
    C = 1 / (1 + omega*(kappa - 1)) * (Ceq + zeta * chi)
    return C

@gas_exchange_model(din=('degC', 'permille', 'atm', 'cc/g', 'dimensionless', 'degC'), dout='cc/g')
def mr_fmb_m_nd_qss_simple(gas:str|Iterable[str], T:float|Quantity, S:float|Quantity, p:float|Quantity, zeta:float|Quantity, omega:float|Quantity, T_r:float|Quantity) -> Quantity|Iterable[Quantity]:
    """Quasi-steady-state mixed reactor including a full mass balance and no diffusion, and a temperature
    differential simplification. Equation reads:
    * C = 1/[1 + ω·(κ-1) + q·Cₑ'(T, S, p)/Cₑ(T, S, p)] · [Cₑ(T_r, S, p) + ζχ]
        * ω = net freeze-to-flush rates ratio
        * κ = ice fractionation coefficient of the given gas
        * Cₑ(T, S, p) = equilibrium concentration at in-situ temperature T, salinity S and air pressure p
        * Cₑ' = dCₑ/dT
        * Cₑ(T_r, S, p) = equilibrium concentration at water recharge temperature T_r, salinity S and air pressure p
        * q = T - T_r
        * ζ = net diffusion + excess air parameter
        * χ = atmospheric abundance of given gas
    See Chiara Hubner's Master Thesis (2024) for more info

    :param gas: Gas(es) whose concentration should be calculated.
    :type gas: str | Iterable[str]
    :param T: In-situ temperature of the water.
    :type T: float | Quantity
    :param S: In-situ salinity of the water.
    :type S: float | Quantity
    :param p: Air pressure over the water during recharge.
    :type p: float | Quantity
    :param zeta: Net diffusion + excess air parameter.
    :type zeta: float | Quantity
    :param omega: Net freeze-to-flush rates ratio.
    :type omega: float | Quantity
    :param T_r: Recharge temperature of the water.
    :type T_r: float | Quantity
    :return: Concentration of gas(es) calculated with the model.
    :rtype: Quantity | Iterable[Quantity]
    """
    chi = abn(gas)
    kappa = ice(gas)
    q = T-T_r
    Ceq_T = calc_Ceq(gas, T, S, p, 'cc/g')
    dCeq_T_dT = calc_dCeq_dT(gas, T, S, p, 'cc/g/K')
    invpref = 1 + (kappa-1)*omega + q*dCeq_T_dT/Ceq_T
    Ceq_T_r = calc_Ceq(gas, T_r, S, p, 'cc/g')
    # C calculation
    C = 1/invpref * (Ceq_T_r + zeta*chi)
    return C