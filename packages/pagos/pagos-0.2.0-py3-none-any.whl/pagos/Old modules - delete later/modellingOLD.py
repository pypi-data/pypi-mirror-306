"""
Functions for fitting models, creating new ones and running existing ones.
"""
from pint import Quantity
from uncertainties import ufloat
from uncertainties.core import Variable, AffineScalarFunc
from collections.abc import Iterable
from typing import Callable
import inspect
import numpy as np
import pandas as pd
from lmfit import minimize, Parameters
import wrapt
from tqdm import tqdm
from inspect import signature

from pagos.core import u as _u, Q as _Q, snv as _snv, ssd as _ssd, sgu as _sgu
from pagos._pretty_gas_wrappers import oneormoregases

#TODO not sure if decorator gas_exchange_model belongs here...
#TODO add in protection so that a gas_exchange_model must ALWAYS have `gas` as its first argument
# decorator for all model functions that the user may implements
@wrapt.decorator    # wrapt decorator used so that function argument specification is preserved (see https://github.com/GrahamDumpleton/wrapt/blob/develop/blog/01-how-you-implemented-your-python-decorator-is-wrong.md)
def gas_exchange_model(func, instance:object, args, kwargs):
    """Decorator for any function representing a gas exchange model, to be used such that
    the function becomes compatible with PAGOS fitting procedure.

    :param func: Model function.
    :param instance: Placeholder required by wrapt's structure.
    :type instance: object
    :param args: Arguments passed to the function. No * due to wrapt funkiness.
    :param kwargs: Keyword arguments passed to the function. No ** due to wrapt funkiness.
    :return: func's return, or possibly nominal_value of func's return if it is a ufloat.
    """
    # check that call signature of func is correct TODO is there a better way than forcing user to write **kwargs?
    if 'kwargs' not in signature(func).parameters:
        raise TypeError('Any function decorated with gas_exchange_model must have a final **kwargs argument in its signature.')
    
    # set to fit mode if a fitting procedure rather than a forward modelling procedure is being run
    fit_mode = False
    if 'fit_mode' in kwargs:
        if kwargs['fit_mode'] == True:
            fit_mode = True
    
    # the actual function call
    ret = func(*args, **kwargs)
    
    # convert function result to desired units
    if 'output_units' in kwargs:
        new_units = kwargs['output_units']
        # TODO this for some reason does not work with sto(); sto() needs to be greatly improved!
        ret = np.array([elt.to(new_units[i]) for i, elt in enumerate(ret)])
        # maybe add this in for speed? I don't know if this will actually be helpful though...
        # if all(ret[i].units == ret[i+1].units for i in range(len(ret)-1)):
        #    ret = Quantity(np.array([elt.magnitude for elt in ret]), ret[0].units)

    if fit_mode:
        # boilerplate for different type handling - TODO quite ugly, can we change this to be nicer??
        if isinstance(ret, Iterable): 
            def return_array(): # definition here so we don't have to write this twice
                retarr = []
                for v in ret:
                    vm = v
                    if type(vm) == _u.Quantity:
                        vm = vm.magnitude
                    if type(vm) in [Variable, AffineScalarFunc]:    #TODO kinda ugly, but for some reason vm.magnitude always gives AffineScalarFunc instead of Variable. So this is a dirty fix.
                        vm = vm.nominal_value
                    retarr.append(vm)
                return np.array(retarr)
            
            if type(ret) == _u.Quantity:    # this seems to be the only way to distinguish iterable Variables/Quantities from singular ones I can come up with at the moment
                if isinstance(ret.magnitude, Iterable):
                    return return_array() # FIXME there's no else statement here, could cause trouble
            else:
                return return_array()
        else:
            if type(ret) == _u.Quantity:
                ret = ret.magnitude
            if type(ret) in [Variable, AffineScalarFunc]:
                ret = ret.nominal_value
            return ret
    else:
        if type(ret) not in [_u.Quantity, Variable] and isinstance(ret, Iterable):
            return np.array([v for v in ret])
        else:
            return ret



