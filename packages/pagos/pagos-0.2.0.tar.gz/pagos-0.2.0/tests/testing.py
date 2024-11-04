#%%
import sys
sys.path.insert(0, 'C:/Users/scopi/source/repos/VACAO_Stan_Chiara/src/')
from pagos import Q
from pagos import fitmodel
from pagos.builtin_models import ua_tim_r_taylor, ua_tim_rd_taylor, mr_fmb_m_nd, mr_fmb_m_nd_qss_simple
from pagos.plotting import make_plots
from pagos.modelling import forward_model
import pandas as pd
import numpy as np

#fakedata_params = pd.read_csv('Test Data/Fake Data.CSV', sep=',')
#fakedata_params.to_pickle('Test Data/Fake Data Params.pkl')
fakedata_params = pd.read_pickle('tests/Test Data/Fake Data Params.pkl')
Ts = fakedata_params['Recharge temp (deg C)'].to_list()
Terrs = fakedata_params['err RTemp'].to_list()
As = fakedata_params['Excess air (e-4 cm3/g)'].to_list()
Aerrs = fakedata_params['err EA'].to_list()
Rs = fakedata_params['Ice fraction'].to_list()
Rerrs = fakedata_params['err IF'].to_list()
Ss = fakedata_params['Salinity (PSU)'].to_list()
Serrs = fakedata_params['err Sal'].to_list()
ps = fakedata_params['Pressure (atm)'].to_list()
perrs = fakedata_params['err Prs'].to_list()

"""# random noise added to set data
for arr in [Ts, As, Rs, Ss, ps]:
    for i in range(len(arr)):
        arr[i] = arr[i] * (1 + np.random.normal(0, 0.2))"""

Tqs = [Q(Ts[i], 'degC', Terrs[i]) for i in range(len(Ts))]
Aqs = [Q(As[i]*1e-4, 'cc/g', Aerrs[i]*1e-4) for i in range(len(As))]
Rqs = [Q(Rs[i], 'dimensionless', Rerrs[i]) for i in range(len(Rs))]
Sqs = [Q(Ss[i], 'permille', Serrs[i]) for i in range(len(Ss))]
pqs = [Q(ps[i], 'atm', perrs[i]) for i in range(len(ps))]

for q in zip([Tqs, Aqs, Rqs, Sqs, pqs], ['Rech. temp. qu.', 'Exc. air qu.', 'Ice frac. qu.', 'Sal. qu.', 'prs. qu.']):
    fakedata_params[q[1]] = q[0]
# %%
#fakedata_concs = forward_model(ua_tim_r_taylor, fakedata_params, noblegases, paramlabels, fitted_only=False)
#fakedata_concs.to_pickle('tests/Test Data/Fake Modelled Concentrations.pkl')
fakedata_concs = pd.read_pickle('tests/Test Data/Fake Modelled Concentrations.pkl')
# %%
noblegases = ['He', 'Ne', 'Ar', 'Kr', 'Xe']
paramlabels = {'T_r':'Rech. temp. qu.', 'A':'Exc. air qu.', 'R':'Ice frac. qu.', 'S':'Sal. qu.', 'p':'prs. qu.'}
tracerlabels = {g:'modelled ' + g for g in noblegases}
tracerlabels['S'] = 'Sal. qu.'
tracerlabels['p'] = 'prs. qu.'
fakedata_fit = fitmodel(ua_tim_r_taylor,
                        fakedata_concs,
                        ['T_r', 'A', 'R'],
                        [Q(1, 'degC'), Q(1e-4, 'cc/g'), Q(1e-2, 'dimensionless')],
                        noblegases,
                        tracerlabels,
                        constraints={'A':(0, np.inf), 'R':(0, 1)},
                        tqdm_bar=True,
                        fitted_only=False)
# %%
make_plots(fakedata_fit, ['T_r', 'A', 'R'], 'Label')
make_plots(fakedata_params, ['Rech. temp. qu.', 'Exc. air qu.', 'Ice frac. qu.'], 'Label')
make_plots(fakedata_concs, ['modelled He', 'modelled Ne', 'modelled Ar', 'modelled Kr', 'modelled Xe'], 'Label')
# %%