from typing import Literal


def state_crosses_value(
    label: str,
    value: float,
    *,
    terminal: bool = False,
    direction: Literal[-1, 0, 1] = 0,
):
    """
    Create an event that detects when a state crossing the given value.


    Example:
        # This example will have an event and terminate when the volume (state)
        # crosses the value 0.

        model = PhysioModeler(
            ...,
            events=[
                state_crosses_value("volume", 0, terminal=True),
            ]
        )

    Attrs:
        label: label of the state to track
        value: the event will trigger when the state crosses this value
        terminal: whether to terminate the simulation if the event occurs
        direction: if 0, any crossing will be detected; if 1, only positive
        crossings (value goes from negative to positive) will be detected; if
        -1, only negative crossings will be detected.
    """

    def event(time, state, inputs, parameters):
        return state[label] - value

    event.terminal = terminal
    event.direction = direction
    return event
