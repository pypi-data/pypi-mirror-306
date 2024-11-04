"""
Functions for fitting models, creating new ones and running existing ones.
"""
from pint import Quantity, Unit
from uncertainties import ufloat
from uncertainties.core import Variable, AffineScalarFunc
from collections.abc import Iterable
from typing import Callable
import inspect
import numpy as np
import pandas as pd
from lmfit import minimize, Parameters, Model
import wrapt
from tqdm import tqdm
from inspect import signature

from pagos.core import u as _u, Q as _Q, snv as _snv, ssd as _ssd, sgu as _sgu, sto as _sto, units_are_equal as _uae
from pagos._pretty_gas_wrappers import oneormoregases

#TODO not sure if decorator gas_exchange_model belongs here...
#TODO add in protection so that a gas_exchange_model must ALWAYS have `gas` as its first argument?
#TODO gas_exchange_model does NOT support **kwargs arguments due to the Pint module, see explanation in the wrapped part below

# decorator for all model functions that the user may implements
def gas_exchange_model(*, din:tuple, dout:tuple) -> Callable:
    """Decorator that turns a function into a gas exchange model useable within PAGOS. Example implementation:\\
    User wishes to make a simple model: C_mod(gas) = A * abundance(gas) + B * temperature\\
    This is a nonsense model but only an example. This is could be implemented:\\
    `>>> from pagos.gas import abn`\\
    `>>> @gas_exchange_model(din=('cc/g', 'cc/g/K', 'K'), dout='cc/g')`\\
    `>>> def C_mod(gas, A, B, T):`\\
    `... \u2007\u2007\u2007\u2007return A * abn(gas) + B * T`\\
    The `din` units will be assigned to arguments passed into the decorated function, or, if Quantity objects
    which already contain units are passed in, then they will be converted to the `din` units.

    :param din: default units of the parameters passed into the gas_exchange_model
    :type din: tuple
    :param dout: default units of the result of the gas_exchange_model
    :type dout: tuple
    :return: function decorated as a gas exchange model for use in PAGOS
    :rtype: Callable
    """
    @wrapt.decorator    # wrapt decorator used so that function argument specification is preserved (see https://github.com/GrahamDumpleton/wrapt/blob/develop/blog/01-how-you-implemented-your-python-decorator-is-wrong.md)
    def wrapped(func, instance:object, args, kwargs):
        """Decorator for any function representing a gas exchange model, to be used such that
        the function becomes compatible with PAGOS fitting procedure.

        :param func: Model function.
        :param instance: Placeholder required by wrapt's structure.
        :type instance: object
        :param args: Arguments passed to the function. No * due to wrapt funkiness.
        :param kwargs: Keyword arguments passed to the function. No ** due to wrapt funkiness (see https://wrapt.readthedocs.io/en/master/).
        :return: func's return, or possibly nominal_value of func's return if it is a ufloat.
        """
        # unit handling
        # NOTE at the moment, this just defaults to the arguments of the gas_exchange_model decorator.
        # in future, I would like to include the possibility to customise the units_in without having to
        # pass Quantity objects into the model functions. To illustrate, currently, to run e.g. the
        # ua_tim_r_taylor model with user-defined unit input, one must write something like:
        # >>> result = ua_tim_r_taylor('Ne', Q(273, 'K'), Q(3, '%'), Q(1, 'atm'), 0.01, Q(0.0005, 'cc/g'))
        # Here, the K and % units will be converted in this wrapper to degC and permille automatically.
        # However, I would prefer to have:
        # >>> result = ua_tim_r_taylor('Ne', 273, 3, 1, 0.01. 0.0005, units_in=['K', '%', 'atm', '', 'cc/g'])
        # but this does not work, as a **kwargs keyword is required in the ua_tim_r_taylor definition, which
        # then causes an error in _u.wraps() below, as pint.wraps() currently does not support arbitrary *args
        # and **kwargs.
        units_in, units_out = din, dout
        # if default_units_in argument did not include None at the start for the gas parameter, add this in here
        if len(units_in) == len(signature(func).parameters) - 1:
            units_in = (None,) + units_in

        # the actual function call
        wfunc = _u.wraps(units_out, units_in, strict=False)(func)
        ret = wfunc(*args, **kwargs)

        # return
        return ret
    return wrapped



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
            paramsdict[p] = _Q(paramsdict[p], parameter_units[p])
        modelled_data = modelfunc(tracers, **paramsdict)
        # perform conversion of units if necessary
        modelled_units = modelled_data.units
        musinglet, tusinglet = isinstance(modelled_units, Unit), isinstance(tracer_units, Unit)
        def convertandgetmag1():
            nonlocal modelled_data
            modelled_data = modelled_data.magnitude
        def convertandgetmag2():
            nonlocal modelled_data
            modelled_data = np.array([_sto(modelled_data[i], tracer_units[i]).magnitude for i in range(len(tracer_units))])
        if musinglet and tusinglet:
            if modelled_units == tracer_units:
                convertandgetmag1()
            else:
                convertandgetmag2()
        elif musinglet:
            if all(tu == modelled_units for tu in tracer_units):
                convertandgetmag1()
            else:
                convertandgetmag2()
        elif tusinglet:
            if all(mu == tracer_units for mu in modelled_units):
                convertandgetmag1()
            else:
                convertandgetmag2()
        else:
            if all(modelled_units[i] == tracer_units[i] for i in range(len(modelled_units))):
                convertandgetmag1()
            else:
                convertandgetmag2()
        
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


