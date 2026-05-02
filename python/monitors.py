from typing import Optional

from thermostat import State, Mode, Input

"""
Defines safety and liveness monitors for the smart thermostat.

Safety checks ensure invalid states never occur, while liveness checks track
whether the system eventually behaves correctly over time. These monitors are
used during simulation and model checking to detect property violations.
"""

# LIVENESS MONITORS =====================================================================================================

class LivenessMonitor:
    def __init__(self, max_wait=5):
        self.max_wait = max_wait
        self.active = {"L1": False, "L2": False, "L3": False, "L4": False, "L5": False, "L6": False}
        self.counter = {"L1": 0, "L2": 0, "L3": 0, "L4": 0, "L5": 0, "L6": 0}


    def clone(self):
        copied = LivenessMonitor(self.max_wait)
        copied.active = self.active.copy()
        copied.counter = self.counter.copy()
        return copied


    def heat_mode_updates_correctly(self, state : State) -> bool:
        """ L1: If heating is selected and temp < setpoint, eventually begin heating."""
        trigger = state.selected_mode == Mode.HEAT and state.temp < state.setpoint
        fulfilled = state.mode == Mode.HEAT
        return self._check_eventually("L1", trigger, fulfilled)


    def cool_mode_updates_correctly(self, state : State) -> bool:
        """ L2: If cooling is selected and temp > setpoint, eventually begin cooling."""
        trigger = state.selected_mode == Mode.COOL and state.temp > state.setpoint
        fulfilled = state.mode == Mode.COOL
        return self._check_eventually("L2", trigger, fulfilled)


    def heating_increases_temperature(self, state : State, next_state : State) -> bool:
        """ L3: If heating is active, temperature should eventually rise."""
        trigger = state.mode == Mode.HEAT
        fulfilled = next_state.temp > state.temp
        return self._check_eventually("L3", trigger, fulfilled)


    def cooling_decreases_temperature(self, state : State, next_state : State) -> bool:
        """ L4: If cooling is active, temperature should eventually fall."""
        trigger = state.mode == Mode.COOL
        fulfilled = next_state.temp < state.temp
        return self._check_eventually("L4", trigger, fulfilled)


    def eventually_reach_setpoint(self, state : State, next_state : State) -> bool:
        """ L5: If the system is trying to reach the setpoint, it should eventually get there."""
        trigger = (state.mode == Mode.HEAT and state.temp < state.setpoint) or (
                state.mode == Mode.COOL and state.temp > state.setpoint)
        fulfilled = next_state.temp == next_state.setpoint
        return self._check_eventually("L5", trigger, fulfilled)


    def mode_becomes_selected_mode(self, state : State, next_state : State, inputs : Input) -> bool:
        """
        L6: If no new mode command is issued, the system will eventually align the mode
        with the selected mode.
        """
        trigger = inputs.new_mode_cmd is None and state.mode != state.selected_mode
        fulfilled = next_state.mode == next_state.selected_mode
        return self._check_eventually("L6", trigger, fulfilled)


    def _check_eventually(self, prop: str, trigger: bool, fulfilled: bool) -> bool:
        # start obligation only once
        if trigger and not self.active[prop]:
            self.active[prop] = True
            self.counter[prop] = 0

        # if no active obligation, property holds
        if not self.active[prop]:
            return True

        # if fulfilled, clear obligation
        if fulfilled:
            self.active[prop] = False
            self.counter[prop] = 0
            return True

        # otherwise increment counter
        self.counter[prop] += 1
        return self.counter[prop] <= self.max_wait


# SAFETY MONITORS ======================================================================================================

def no_simultaneous_heat_cool(heat_on: bool, cool_on: bool) -> bool:
    """ S1: The thermostat cannot be heating and cooling at the same time. """
    return not (heat_on and cool_on)


def no_heat_cool_when_off(heat_on: bool, cool_on: bool, state: State) -> bool:
    """ S2: When the thermostat is off, heating or cooling must both be off. """
    return state.mode != Mode.OFF or (not heat_on and not cool_on)


def timer_expiration_turns_off(state : State, next_state : State) -> bool:
    """ S3: The thermostat must turn off in the next tick when the timer runs out. """
    return not (state.timer_active and state.timer == 0) or next_state.mode == Mode.OFF


def turn_off_at_setpoint(state: State, next_state: State, inputs: Input) -> bool:
    """
    S4: In heating mode, when current temperature is >= desired temperature, the thermostat
        will turn off in the same tick.
    S5: In cooling mode, when current temperature is <= desired temperature, the thermostat
        will turn off in the same tick.
    """
    effective_setpoint = inputs.new_setpoint if inputs.new_setpoint is not None else state.setpoint
    s4 = state.mode == Mode.HEAT and state.temp >= effective_setpoint
    s5 = state.mode == Mode.COOL and state.temp <= effective_setpoint
    return not (s4 or s5) or next_state.mode == Mode.OFF


def selected_mode_updates_correctly(next_state : State, new_mode_cmd : Optional[Mode]) -> bool:
    """
    S6: If a new mode command is issued, the thermostat stores that command as the selected
    mode in the next tick.
    """
    if new_mode_cmd is None:
        return True

    return next_state.selected_mode == new_mode_cmd

