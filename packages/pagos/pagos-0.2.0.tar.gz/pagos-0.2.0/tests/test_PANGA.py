# This is redundant when using pip-installed build of pagos, but necessary for
# testing purposes as we cannot upload every test version of pagos to the PyPI
import sys
sys.path.insert(0, 'C:/Users/scopi/source/repos/PAGOS/src/')

from pagos import Q, gas as pgas, modelling as pmod, builtin_models as pbim, plotting as pplt
import numpy as np
import pandas as pd

# data import and preparation
gases_used = ['Ne', 'Ar', 'Kr', 'Xe']
desired_columns_dict = {c:[] for c in gases_used + ['p', 'Sample Name']}#, 'S']}
pangadata_raw = pd.read_csv('C:/Users/scopi/source/repos/PAGOS/tests/Test Data/Complete_Input_Data_Samples_Belgium.CSV', sep=',')
pangadata_qs = pd.DataFrame(desired_columns_dict)
for i, r in pangadata_raw.iterrows():
    row_to_append = desired_columns_dict
    row_to_append['Sample Name'] = r['Sample']
    #row_to_append['S'] = Q(r['S [g/kg]'], 'permille')
    row_to_append['p'] = Q(0.997593, 'atm')    # explicit assumption of atmospheric equilibration pressure
    for g in gases_used:
        quantity_for_this_gas = Q(r[g], 'cc/g', r['err ' + g])
        row_to_append[g] = quantity_for_this_gas
    pangadata_qs.loc[i] = row_to_append.values()

print(pangadata_qs)

# plotting
pplt.make_plots(pangadata_qs, gases_used, 'Sample Name', title='Raw Test Data from PANGA')

# unfractionated excess air (UA) model
@pmod.gas_exchange_model(din=('degC', 'permille', 'atm', 'cc/g'), dout='cc/g')
def ua_model(gas, T, S, p, A):
    z = pgas.abn(gas)
    Ceq = pgas.calc_Ceq(gas, T, S, p, 'cc/g')
    return Ceq + A * z

# closed-system equilibrium (CE) model
@pmod.gas_exchange_model(din=('degC', 'permille', 'atm', 'cc/g', ''), dout='cc/g')
def ce_model(gas, T, S, p, A, F):
    z = pgas.abn(gas)
    Ceq = pgas.calc_Ceq(gas, T, S, p, 'cc/g')
    return Ceq + (1 - F)*A*z/(1 + F*A*z/Ceq)

# fitting UA model to data
fit = pmod.fitmodel(ua_model, pangadata_qs, ['T', 'S', 'A'],
                                            [Q(10, 'degC'), Q(1, 'permille'), Q(0.01,'cc/g')],
                                            gases_used,
                                            constraints={'S':(0, 100), 'T':(-100, 100)},
                                            tqdm_bar=True)
"""
# fitting CE model to data
fitCE = pmod.fitmodel(ce_model, pangadata_qs, ['A', 'F', 'T'],
                                              [Q(0.01, 'cc/g'), Q(0.5, None), Q(2, 'degC')],
                                              gases_used,
                                              tqdm_bar=True)"""

#plotting UA model results
pplt.make_plots(fit, ['A', 'S', 'T'], 'Sample Name', title='Parameters Fitted from Raw Test Data from Panga')
fit.to_csv('C:/Users/scopi/source/repos/PAGOS/tests/Test Data/PANGA Belgium samples fit.csv')
"""
# plotting CE model results
pplt.make_plots(fitCE, ['A', 'F', 'T'], 'Sample Name', title='Parameters Fitted (CE) from Raw Test Data from Panga')
fitCE.to_csv('C:/Users/scopi/source/repos/PAGOS/tests/Test Data/PANGA Belgium samples fit (CE).csv')"""