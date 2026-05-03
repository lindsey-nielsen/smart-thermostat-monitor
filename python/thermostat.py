from enum import Enum
from dataclasses import dataclass
from typing import Tuple
from typing import Optional

"""
Implements the core logic of a smart thermostat system.

This module defines the system state, inputs, and transition behavior for
a thermostat that supports heating, cooling, timers, and setpoints.
Each step updates the system based on user inputs and environmental conditions.

The model includes both a correct temperature update and a buggy version,
allowing testing of safety and liveness properties under faulty behavior.
"""

# DATA MODELS ==========================================================================================================

class Mode (Enum):
    OFF = 0
    HEAT = 1
    COOL = 2


@dataclass(frozen=True)
class State:
    mode: Mode
    selected_mode: Mode
    temp: int
    setpoint: int
    timer: int
    timer_active: bool


@dataclass(frozen=True)
class Input:
    new_mode_cmd: Optional[Mode]
    new_setpoint: Optional[int]
    timer_set: Optional[int]
    ambient_temp: int


# OUTPUT LOGIC =========================================================================================================

def get_outputs(state: State) -> Tuple[bool, bool]:
    """
    Determines output signals based on the current mode
    Returns: heat_on, cool_on
    """
    return state.mode == Mode.HEAT, state.mode == Mode.COOL


# INPUT PROCESSING ====================================================================================================

def update_mode_cmd(state : State, new_mode_cmd: Optional[Mode]) -> Mode:
    """
    Updates the selected mode based on user input.
    - If a new mode command is provided, use it.
    - Otherwise, keep the current selected mode.
    Returns: updated selected_mode
    """
    return new_mode_cmd if new_mode_cmd is not None else state.selected_mode


def update_setpoint(state: State, new_setpoint: Optional[int]) -> int:
    """
    Updates the temperature setpoint based on user input.
    - If a new setpoint is provided, use it.
    - Otherwise, keep the current setpoint.
    Returns: updated setpoint value
    """
    return new_setpoint if new_setpoint is not None else state.setpoint


def update_timer(state: State, timer_set: Optional[int]) -> Tuple[int, bool]:
    """
    Updates the timer and its active status
    - if a new timer value is provided and > 0, start/reset the timer
    - if the timer is active, decrement it
    - otherwise, reset timer and deactivate it
    Returns: updated timer value and timer_active flag
    """
    if timer_set is not None and timer_set > 0:
        return timer_set, True

    elif state.timer_active and state.timer > 0:
        return state.timer - 1, True

    else:
        return 0, False


# MODE TRANSITIONS =====================================================================================================

def update_mode(state: State, selected_mode: Mode, setpoint: int, new_mode_cmd: Optional[Mode]) -> Tuple[Mode, Mode]:
    """
    Determines the next operating mode of the thermostat
    - Turns OFF if commanded, timer expires, or setpoint is reached
    - Turns HEAT/COOL on if commanded and temperature is outside threshold
    - Otherwise keeps the current mode
    Returns: next mode and selected mode
    """
    delta: int = 1
    timer_expired : bool = state.timer_active and state.timer == 0
    new_command_issued : bool = new_mode_cmd is not None

    # user explicitly turned system off
    if new_command_issued and selected_mode == Mode.OFF:
        return Mode.OFF, Mode.OFF

    # timer expires only if no new command was issued
    if timer_expired and not new_command_issued:
        return Mode.OFF, Mode.OFF

    # stop heating/cooling once setpoint is reached
    if state.mode == Mode.HEAT and state.temp >= setpoint:
        return Mode.OFF, selected_mode

    if state.mode == Mode.COOL and state.temp <= setpoint:
        return Mode.OFF, selected_mode

    # start heating/cooling if selected mode requires it
    if selected_mode == Mode.HEAT and state.temp <= setpoint - delta:
        return Mode.HEAT, selected_mode

    if selected_mode == Mode.COOL and state.temp >= setpoint + delta:
        return Mode.COOL, selected_mode

    # if selected mode is OFF, stay off
    if selected_mode == Mode.OFF:
        return Mode.OFF, selected_mode

    return state.mode, selected_mode


