from collections import deque
from typing import Optional, List
from monitors import (
    LivenessMonitor,
    no_simultaneous_heat_cool,
    no_heat_cool_when_off,
    timer_expiration_turns_off,
    turn_off_at_setpoint,
    selected_mode_updates_correctly,
)
from thermostat import Mode, Input, State, step

"""
Performs BFS model checking on a smart thermostat.

The system explores possible state transitions from an initial state using
generated inputs. At each step, safety and liveness properties are checked.

Safety properties ensure invalid states never occur, while liveness properties
ensure the system eventually behaves correctly.

If a violation is found, a counterexample trace is printed showing the sequence
of states and inputs that led to the issue.
"""

# INPUT GENERATION =====================================================================================================

def generate_inputs_for_heating_liveness(state: State):
    """
    Generates a minimal input sequence to drive the system into a heating scenario.
    Used to expose liveness violations related to heating behavior.
    """
    if state.selected_mode == Mode.OFF:
        return [Input(Mode.HEAT, 72, None, 65)]
    return [Input(None, None, None, 65)]


def generate_inputs_for_cooling_liveness(state: State):
    """
    Generates a minimal input sequence to drive the system into a cooling scenario.
    Used to expose liveness violations related to cooling behavior.
    """
    if state.selected_mode == Mode.OFF:
        return [Input(Mode.COOL, 68, None, 75)]
    return [Input(None, None, None, 75)]


def generate_inputs_for_safety(state : State):
    """
    Generates a reduced set of meaningful inputs for safety checking.
    Limits branching while still exploring relevant state transitions.
    """
    inputs = []

    possible_modes: List[Optional[Mode]] = [None]
    for mode in [Mode.OFF, Mode.HEAT, Mode.COOL]:
        if mode != state.selected_mode:
            possible_modes.append(mode)

    possible_setpoints: List[Optional[int]] = [None]
    for setpoint in [68, 70, 72]:
        if setpoint != state.setpoint:
            possible_setpoints.append(setpoint)

    possible_timers: List[Optional[int]] = [None]
    for timer in [1, 2, 3]:
        if not state.timer_active or timer != state.timer:
            possible_timers.append(timer)

    # small finite ambient set
    possible_ambient = [65, 70, 75]

    for mode_cmd in possible_modes:
        for setpoint in possible_setpoints:
            for timer_set in possible_timers:
                for ambient in possible_ambient:
                    inputs.append(Input(
                        new_mode_cmd=mode_cmd,
                        new_setpoint=setpoint,
                        timer_set=timer_set,
                        ambient_temp=ambient
                    ))

    return inputs


# TRACE RECONSTRUCTION =================================================================================================

def reconstruct_trace(parent_map, input_map, end_state):
    """
    Reconstructs the execution path from the initial state to the given end state.
    Each step includes the state and the input that led to it.
    """
    trace = []
    current = end_state

    while current is not None:
        trace.append((current, input_map.get(current)))
        current = parent_map.get(current)

    trace.reverse()
    return trace


def print_trace(trace):
    """
    Prints a counterexample trace showing states and inputs step-by-step.
    """
    print("\nCounterexample trace:")
    for i, (state, input_used) in enumerate(trace):
        print(f"\nStep {i}:")
        print("State:", state)
        if input_used is not None:
            print("Input:", input_used)


def update_trace_maps(parent_map, input_map, state, next_state, inputs):
    """
    Stores parent and input mappings for trace reconstruction.
    """
    if next_state not in parent_map:
        parent_map[next_state] = state
        input_map[next_state] = inputs


# BFS SETUP & STATE TRACKING ===========================================================================================

def initialize_bfs(initial_state):
    """
    Initializes BFS structures: visited set, queue, parent map, and input map.
    """
    visited = set()

    initial_monitor = LivenessMonitor()
    initial_key = (initial_state, monitor_key(initial_monitor))
    visited.add(initial_key)

    parent_map = {initial_state: None}
    input_map = {initial_state: None}

    queue = deque()
    queue.append((initial_state, 0, initial_monitor))

    return visited, parent_map, input_map, queue


def monitor_key(monitor):
    """
    Creates a hashable representation of the monitor state for BFS tracking.
    Includes active obligations and their counters.
    """
    return (
        tuple(sorted(monitor.active.items())),
        tuple(sorted(monitor.counter.items()))
    )


# TRANSITION EXECUTION =================================================================================================

