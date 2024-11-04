# This is redundant when using pip-installed build of pagos, but necessary for
# testing purposes as we cannot upload every test version of pagos to the PyPI
import sys
sys.path.insert(0, 'C:/Users/scopi/source/repos/PAGOS/src/')

from pagos import Q, gas as pgas, modelling as pmod, builtin_models as pbim, plotting as pplt
import numpy as np
import pandas as pd

# data import and preparation
gases_used = ['Ne', 'Ar', 'Kr']
colorlist = ['#eaadc2' for _ in range(27)] + ['#d72243' for _ in range(70)] + ['#1dc8fb' for _ in range(34)] + ['#aeb9c6' for _ in range(14)] + ['#726cff' for _ in range(34)]
desired_columns_dict = {c:[] for c in gases_used + ['depth', 'T', 'S', 'p']}
HE_data_raw = pd.read_csv('C:/Users/scopi/source/repos/PAGOS/tests/Test Data/HE17 data.csv', sep=',')
HE_data_qs = pd.DataFrame(desired_columns_dict)
for i, r in HE_data_raw.iterrows():
    row_to_append = desired_columns_dict
    row_to_append['depth'] = r['depth']
    row_to_append['T'] = Q(r['ptmp'], 'degC')
    row_to_append['S'] = Q(r['CTDsal'], 'permille')
    row_to_append['p'] = Q(1, 'atm')    # explicit assumption of atmospheric equilibration pressure
    for g in gases_used:
        s = g + 'sat'
        quantity_for_this_gas = Q(r[s]/100, None)
        row_to_append[g] = quantity_for_this_gas
    HE_data_qs.loc[i] = row_to_append.values()

# plotting
pplt.make_plots(HE_data_qs, ['Ne', 'Ar', 'Kr'], 'depth', custom_colors=colorlist)

# HE17 model
@pmod.gas_exchange_model
def he17_model(gas, pres_term, temp_term, bub_term, T, S, p, **kwargs):
    Sc = pgas.calc_Sc(gas, T, S)
    chi = pgas.abn(gas)
    Ceq = pgas.calc_Ceq(gas, T, S, p, 'mol/m^3')
    dCeqdT = pgas.calc_dCeq_dT(gas, T, S, p, 'mol/m^3/K')

    gas_dependent_temp_term = -(Sc/660)**0.5 * dCeqdT / Ceq
    gas_dependent_bub_term = (Sc/660)**0.5 * chi/Ceq

    deltaC = pres_term + temp_term*gas_dependent_temp_term + bub_term*gas_dependent_bub_term
    return deltaC

# fitting HE17 model to data
fit = pmod.fitmodel(he17_model, HE_data_qs, ['pres_term', 'temp_term', 'bub_term'],
                    [Q(0, 'dimensionless'), Q(0, 'K'), Q(0, 'mol/m^3')], gases_used, tqdm_bar=True)

# plotting UA model results
pplt.make_plots(fit, ['pres_term', 'temp_term', 'bub_term'], 'depth', title='Parameters Fitted HE17 Data', custom_colors=colorlist)
fit.to_csv('C:/Users/scopi/source/repos/PAGOS/tests/Test Data/HE17 fit.csv')