###################################################################################
###################################################################################
# WORK IN PROGRESS - re-work of gas exchange models as classes

class GasExchangeModel:
    def __init__(self, model_function, default_units_in, default_units_out, jacobian=None):
        # set instance variables
        # if default_units_in argument did not include None at the start for the gas parameter, add this in here
        self._model_function_in = model_function
        self.default_units_in = self._check_units_list_against_sig(model_function, default_units_in)
        self.default_units_out = default_units_out
        self.model_arguments = inspect.getfullargspec(self._model_function_in).args
        self.default_units_in_dict = {key:val for key, val in zip(self.model_arguments, self.default_units_in)}
        self._jacobian_in = jacobian
        # the function and jacobian that will run if the user does not specify units_in or units_out when calling run()
        self.model_function = _u.wraps(self.default_units_out, self.default_units_in, strict=False)(self._model_function_in)
        self.model_func_sig = signature(self.model_function)
        if self._jacobian_in is None:
            self.runjac = None
        else:
            self.model_jacobian = _u.wraps(default_units_out, self.default_units_in, strict=False)(self._jacobian_in)
            self.model_jac_sig = signature(self.model_jacobian)
    

    def run(self, *args_to_model_func, units_in='default', units_out='default', **kwargs_to_model_func):
        # wrap the model function differently if units out or in differ from defaults
        if units_in == 'default':
            units_in = self.default_units_in_dict
        elif type(units_in) != dict:
            # set the units_in - append a None value to the units_in tuple for the "units" of the gas argument if this has not already been done by the user
            units_in = self._check_units_list_against_sig(self._model_function_in, units_in)
            # if units are provided in the form of an array instead of a dict, make it a dict
            units_in = {k:u for k, u in zip(self.model_func_sig.parameters, units_in)}
        else:
            units_in = self._check_units_dict_against_sig(self._model_function_in, units_in)
        args_to_model_func = self._convert_or_make_quants_list(args_to_model_func, units_in)
        kwargs_to_model_func = self._convert_or_make_quants_dict(kwargs_to_model_func, units_in)
               
        result = self.model_function(*args_to_model_func, **kwargs_to_model_func)
        if units_out != 'default':
            result = _sto(result, units_out, strict=False)
        return result
    
    def runjac(self, *args_to_jac_func, units_in='default', units_out='default', **kwargs_to_jac_func):
        # NOTE I think due to the nature of this construction, jacobian should always have the same signature as model_function
        # wrap the jacobian differently if units out or in differ from defaults
        if units_in == 'default':
            units_in = self.default_units_in_dict
        elif type(units_in) != dict:
            # set the units_in - append a None value to the units_in tuple for the "units" of the gas argument if this has not already been done by the user
            units_in = self._check_units_list_against_sig(self._jacobian_in, units_in)
            # if units are provided in the form of an array instead of a dict, make it a dict
            units_in = {k:u for k, u in zip(self.model_jac_sig.parameters, units_in)}
        else:
            units_in = self._check_units_dict_against_sig(self._jacobian_in, units_in)
        args_to_jac_func = self._convert_or_make_quants_list(args_to_jac_func, units_in)
        kwargs_to_jac_func = self._convert_or_make_quants_dict(kwargs_to_jac_func, units_in)
        
        result = self.model_jacobian(*args_to_jac_func, units_out=units_out, **kwargs_to_jac_func) 
        if units_out != 'default':
            result = _sto(result, units_out, strict=False)
        return result
    

    @staticmethod
    def _check_units_list_against_sig(func, units):
        if len(units) == len(signature(func).parameters) - 1:
            return (None,) + units
        else:
            return units
    

    @staticmethod
    def _check_units_dict_against_sig(func, units):
        sigparams = signature(func).parameters
        if len(units) == len(sigparams) - 1:
            ret = units
            gasparam = [p for p in sigparams if p not in units][0]
            ret[gasparam] = None
            return ret
        else:
            return units

    
    @staticmethod
    def _convert_or_make_quants_list(values, units):
        ret = [v if units[k] is None else _sto(v, units[k]) if isinstance(v, Quantity) else _Q(v, units[k]) for v, k in zip(values, units)]
        return ret
    

    @staticmethod
    def _convert_or_make_quants_dict(valsdict, units):
        ret = {k:(v if units[k] is None else _sto(v, units[k]) if isinstance(v, Quantity) else _Q(v, units[k]))
               for v, k in zip(valsdict.values(), valsdict.keys())}
        return ret
        
    
    def fit(self, data:pd.DataFrame, to_fit:Iterable[str], init_guess:Iterable[float], tracers_used:Iterable[str], arg_tracer_labels:dict=None, constraints:dict=None, **kwargs) -> pd.DataFrame:   # TODO init_guess is currently only a 1D list, perhaps should be allowed to take a second dimension the same length as data?
         # input to objective function: all parameters (fitted and set), tracers to calculate, observed data and their errors, parameter and tracer units
        def objfunc(parameters, tracers, observed_data, observed_errors, tracer_units):
            # separation of parameter names and values
            parameter_names = list(parameters.valuesdict().keys())
            parameter_values = list(parameters.valuesdict().values())
            paramsdict = {parameter_names[i]:parameter_values[i] for i in range(len(parameter_names))}
            """# re-assemble Quantity objects that were disassembled for usage in lmfit Parameter instances
            if any(not _uae(parameter_units[p], self.default_units_in_dict[p]) for p in parameter_units.keys()):
                for p in parameter_units.keys():
                    if not _uae(parameter_units[p], self.default_units_in_dict[p]):
                        paramsdict[p] = _Q(paramsdict[p], parameter_units[p])""" # TODO DELETE ME?
            modelled_data = self.run(tracers, **paramsdict)
            # perform conversion of units of result if necessary
            if hasattr(modelled_data, 'units'):
                modelled_data = _convertandgetmag(modelled_data, tracer_units)
            
            # if there is an error associated with every observation, weight by the errors
            if all(e is not None for e in observed_errors): #OLD CODE, if a problem arises here, check if reverting back to this fixes it: if observed_errors is not None:
                return (observed_data - modelled_data) / observed_errors
            else:
                return observed_data - modelled_data
        

        def jacfunc(parameters, tracers, observed_data, observed_errors, tracer_units):
            # separation of parameter names and values
            parameter_names = list(parameters.valuesdict().keys())
            parameter_values = list(parameters.valuesdict().values())
            paramsdict = {parameter_names[i]:parameter_values[i] for i in range(len(parameter_names))}
            """# re-assemble Quantity objects that were disassembled for usage in lmfit Parameter instances
            if any(not _uae(parameter_units[p], self.default_units_in_dict[p]) for p in parameter_units.keys()):
                for p in parameter_units.keys():
                    if not _uae(parameter_units[p], self.default_units_in_dict[p]):
                        paramsdict[p] = _Q(paramsdict[p], parameter_units[p])""" # TODO DELETE ME?
            modelled_jac = self.runjac(tracers, **paramsdict)
            # perform conversion of units of result if necessary
            if hasattr(modelled_jac, 'units'):
                modelled_jac = _convertandgetmag(modelled_jac, tracer_units)
            
            return modelled_jac
    
        model_arg_names = self.model_arguments
        data_headers = data.columns.values.tolist()
        output_list = []
        fitted_only_out = False
        nrows = range(len(data))
        # TODO make this more flexible, allow some to be given and some not
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

        # checking for errors on tracers TODO this is still quite primitive, can be made more powerful
        if all(t + ' err' in data_headers for t in tracers_used):
            errs_present_as_col, errstructure = True, 'right'
        elif all('err ' + t in data_headers for t in tracers_used):
            errs_present_as_col, errstructure = True, 'left'
        else:
            errs_present_as_col = False

        # fit procedure for every row
        for r in nrows:
            # parameters to be fitted by lmfit initialised here.
            # lmfit's Parameter class cannot hold uncertainty/unit information that Pint Quantity objects can,
            # therefore we disassemble those objects into their magnitudes and units and then reassemble them
            # in the objective function (see also above).
            #param_units = {}    # dictionary of units of parameters to be used internally  # TODO DELETE ME?
            all_params = Parameters()
            model_sig_as_list = list(self.model_func_sig.parameters)
            for i in range(len(to_fit)):
                # convert units of the initial guess to the default_units_in of the function, so we can save on speed
                p = to_fit[i]
                igi = init_guess[i]
                def_unit = self.default_units_in_dict[p]
                if not isinstance(igi, Quantity):
                    igi = _u.Quantity(igi, def_unit)
                igi = _sto(igi, def_unit).magnitude # <- strip initial guesses of units, for further speed improvements
                
                if constraints is not None and p in constraints.keys():
                    # here the same story as for the initial guesses, but with their constraints
                    min_ = constraints[p][0]
                    max_ = constraints[p][1]
                    if not isinstance(min_, Quantity):
                        min_ = _u.Quantity(min_, def_unit)
                    if not isinstance(max_, Quantity):
                        max_ = _u.Quantity(max_, def_unit)
                    min_ = _sto(min_, def_unit).magnitude
                    max_ = _sto(max_, def_unit).magnitude
                    all_params.add(p, value=igi, vary=True, min=min_, max=max_)
                else:
                    all_params.add(p, value=igi, vary=True)
                #param_units[p] = u TODO DELETE ME?


            # parameters set by observation initialised here
            # similar logic regarding unit dissassembly applies here (see above)  
            for a in model_arg_names:
                if a in arg_tracer_labels and arg_tracer_labels[a] in data_headers: # if a in data_headers and a not in to_fit:
                    # convert the units of values in data to the default_units_in, to save on speed
                    v = data[arg_tracer_labels[a]][r]
                    def_unit = self.default_units_in_dict[a]
                    if not isinstance(v, Quantity):
                        v = _u.Quantity(v, def_unit)
                    v = _sto(v, def_unit).magnitude # <- strip value of units, for further speed improvements
                    # extract nominal value if magnitude is an uncertainties Variable
                    if isinstance(v, (Variable, AffineScalarFunc)):
                        v = v.nominal_value
                    all_params.add(a, value=v, vary=False)
            
            # preparing the data for the minimisation process
            obs_tracerdata_in_row = np.array([_snv(data[arg_tracer_labels[t]][r]) for t in tracers_used])
            if errs_present_as_col:
                if errstructure == 'right':
                    obs_tracerdata_errs_in_row = np.array([_snv(data[arg_tracer_labels[t] + ' err'][r]) for t in tracers_used])
                elif errstructure == 'left':
                    obs_tracerdata_errs_in_row = np.array([_snv(data['err ' + arg_tracer_labels[t]][r]) for t in tracers_used])
            else:
                obs_tracerdata_errs_in_row = np.array([_ssd(data[arg_tracer_labels[t]][r]) for t in tracers_used])
            obs_tracerdata_units_in_row = np.array([_sgu(data[arg_tracer_labels[t]][r]) for t in tracers_used])
            # set Jacobian to None if none was provided in the model
            if self.runjac is None:
                jacfunc = None
            M = minimize(objfunc, all_params, args=(tracers_used, obs_tracerdata_in_row, obs_tracerdata_errs_in_row, obs_tracerdata_units_in_row), method='leastsq', nan_policy='propagate', Dfun=jacfunc)
            optimised_params = M.params
            optimised_param_quants = {}
            for p in to_fit:
                v, e = optimised_params[p].value, optimised_params[p].stderr
                if v is not None and e is not None: # protection for if None values are returned by the fit
                    optimised_param_quants[p] = _u.Quantity(ufloat(v, e), self.default_units_in_dict[p])
                else:
                    optimised_param_quants[p] = _u.Quantity(ufloat(np.nan, np.nan), self.default_units_in_dict[p])
            output_list.append(optimised_param_quants)
        
        output_dataframe = pd.DataFrame(output_list)
        if not fitted_only_out:
            output_dataframe = data.join(output_dataframe)

        return output_dataframe
            