# TODO set up some model function object which has a default set of to_fit, init_guess variables so they don't have to be typed in every time?
# TODO parameters such as T, S and p have no associated uncertainty when considered here - is that okay?
def fitmodel(modelfunc:Callable, data:pd.DataFrame, to_fit:Iterable[str], init_guess:Iterable[float], tracers_used:Iterable[str], arg_tracer_labels:dict=None, constraints:dict=None, **kwargs) -> pd.DataFrame:   # TODO init_guess is currently only a 1D list, perhaps should be allowed to take a second dimension the same length as data?
    """Function that fits a given gas exchange model's parameters to provided tracer data
    in a least-squares fashion with the lmfit module.

    :param modelfunc: Gas exchange model function whose parameters should be optimised.
    :type modelfunc: Callable
    :param data: Tracer data. Must include, at minimum, entries for all tracers and non-fitted model parameters.
    :type data: DataFrame
    :param to_fit: Names of the parameters to be fitted by lmfit.
    :type to_fit: Iterable[str]
    :param init_guess: Initial guesses for the parameters to be fitted.
    :type init_guess: Iterable[float]
    :param tracers_used: Names of the tracers to be used in fitting, for example ['He', 'Ne', 'N2'].
    :type tracers_used: Iterable[str]
    :param to_fit_units: Output units of each parameter to be fitted.
    :type to_fit_units: dict, optional
    :param arg_tracer_labels: Names of the column headers in data corresponding to each string in `tracer_labels` and the arguments passed to `modelfunc`.
    :type arg_tracer_labels: dict, optional
    :param constraints: Constraints (upper and lower bounds, l and u) on parameters p in the form of a dict {p₁:(l₁, u₁), ..., pₙ:(lₙ, uₙ)}.
    :type constraints: dict, optional
    :param tqdm_bar: Whether or not to print out a tqdm progress bar in the terminal when fitting, defaults to False
    :type tqdm_bar: bool, optional
    :return: DataFrame of all the fitted parameters, for each row in data.
    :rtype: DataFrame
    """
    # input to objective function: all parameters (fitted and set), tracers to calculate, observed data and their errors, parameter and tracer units
    def objfunc(parameters, tracers, observed_data, observed_errors, parameter_units, tracer_units):
        # separation of parameter names and values
        parameter_names = list(parameters.valuesdict().keys())
        parameter_values = list(parameters.valuesdict().values())
        paramsdict = {parameter_names[i]:parameter_values[i] for i in range(len(parameter_names))}
        # re-assemble Quantity objects that were disassembled for usage in lmfit Parameter instances
        for p in parameter_units.keys():
            paramsdict[p] = _Q(paramsdict[p], parameter_units[p], 0) # TODO currently sets uncertainty to zero, should original uncertainty be considered?
        modelled_data = modelfunc(tracers, **paramsdict, fit_mode=True, output_units=tracer_units)
        # if there is an error associated with every observation, weight by the errors
        if all(e is not None for e in observed_errors): #OLD CODE, if a problem arises here, check if reverting back to this fixes it: if observed_errors is not None:
            return (observed_data - modelled_data) / observed_errors
        else:
            return observed_data - modelled_data 

    model_arg_names = inspect.getfullargspec(modelfunc).args
    data_headers = data.columns.values.tolist()
    output_list = []
    fitted_only_out = False
    nrows = range(len(data))
    if arg_tracer_labels == None:
            # default behaviour for no input in tracer labels: take the user-given
            # names of the tracers used and the set names of the args of modelfunc
            # which are not to be fit.
            dont_fit_these_args = [a for a in model_arg_names if a not in to_fit]
            arg_tracer_labels = {x:x for x in tracers_used + dont_fit_these_args}

    # keyword argument handling
    for k in kwargs.keys():
        kv = kwargs[k]
        # terminal loading bar
        if k == 'tqdm_bar':
            if kv == True:
                nrows = tqdm(range(len(data)))
        # whether to output all data + fitted parameters or only fitted parameters
        if k == 'fitted_only':
            if kv == True:
                fitted_only_out = True

    for r in nrows:
        # parameters to be fitted by lmfit initialised here.
        # lmfit's Parameter class cannot hold uncertainty/unit information that Pint Quantity objects can,
        # therefore we disassemble those objects into their magnitudes and units and then reassemble them
        # in the objective function (see also above).
        param_units = {}    # dictionary of units of parameters to be used internally
        all_params = Parameters()
        for i in range(len(to_fit)):
            p = to_fit[i]
            if type(init_guess[i]) == _u.Quantity:
                v = init_guess[i].magnitude
                u = init_guess[i].units
            else:
                raise TypeError('All members of init_guess must have units, i.e. must be Quantity objects.')
            if constraints is not None and p in constraints.keys():
                min_ = constraints[p][0]
                max_ = constraints[p][1]
                all_params.add(p, value=v, vary=True, min=min_, max=max_)
            else:
                all_params.add(p, value=v, vary=True)
            param_units[p] = u


        # parameters set by observation initialised here
        # similar logic regarding unit dissassembly applies here (see above)  
        for a in model_arg_names:
            if a in arg_tracer_labels and arg_tracer_labels[a] in data_headers: # if a in data_headers and a not in to_fit:
                v = data[arg_tracer_labels[a]][r]
                # extract magnitude if the parameter is a pint Quantity
                if isinstance(v, Quantity): # TODO used to have this but fails when loading a pickled dataframe. Is there a better solution?: if type(v) == _u.Quantity:
                    param_units[a] = v.units
                    v = v.magnitude
                # extract nominal value if magnitude is an uncertainties Variable
                if type(v) in [Variable, AffineScalarFunc]:
                    v = v.nominal_value
                all_params.add(a, value=v, vary=False)
        
        obs_tracerdata_in_row = np.array([_snv(data[arg_tracer_labels[t]][r]) for t in tracers_used])
        obs_tracerdata_errs_in_row = np.array([_ssd(data[arg_tracer_labels[t]][r]) for t in tracers_used])
        obs_tracerdata_units_in_row = np.array([_sgu(data[arg_tracer_labels[t]][r]) for t in tracers_used])
        M = minimize(objfunc, all_params, args=(tracers_used, obs_tracerdata_in_row, obs_tracerdata_errs_in_row, param_units, obs_tracerdata_units_in_row), method='leastsq', nan_policy='propagate')
        optimised_params = M.params
        optimised_param_quants = {}
        for p in to_fit:
            v, e = optimised_params[p].value, optimised_params[p].stderr
            if v is not None and e is not None: # protection for if None values are returned by the fit
                optimised_param_quants[p] = _u.Quantity(ufloat(v, e), param_units[p])
            else:
                optimised_param_quants[p] = _u.Quantity(ufloat(np.nan, np.nan), param_units[p])
        output_list.append(optimised_param_quants)
    
    output_dataframe = pd.DataFrame(output_list)
    if not fitted_only_out:
        output_dataframe = data.join(output_dataframe)

    return output_dataframe


