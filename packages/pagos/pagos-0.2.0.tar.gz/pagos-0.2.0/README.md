# PAGOS
**P**ython **A**nalysis of **G**roundwater and **O**cean **S**amples_ (PAGOS) is a Python toolkit for creating and testing hydrological gas exchange models. Datasets from field campaigns containing data for a number of gas tracers can be used to optimise the parameters of gas exchange models, expressed as Python functions. These can be PAGOS' built-in models or user-defined.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PAGOS.

```bash
pip install pagos
```

## Usage
### How quantities are defined in PAGOS
As this package is designed to be used with real-world measurements, quantites in PAGOS encapsulate measurement uncertainty using `uncertainties` and units with `pint`. Although many of the functions in PAGOS will work with other types, they are designed for use with `Quantity` (see [Pint](https://pint.readthedocs.io/en/stable/)) objects with `ufloat` (see [uncertainties](https://pythonhosted.org/uncertainties/)) magnitudes. The following code produces such a quantity representing the speed measurement (11.2 ± 0.3) m/s.
```python
from pint import Quantity, UnitRegistry
from uncertainties import ufloat
u = UnitRegistry()
mySpeed = u.Quantity(ufloat(11.2, 0.3), 'm/s')
mySpeed
# -> <Quantity(11.2000+/-0.3000, 'meter / second')>
```
Writing measurements like this is tedious, so PAGOS implements a shortcut `Q()`:
```python
from pagos import Q
mySpeed = Q(11.2, 'm/s', 0.3)
mySpeed
# -> <Quantity(11.2000+/-0.3000, 'meter / second')>
```
### Gas and water property calculations
The properties of seawater and various gases can be calculated with the `water` and `gas` modules. For example, calculating the density of, kinematic viscosity of and vapour pressure over water at a given temperature and salinity:
```python
from pagos import water
# properties of water at (6.0 ± 0.1) °C temperature and (9.12 ± 0.05) ‰ salinity
T1 = Q(6.0, 'degC', 0.1)
S1 = Q(9.12, 'permille', 0.05)
water.calc_dens(T1, S1) # -> <Quantity(1007.16+/-0.04, 'kilogram / meter ** 3')>
water.calc_vappres(T1) # -> <Quantity(9.34698+/-0.06466, 'millibar')>
water.calc_kinvisc(T1, S1) # -> <Quantity((1.48410+/-0.00457)e-06, 'meter ** 2 / second')>
```
And calculating the Schmidt number and concentration of nitrogen in the water:
```python
from pagos import gas
p1 = Q(1.00, 'atm', 0.01)
gas.calc_Sc('N2', T1, S1) # -> <Quantity(1275.31+/-7.56, 'dimensionless')>
gas.calc_Ceq('N2', T1, S1, p1, 'cc/g') # -> <Quantity(0.0149088+/-0.0001544, 'cubic_centimeter / gram')>
```
### Inverse Modelling
The real power of PAGOS is in its gas exchange modelling capabilities. These can be seen in the tests folder and are briefly explained here. The `fitmodel` function can be used to fit a number of parameters of a gas exchange model using a least-squares minimisation. Here is an example using the fake concentration data taken from the tests folder:
```python
from pagos.modelling import fitmodel
noblegases = ['He', 'Ne', 'Ar', 'Kr', 'Xe']
argtracerlabels = {g:'sample ' + g for g in noblegases}
argtracerlabels['S'] = 'Sal. qu.'
argtracerlabels['p'] = 'prs. qu.'
fakedata_fit = fitmodel(fitmodel=ua_tim_r_taylor,
                        data=fakedata_concs,
                        to_fit=['T_r', 'A', 'R'],
                        init_guess=[Q(1, 'degC'), Q(1e-4, 'cc/g'), Q(1e-2, 'dimensionless')],
                        tracers_used=noblegases,
                        arg_tracer_labels=argtracerlabels,
                        constraints={'A':(0, np.inf), 'R':(0, 1)},
                        tqdm_bar=True,
                        fitted_only=False)
```
The arguments are explained in the method docstrings (*and will be explained in future, more thorough documentation!). This produces an extended DataFrame, appending columns with the fitted values of the parameters `'T_r'`, `'A'` and `'R'`.

```
DataFrame: fakedata_fit
|       sample He        |        sample Ne       | ... |    T_r    |      A      |   R  |
|------------------------|------------------------| ... |-----------|-------------|------|
| (1.30 +- 0.04)e-5 cc/g | (3.05 +- 0.04)e-5 cc/g | ... | 0.34 degC | 2.5e-4 cc/g | 0.03 |
| (1.30 +- 0.04)e-5 cc/g | (3.05 +- 0.04)e-5 cc/g | ... | 4.75 degC | 6.0e-4 cc/g | 0.10 |
            :                        :               :        :            :          :
```
Each row of parameters on the right is fit using the gas tracers on the left.
### Forward modelling
The `forward_model` function can then use previously modelled or simply predefined model parameters to calculate a set of tracer concentrations.
```python
paramlabels = {'T_r':'Rech. temp. qu.', 'A':'Exc. air qu.', 'R':'Ice frac. qu.',
               'S':'Sal. qu.', 'p':'prs. qu.'}
fakedata_concs = forward_model(ua_tim_r_taylor, fakedata_fit, noblegases,
                               paramlabels, fitted_only=False)
```
In this example, as it is modelling based on parameters which were already fitted from a set of given tracer concentrations, these concentrations should be reproduced.
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

Feel free to contact the author, Stanley Scott, at [sscott@iup.uni-heidelberg.de](mailto:sscott@iup.uni-heidelberg.de?subject=PAGOS).

## License

[BSD-3-Clause](https://opensource.org/license/bsd-3-clause), see LICENSE file.\
PAGOS was developed for Python 3 by Stanley Scott and Chiara Hubner.