###################
###################
###################
# OLD CODE, DELETE ME
###################
###################
###################
def fitmodelobj(model:GasExchangeModel, data:pd.DataFrame, to_fit:Iterable[str], init_guess:Iterable[float], tracers_used:Iterable[str], arg_tracer_labels:dict=None, constraints:dict=None, **kwargs) -> pd.DataFrame:   # TODO init_guess is currently only a 1D list, perhaps should be allowed to take a second dimension the same length as data?
    """Function that fits a given gas exchange model's parameters to provided tracer data
    in a least-squares fashion with the lmfit module.

    :param model: Gas exchange model containing function whose parameters should be optimised.
    :type model: GasExchangeModel
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
        if any(not _uae(parameter_units[p], model.default_units_in_dict[p]) for p in parameter_units.keys()):
            for p in parameter_units.keys():
                if not _uae(parameter_units[p], model.default_units_in_dict[p]):
                    paramsdict[p] = _Q(paramsdict[p], parameter_units[p])
        modelled_data = model.run(tracers, **paramsdict)
        # perform conversion of units of result if necessary
        if hasattr(modelled_data, 'units'):
            modelled_data = _convertandgetmag(modelled_data, tracer_units)
        
        # if there is an error associated with every observation, weight by the errors
        if all(e is not None for e in observed_errors): #OLD CODE, if a problem arises here, check if reverting back to this fixes it: if observed_errors is not None:
            return (observed_data - modelled_data) / observed_errors
        else:
            return observed_data - modelled_data 
    

    def jacfunc(parameters, tracers, observed_data, observed_errors, parameter_units, tracer_units):
        # separation of parameter names and values
        parameter_names = list(parameters.valuesdict().keys())
        parameter_values = list(parameters.valuesdict().values())
        paramsdict = {parameter_names[i]:parameter_values[i] for i in range(len(parameter_names))}
        # re-assemble Quantity objects that were disassembled for usage in lmfit Parameter instances
        if any(not _uae(parameter_units[p], model.default_units_in_dict[p]) for p in parameter_units.keys()):
            for p in parameter_units.keys():
                if not _uae(parameter_units[p], model.default_units_in_dict[p]):
                    paramsdict[p] = _Q(paramsdict[p], parameter_units[p])
        modelled_jac = model.runjac(tracers, **paramsdict)
        # perform conversion of units of result if necessary
        # TODO I'm not sure this encompasses all cases...
        if hasattr(modelled_jac, 'units'):
            modelled_jac = _convertandgetmag(modelled_jac, tracer_units)
        
        return modelled_jac


    model_arg_names = model.model_arguments
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
                v = init_guess[i]
                u = None
                #raise TypeError('All members of init_guess must have units, i.e. must be Quantity objects.')
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
        # set Jacobian to None if none was provided in the model
        if model.jacobian == None:
            jacfunc = None
        M = minimize(objfunc, all_params, args=(tracers_used, obs_tracerdata_in_row, obs_tracerdata_errs_in_row, param_units, obs_tracerdata_units_in_row), method='leastsq', nan_policy='propagate', Dfun=jacfunc)
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


def _convertandgetmag(modelled_data, tracer_units):
    # TODO I'm not sure this encompasses all cases...
    modelled_units = modelled_data.units
    musinglet, tusinglet = isinstance(modelled_units, Unit), isinstance(tracer_units, Unit)
    def convertandgetmag1():
        nonlocal modelled_data
        return modelled_data.magnitude
    def convertandgetmag2():
        nonlocal modelled_data
        return np.array([_sto(modelled_data[i], tracer_units[i]).magnitude for i in range(len(tracer_units))])
    if musinglet and tusinglet:
        if modelled_units == tracer_units:
            return convertandgetmag1()
        else:
            return convertandgetmag2()
    elif musinglet:
        if all(tu == modelled_units for tu in tracer_units):
            return convertandgetmag1()
        else:
            return convertandgetmag2()
    elif tusinglet:
        if all(mu == tracer_units for mu in modelled_units):
            return convertandgetmag1()
        else:
            return convertandgetmag2()
    else:
        if all(modelled_units[i] == tracer_units[i] for i in range(len(modelled_units))):
            return convertandgetmag1()
        else:
            return convertandgetmag2()