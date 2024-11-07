import numpy as np
from numpy.typing import ArrayLike


def sanitize_inputs(
    inputs,
    allow_none=True,
    allow_callable=False,
    allow_string=False,
    allow_sequence=False,
):
    if not isinstance(inputs, dict):
        inputs = dict.fromkeys(inputs)

    def check_value(key, value):
        if not isinstance(key, str):
            msg = f"Keys should be a non-string sequence, not '{key}' ({type(key)})"
            raise TypeError(msg)

        if (
            (allow_none and value is None)
            or isinstance(value, (int, float))
            or (allow_callable and callable(value))
            or (allow_string and isinstance(value, str))
            or (allow_sequence and isinstance(value, (list, tuple)))
        ):
            return value

        if isinstance(value, list):
            value = np.array(value)

        if isinstance(value, np.ndarray):
            if np.sum(np.array(value.shape)) != 1:
                raise ValueError("Input array should be 1D or reducable to 1D")

            value = np.flatten(value)

            return value

        msg = f"Input with key '{key}' must be a {'function, ' if allow_callable else ''}number, list or 1D-array, not '{value}' ({type(value)})."
        raise TypeError(msg)

    return {key: check_value(key, value) for key, value in inputs.items()}


def parse_time(
    time: float | tuple[float, float] | tuple[float, float, float] | list | np.ndarray,
    dt: float | None = None,
) -> tuple[float, float, np.ndarray]:
    step = start = end = None

    if isinstance(time, (float, int)):
        start = 0
        end = time
        step = dt
    elif isinstance(time, tuple) and len(time) == 2:
        start = time[0] or 0
        end = time[1]
        step = dt
    elif isinstance(time, tuple) and len(time) == 3:
        if dt:
            msg = "Multiple values for `dt`: can't parse `time` as a tuple with length 3 when `dt` is set."
            raise ValueError(msg)
        start = time[0] or 0
        end = time[1]
        step = time[2]
    elif isinstance(time, tuple):
        msg = f"`time` should a tuple with length 2 or 3, not {time}"
        raise ValueError(msg)
    elif isinstance(time, list):
        time = np.array(time)

    if isinstance(time, np.ndarray):
        start = time[0]
        end = time[-1]
    elif step:
        time = np.arange(start, end, step)
    else:
        time = None

    if start is None or end is None:
        raise ValueError("`time` cannot be parsed. No start and end are provided.")

    return start, end, time


def convert_inputs(inputs: dict, time: int | ArrayLike, parameters):
    """Converts function inputs to values at the given time point."""

    parsed_inputs = dict()
    for key, input_ in inputs.items():
        if callable(input_):
            parsed_inputs[key] = input_(time=time, parameters=parameters)
        else:
            parsed_inputs[key] = input_

        if (
            isinstance(parsed_inputs[key], np.ndarray)
            and parsed_inputs[key].shape == tuple()
        ):
            # convert 0D array to number
            parsed_inputs[key] = parsed_inputs[key].item()

    return parsed_inputs
