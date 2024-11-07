from functools import reduce
from typing import Final, Literal, TypeAlias
from collections.abc import Callable

import numpy as np
import scipy as sp
import pandas as pd

from attrs import define, field, validators

from .converters import sanitize_inputs, parse_time, convert_inputs

ModelFunc: TypeAlias = Callable[[float | np.ndarray, dict, dict, dict], dict]

STATE_DERIVATIVE_LABEL_TEMPLATE: Final = "d{label}"


@define()
class PhysioModel:
    """A state-space model described by an update function and parameters.

    This class can be used to describe and numerically analyze a state space
    model. A state-space model has at least one state variable that evolves
    over time based on the state, as well as the inputs to and parameters of
    the model.

    The model is described by one or multiple update functions that returns how
    the state changes. An update function should have the signature `fun(time,
    state, inputs, parameters)`. Update functions are called in the order they
    are provided. The output of each update function is added to the input of
    later update functions. Each update function should return a dictionary
    containing state derivatives and other value outputs. State derivates can
    be returned by different functions, but a derivative should be returned for
    all state variables.

    By default, the key for a state derivative should be "d" + the state label,
    e.g. "dvelocity" for the state "velocity". Alternatively, you can supply a
    mapping dictionary `state_derivative_label_map` where the key is the state
    variable label and the value is the state derivative label.

    Inputs and parameters both contain values that can be used by the update
    function. There is, however, a distinction between inputs and parameters.
    Parameters are fixed values that are independent of time, e.g. the mass of
    an object at the end of a pendulum. Inputs are disturbances added to the
    system, and can be either fixed or variable with time, e.g. the force
    applied to a moving mass. `inputs` and `parameters` are both dictionaries.
    `inputs` values can be functions with the signature `fun(time, inputs,
    parameters)`, which are converted to the appropriate before being passed to
    the update function.

    Events are functions with a signature `fun(time, state, inputs,
    parameters)`. An event occurs when a function returns `0`. The solver will
    find an accurate value of `time` where `fun(time, ...) == 0`. This ensures
    proper simulation around that time point. Each event function can be marked
    'terminal' by adding the `terminal` attribute with value `True` to the
    event function (`fun.terminal = True`). This results in the simulation
    being terminal as soon as the event return value crosses `0`. See
    [`scipy.integrate.solve_ivp`](https://docs.scipy.org/doc/scipy-1.14.1/reference/reference/generated/scipy.integrate.solve_ivp.html#scipy.integrate.solve_ivp)
    for more details.

    Post analysis functions can be supplied, which receive the output of the
    system as a pandas DataFrame (see `input_output_response`) and either
    update the dataframe or return an array, list, Series or DataFrame object
    with the same length that is added to the output of the model.

    ### Example

    The example below is the classic undampended pendulum. The system is
    governed by the second derivative of the angle theta. The system state has
    two components: the current angle "theta" and the angular velocity
    "dtheta". The function `pendulum()` calculates the second derivative and
    returns both the first and second derivative. When this system is solved,
    the new state is calculated based on the derivatives of the previous step.

    Example:
    ```
    >>> def pendulum(time, state, inputs, parameters):
    ...     g = parameters["g"]
    ...     l = parameters["l"]
    ...     theta = state["theta"]
    ...
    ...     first_derivative_theta = state["dtheta"]
    ...     second_derivative_theta = -(g / l) * np.sin(theta)
    ...
    ...     return {
    ...         "dtheta": first_derivative_theta,
    ...         "ddtheta": second_derivative_theta
    ...     }
    >>> model = PhysioModel(
    ...     function=pendulum,
    ...     state=("theta", "dtheta"),
    ...     parameters={"g": 9.81, "l": 1},
    ... )
    >>> df = model.input_output_response(time=10, initial_state=(0.1, 0))
    ```

    Args:
        function: a (list of) functions with accepting time, state, inputs and
        parameters as arguments and returning a dictionary containing (at
        least) the state derivatives state: a list containing the state labels,
        or a dictionary containing the intial values of the state inputs: a
        list/tuple containing the input labels, or a dictionary containing the
        inputs parameters: a dictionary containing the parameters of the model
        post_analysis: optional, a dictionary containing functions to calculate
        values based on the output of the model state_derivative_label_map:
        optional, a dictionary mapping the labels of the state derivatives to
        the labels of the state variables.

    """

    function: ModelFunc | list[ModelFunc]
    state: dict[str, float | None] = field(
        kw_only=True,
        converter=lambda x: sanitize_inputs(x, allow_callable=False),
        validator=validators.min_len(1),
    )
    inputs: dict[str, float | Callable | None] = field(
        kw_only=True,
        factory=dict,
        converter=lambda x: sanitize_inputs(x, allow_callable=True),
    )
    parameters: dict[str, float | str | bool] = field(kw_only=True, factory=dict)
    events: Callable | list[Callable] = field(kw_only=True, factory=list)
    post_analysis: dict[str, Callable] = field(kw_only=True, factory=dict)

    state_derivative_label_map: dict[str, str] = field(kw_only=True, factory=dict)

    @property
    def input_labels(self) -> tuple:
        """Labels of the inputs of the model."""
        return tuple(self.inputs)

    @property
    def state_labels(self) -> tuple:
        """Labels of the state variables of the model."""
        return tuple(self.state)

    @property
    def state_derivative_labels(self) -> tuple:
        """Labels of the state derivatives of the model."""
        default_labels = {
            label: STATE_DERIVATIVE_LABEL_TEMPLATE.format(label=label)
            for label in self.state_labels
        }
        updated_labels = default_labels | self.state_derivative_label_map
        return tuple(updated_labels.values())

    def input_output_response(
        self,
        *,
        initial_state: dict | list | tuple | None = None,
        inputs: dict | list | tuple | None = None,
        parameters: dict | list | tuple | None = None,
        time: float | tuple | np.ndarray,
        dt: float | None = None,
        solve_ivp_method: Literal["Radau"] = "Radau",
        rtol=1e-4,
        atol=1e-6,
    ):
        """Generate an output based on the given initial state, inputs and
        parameters.

        This function generates the output of the model over a given time axis
        based on an initial state, the inputs and parameters. If no or not all
        the `initial_state`, `inputs` or `parameters` values are given, the
        values provided to the system at initialisation are used instead.

        The time can be passed in several ways. The simplest is passing a
        duration. The model will be solved up to that duration. When `time` is
        a tuple of length 2, it indicates the start and end time. (Note that
        the initial state is the state at `t=start`, not at `t=0`.) The time
        step will be `dt` if supplied, or determined by the solver otherwise.
        If `time` is a tuple of length 3, the last value is used as the time
        step. If a list or array is supplied, the output will contain these
        time points.

        Relative and abolute tolerance for the solver. The solver estimates a
        local error as `atol + rol * abs(state)`. `rtol` controls a relative
        accuracy ('number of correct digits') while `atol` controls abolute
        accuracy ('number of correct decimal places'). See
        [`scipy.integrate.solve_ivp`](https://docs.scipy.org/doc/scipy-1.14.1/reference/reference/generated/scipy.integrate.solve_ivp.html#scipy.integrate.solve_ivp)
        for more details.

        Args:
            initial_state: optional, initial values for the state as a
            dictionary, or list/tuple of values
            inputs: optional, inputs of the system as a dictionary or
            list/tuple of values
            parameters:
            optional, dictionary with the parameters of the system
            time:
            int/float, tuple or array indicating the time axis of the output
            dt: optional, the time step of the time axis
            solve_ivp_method: solver used; currently only "Radau" is supported
            rtol: float, relative tolerance
            atol: float: absolute tolerance
        """

        inputs = self._parse_inputs(inputs)
        parameters = self._parse_parameters(parameters)
        initial_state = self._parse_state(initial_state)
        (t_start, t_end, time) = parse_time(time, dt)
        events = self._parse_events(inputs, parameters)

        update_function: Callable

        if isinstance(self.function, list):
            functions: list = self.function

            def multiple_functions_wrapper(time, state, inputs, parameters) -> dict:
                updating_inputs = inputs.copy()
                outputs = []
                for function in functions:
                    out = function(time, state, updating_inputs, parameters)
                    updating_inputs |= out
                    outputs.append(out)

                # combine all dictionaries
                return reduce(lambda a, b: {**a, **b}, outputs)

            update_function = multiple_functions_wrapper
        elif callable(self.function):
            update_function = self.function
        else:
            msg = "Provided argument `function` is not a function or list of functions."
            raise TypeError(msg)

        def function_wrapper(
            time, state, inputs=inputs, parameters=parameters, function=update_function
        ) -> dict:
            """Wraps the user function to provide proper inputs and add inputs
            and state to the results."""
            converted_inputs = convert_inputs(inputs, time, parameters)

            state = {k: v for k, v in zip(self.state_labels, state)}
            result = function(time, state, converted_inputs, parameters)

            result = converted_inputs | state | result

            return result

        def simplified_func(time, state, inputs=inputs, parameters=parameters) -> tuple:
            output = function_wrapper(time, state, inputs, parameters)
            return tuple(output[label] for label in self.state_derivative_labels)

        solution = sp.integrate.solve_ivp(
            simplified_func,
            (t_start, t_end),
            [initial_state[k] for k in self.state_labels],
            method=solve_ivp_method,
            t_eval=time,
            events=events,
            rtol=rtol,
            atol=atol,
        )

        # generate an output for each timepoint/state combination
        all_outputs = list(
            function_wrapper(time, state)
            for time, state in zip(solution.t, solution.y.T)
        )
        output_keys = all_outputs[0].keys()

        # zip all outputs
        zipped_outputs = {k: [o[k] for o in all_outputs] for k in output_keys}

        if "time" not in zipped_outputs:
            zipped_outputs["time"] = solution.t

        data_frame = pd.DataFrame(zipped_outputs).set_index("time")

        for k, update_function in self.post_analysis.items():
            post_analysis_result = update_function(data_frame, parameters)
            if post_analysis_result is None:
                pass
            elif isinstance(post_analysis_result, pd.DataFrame):
                # TODO: join with copy of orignal, not original
                data_frame = data_frame.join(post_analysis_result)
            else:
                try:
                    data_frame[k] = post_analysis_result
                except:  # noqa: E722
                    msg = "The result of post analysis can't seem to be added to the output."
                    raise RuntimeError(msg)

        data_frame.attrs = dict(solution)

        return data_frame

    def _parse_events(self, inputs, parameters):
        if self.events is None:
            return []

        def event_wrapper(event):
            if not callable(event):
                msg = f"'{event}' ({type(event)}) is not callable."
                raise TypeError(msg)

            def internal(time, state):
                state = dict(zip(self.state_labels, state))
                return event(
                    time=time, state=state, inputs=inputs, parameters=parameters
                )

            if hasattr(event, "terminal"):
                internal.terminal = event.terminal

            if hasattr(event, "direction"):
                internal.direction = event.direction

            return internal

        events = self.events if isinstance(self.events, list) else [self.events]
        events = [event_wrapper(event) for event in events]
        return events

    def _parse_state(self, state) -> dict:
        if state is None:
            state = {}
        elif isinstance(state, list | tuple):
            state = {k: v for k, v in zip(self.state_labels, state, strict=True)}

        if not isinstance(state, dict):
            msg = f"Initial state should be dict or sequence, not {type(state)}"
            raise TypeError(msg)

        state = self.state | state
        state = sanitize_inputs(state, allow_none=False)
        return state

    def _parse_parameters(self, parameters):
        if parameters is None:
            parameters = {}

        parameters = self.parameters | parameters
        parameters = sanitize_inputs(
            parameters, allow_string=True, allow_none=False, allow_sequence=True
        )
        return parameters

    def _parse_inputs(self, inputs):
        if inputs is None:
            inputs = {}

        elif isinstance(inputs, (list, tuple, np.ndarray)):
            if len(inputs) != len(self.input_labels):
                msg = f"The number of inputs ({len(inputs)}) does not match the number of defined inputs ({len(self.input_labels)})."
                raise ValueError(msg)
            inputs = {k: v for k, v in zip(self.input_labels, inputs, strict=True)}

        if not isinstance(inputs, dict):
            raise TypeError(f"Inputs should be dict or sequence, not {type(inputs)}")

        inputs = self.inputs | inputs
        inputs = sanitize_inputs(inputs, allow_callable=True, allow_none=False)
        return inputs

    def find_equilibrium_state(
        self,
        *,
        time: float,
        dt: float | None = None,
        estimated_equilibrium_state: dict | None = None,
        inputs: dict | None = None,
        parameters: dict | None = None,
        max_n_runs: int = 100,
        rtol: float = 1e-4,
        atol: float = 1e-6,
        rtol_eq: float = 1e-3,
    ):
        for _ in range(max_n_runs):
            if estimated_equilibrium_state is None:
                estimated_equilibrium_state = {k: 0 for k in self.state_labels}

            data = self.input_output_response(
                time=time,
                dt=dt,
                initial_state=estimated_equilibrium_state,
                inputs=inputs,
                parameters=parameters,
                atol=atol,
                rtol=rtol,
            )
            final_state = dict(data.loc[:, self.state_labels].iloc[-1])

            if np.allclose(
                list(estimated_equilibrium_state.values()),
                list(final_state.values()),
                rtol=rtol_eq,
            ):
                return final_state

            estimated_equilibrium_state = final_state

        else:
            msg = f"Could not find an equilibrium in {max_n_runs} iterations."
            raise RuntimeError(msg)