def process_transition(state, inputs, monitor):
    """
    Executes one transition:
    - Calls step()
    - Clones and updates the liveness monitor
    Returns next_state, outputs, and updated monitor.
    """
    next_state, heat_on, cool_on = step(state, inputs)
    next_monitor = monitor.clone()
    return next_state, heat_on, cool_on, next_monitor

def should_explore_state(next_key, visited):
    """
    Checks if a state + monitor combination has been visited.
    """
    return next_key not in visited


# PROPERTY CHECKING ====================================================================================================

def check_properties(state, next_state, inputs, heat_on, cool_on, monitor):
    """
    Evaluates safety and liveness properties.
    Returns (violation_type, property_name) if violated, otherwise (None, None).
    """
    safety_ok, safety_name = passed_safety_checks(state, next_state, heat_on, cool_on, inputs)
    if not safety_ok:
        return "safety", safety_name

    liveness_ok, liveness_name = passed_liveness_checks(monitor, state, next_state, inputs)
    if not liveness_ok:
        return "liveness", liveness_name

    return None, None


def passed_safety_checks(state: State, next_state: State, heat_on, cool_on, inputs: Input):
    """
    Evaluates all safety properties.
    Returns (True, None) if all hold, otherwise (False, violated_property).
    """
    if not no_simultaneous_heat_cool(heat_on, cool_on):
        return False, "S1"

    if not no_heat_cool_when_off(heat_on, cool_on, state):
        return False, "S2"

    if not timer_expiration_turns_off(state, next_state, inputs.new_mode_cmd):
        return False, "S3"

    if not turn_off_at_setpoint(state, next_state, inputs):
        return False, "S4/S5"

    if not selected_mode_updates_correctly(next_state, inputs.new_mode_cmd):
        return False, "S6"

    return True, None


def passed_liveness_checks(liveness_monitor, state: State, next_state: State, inputs: Input):
    """
    Evaluates all liveness properties.
    Returns (True, None) if none are violated, otherwise (False, violated_property).
    """
    if not liveness_monitor.heat_mode_updates_correctly(state):
        return False, "L1"

    if not liveness_monitor.cool_mode_updates_correctly(state):
        return False, "L2"

    if not liveness_monitor.heating_increases_temperature(state, next_state):
        return False, "L3"

    if not liveness_monitor.cooling_decreases_temperature(state, next_state):
        return False, "L4"

    if not liveness_monitor.eventually_reach_setpoint(state, next_state):
        return False, "L5"

    if not liveness_monitor.mode_becomes_selected_mode(state, next_state, inputs):
        return False, "L6"

    return True, None

# VIOLATION HANDLING ===================================================================================================

def handle_violation(violation_type, name, state, next_state, inputs, parent_map, input_map):
    """
    Prints violation details and reconstructs the counterexample trace.
    """
    print(f"\n{name} violated")

    if violation_type == "safety":
        print("Violating transition:")
        print("state:", state)
        print("input:", inputs)
        print("next_state:", next_state)
        trace = reconstruct_trace(parent_map, input_map, state)
    else:
        trace = reconstruct_trace(parent_map, input_map, next_state)

    print_trace(trace)


# BFS MODEL CHECK ======================================================================================================

def bfs_model_check(initial_state: State, generate_inputs_fn, max_depth: int = 10):
    """
    Runs BFS model checking using a provided input generator.
    Explores state space while tracking liveness obligations.
    Returns counterexample trace if violation found.
    """
    visited, parent_map, input_map, queue = initialize_bfs(initial_state)

    while queue:
        state, depth, monitor = queue.popleft()

        if depth >= max_depth:
            continue

        for inputs in generate_inputs_fn(state):
            next_state, heat_on, cool_on, next_monitor = process_transition(state, inputs, monitor)

            update_trace_maps(parent_map, input_map, state, next_state, inputs)

            violation_type, name = check_properties(state, next_state, inputs, heat_on, cool_on, next_monitor)

            if violation_type:
                handle_violation(violation_type, name, state, next_state, inputs, parent_map, input_map)
                trace = reconstruct_trace(parent_map, input_map, next_state)
                return trace

            next_key = (next_state, monitor_key(next_monitor))

            if next_key not in visited:
                visited.add(next_key)
                queue.append((next_state, depth + 1, next_monitor))

    print("No violations found up to depth:", max_depth)
    return None