def update_mode_buggy(state: State, selected_mode: Mode, setpoint: int, new_mode_cmd: Optional[Mode]) -> Tuple[Mode, Mode]:
    """
    Buggy mode update: ignores timer expiration.
    """
    delta: int = 1
    new_command_issued : bool = new_mode_cmd is not None

    # user explicitly turned system off
    if new_command_issued and selected_mode == Mode.OFF:
        return Mode.OFF, Mode.OFF

    # bug! removed timer expiration check

    # stop heating/cooling once setpoint is reached
    if state.mode == Mode.HEAT and state.temp >= setpoint:
        return Mode.OFF, selected_mode

    if state.mode == Mode.COOL and state.temp <= setpoint:
        return Mode.OFF, selected_mode

    # start heating/cooling if selected mode requires it
    if selected_mode == Mode.HEAT and state.temp <= setpoint - delta:
        return Mode.HEAT, selected_mode

    if selected_mode == Mode.COOL and state.temp >= setpoint + delta:
        return Mode.COOL, selected_mode

    # if selected mode is OFF, stay off
    if selected_mode == Mode.OFF:
        return Mode.OFF, selected_mode

    return state.mode, selected_mode


# TEMPERATURE UPDATE ===================================================================================================

def update_temp(state: State, mode: Mode, ambient_temp: int) -> int:
    """
    Updates the temperature based on system behavior
    - in HEAT mode, temperature increases
    - in COOL mode, temperature decreases
    - Otherwise moves toward ambient temperature
    Returns: updated temp
    """
    temp: int

    if mode == Mode.HEAT:
        temp = state.temp + 1
    elif mode == Mode.COOL:
        temp = state.temp - 1
    elif state.temp < ambient_temp:
        temp = state.temp + 1
    elif state.temp > ambient_temp:
        temp = state.temp - 1
    else:
        temp = state.temp

    return temp


def update_temp_buggy(state: State, mode: Mode, ambient_temp: int) -> int:
    """
    Buggy temperature update: decreases temp when heating and increases when cooling.
    """
    temp: int

    if mode == Mode.HEAT:
        temp = state.temp - 1   # bug! heating decreases
    elif mode == Mode.COOL:
        temp = state.temp + 1   # bug! cooling increases
    elif state.temp < ambient_temp:
        temp = state.temp + 1
    elif state.temp > ambient_temp:
        temp = state.temp - 1
    else:
        temp = state.temp

    return temp


# SYSTEM STEP ==========================================================================================================

def step(state: State, inputs: Input, use_buggy_temp=False, use_buggy_mode=False) -> Tuple[State, bool, bool]:
    """
    Executes one step of the system
    - Computes outputs (heat_on, cool_on)
    - Updates timer and mode
    - Updates temperature
    - Constructs the next state
    - Can use buggy functions instead by setting those parameters to true
    Returns: next_state, heat_on, cool_on
    """
    heat_on: bool
    cool_on: bool
    timer: int
    timer_active: bool
    mode: Mode
    temp: int
    setpoint: int
    selected_mode: Mode

    heat_on, cool_on = get_outputs(state)
    selected_mode = update_mode_cmd(state, inputs.new_mode_cmd)
    setpoint = update_setpoint(state, inputs.new_setpoint)
    timer, timer_active = update_timer(state, inputs.timer_set)

    # Choose between correct and buggy mode update
    if use_buggy_mode:
        mode, selected_mode = update_mode_buggy(state, selected_mode, setpoint, inputs.new_mode_cmd)
    else:
        mode, selected_mode = update_mode(state, selected_mode, setpoint, inputs.new_mode_cmd)

    # Choose between correct and buggy temperature update
    if use_buggy_temp:
        temp = update_temp_buggy(state, mode, inputs.ambient_temp)
    else:
        temp = update_temp(state, mode, inputs.ambient_temp)

    next_state: State = State(
        mode=mode,
        selected_mode=selected_mode,
        temp=temp,
        setpoint=setpoint,
        timer=timer,
        timer_active=timer_active,
    )

    return next_state, heat_on, cool_on