def forward_model(modelfunc, data:pd.DataFrame, to_model:list, param_labels:dict, **kwargs) -> pd.DataFrame:
    """Calculates the results of a gas exchange model, given a large set
    of observations / parameters.

    :param modelfunc: Gas exchange model function used in calculation.
    :type modelfunc: function
    :param data: Observations/parameters dataset. Must include, at minimum, entries for all model parameters.
    :type data: DataFrame
    :param to_model: Parameters (arguments of `modelfunc`) to fit.
    :type to_model: list
    :param param_labels: Dictionary matching arguments of `modelfunc` to perhaps differently-named column headings of `data`.
    :type param_labels: dict
    :return: Results of the forward modelling.
    :rtype: DataFrame.
    """
    output_list = []
    nrows = len(data)
    # TODO change the name from fitted to modelled or something
    fitted_only_out = False

    # keyword argument handling
    for k in kwargs.keys():
        kv = kwargs[k]
        # whether to output all data + fitted parameters or only fitted parameters
        if k == 'fitted_only' and kv == True:
            fitted_only_out = True
    
    # perform modelling for each row
    for r in range(nrows):
        params_and_values = {p:data[param_labels[p]][r] for p in param_labels}
        model_result = {}
        res_arr = modelfunc(to_model, **params_and_values)
        for i, tm in enumerate(to_model):
            label = 'modelled ' + tm
            model_result[label] = res_arr[i]
        output_list.append(model_result)
    
    output_dataframe = pd.DataFrame(output_list)
    if not fitted_only_out:
        output_dataframe = data.join(output_dataframe)
    
    return output_dataframe

