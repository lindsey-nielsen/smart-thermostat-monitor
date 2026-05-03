import json
from thermostat import Mode, State, step
from monitors import (
    LivenessMonitor,
    no_simultaneous_heat_cool,
    no_heat_cool_when_off,
    timer_expiration_turns_off,
    turn_off_at_setpoint,
    selected_mode_updates_correctly
)
from model_check import (
    bfs_model_check,
    generate_inputs_for_safety,
    generate_inputs_for_cooling_liveness,
    generate_inputs_for_heating_liveness,
)
from scenarios import (
    normal_heating_scenario,
    normal_cooling_scenario,
    timer_scenario,
    fault_setpoint_jump_scenario,
    fault_unstable_ambient_scenario,
    mode_switch_heat_to_cool_scenario,
    user_turns_off_scenario
)

"""
Runs simulations and model checking for the smart thermostat.

This file executes predefined scenarios to observe system behavior over time,
including safety and liveness properties. It also runs BFS-based model checking
to systematically explore possible states and detect violations.

The goal is to validate both normal and faulty behaviors of the thermostat
through simulation traces and exhaustive state exploration.
"""


# INITIALIZATION =======================================================================================================

def initial_state():
    """
    Creates and returns the default starting state of the thermostat.
    """
    return State(
        mode=Mode.OFF,
        selected_mode=Mode.OFF,
        temp=70,
        setpoint=70,
        timer=0,
        timer_active=False,
    )


# STATE / INPUT FORMATTING =============================================================================================

def state_to_dict(state):
    """
    Creates and returns the default starting state of the thermostat.
    """
    return {
        "mode": state.mode.name,
        "selected_mode": state.selected_mode.name,
        "temp": state.temp,
        "setpoint": state.setpoint,
        "timer": state.timer,
        "timer_active": state.timer_active,
    }


def input_to_dict(inputs):
    """
    Converts an Inputs object into a dictionary for logging/export.
    """
    return {
        "new_mode_cmd": inputs.new_mode_cmd.name if inputs.new_mode_cmd else None,
        "new_setpoint": inputs.new_setpoint if inputs.new_setpoint else None,
        "timer_set": inputs.timer_set if inputs.timer_set else None,
        "ambient_temp": inputs.ambient_temp
    }


def bfs_trace_to_dict(trace):
    """
    Converts BFS trace (State, Input) tuples into JSON-serializable format.
    """
    result = []

    for i, (state, input_used) in enumerate(trace):
        result.append({
            "step": i,
            "state": state_to_dict(state),
            "input": input_to_dict(input_used) if input_used else None
        })

    return result


# PROPERTY CHECKING ====================================================================================================

def run_liveness_checks(monitor, state, next_state, inputs):
    """
    Runs all liveness property checks and returns their results.
    """
    return {
        "L1": monitor.heat_mode_updates_correctly(state),
        "L2": monitor.cool_mode_updates_correctly(state),
        "L3": monitor.heating_increases_temperature(state, next_state),
        "L4": monitor.cooling_decreases_temperature(state, next_state),
        "L5": monitor.eventually_reach_setpoint(state, next_state),
        "L6": monitor.mode_becomes_selected_mode(state, next_state, inputs),
    }


def run_safety_checks(state, next_state, inputs, heat_on, cool_on):
    """
    Runs all safety property checks and returns their results.
    """
    return {
        "S1": no_simultaneous_heat_cool(heat_on, cool_on),
        "S2": no_heat_cool_when_off(heat_on, cool_on, state),
        "S3": timer_expiration_turns_off(state, next_state, inputs.new_mode_cmd),
        "S4/S5": turn_off_at_setpoint(state, next_state, inputs),
        "S6": selected_mode_updates_correctly(next_state, inputs.new_mode_cmd)
    }


# SIMULATION ===========================================================================================================

def run_simulation(name, scenario):
    """
    Executes a simulation for a given scenario and records a trace of states,
    inputs, outputs, and property checks at each step.
    """
    state = initial_state()
    trace = []
    monitor = LivenessMonitor()

    print(f"\n=== {name} ===")
    print("Initial state:", state)

    for tick, inputs in enumerate(scenario, start=0):
        next_state, heat_on, cool_on = step(state, inputs)

        safety_checks = run_safety_checks(state, next_state, inputs, heat_on, cool_on)
        liveness_checks = run_liveness_checks(monitor, state, next_state, inputs)

        trace.append({
            "tick": tick,
            "state": state_to_dict(state),
            "input": input_to_dict(inputs),
            "outputs": {
                "heat_on": heat_on,
                "cool_on": cool_on,
            },
            "next_state": state_to_dict(next_state),
            "safety_checks": safety_checks,
            "liveness_checks": liveness_checks
        })

        print(f"\nTick {tick}")
        print("Input:", inputs)
        print("State:", state)
        print("Outputs: heat_on =", heat_on, ", cool_on =", cool_on)
        print("Next state:", next_state)
        print("Safety Checks:", safety_checks)
        print("Liveness Status:", liveness_checks)

        state = next_state

    return trace


# TRACE EXPORT =========================================================================================================

def export_trace(filename, trace):
    """
    Saves the simulation trace to a JSON file.
    """

    # change folder depending on which model is used (correct_behavior, buggy_temp, or buggy_mode)
    folder = "correct_behavior"

    with open(f"../public/{folder}/{filename}", "w") as f:
        json.dump(trace, f, indent=4)


# MODEL CHECKING =======================================================================================================

def run_model_check():
    """
    Runs BFS model checking from an initial state.
    Exports counterexample trace to JSON file
    """
    print("\n=== BFS Model Check ===")

    print("\nSafety Checks")
    trace = bfs_model_check(initial_state(), generate_inputs_for_safety, max_depth=3)
    if trace:
        export_trace("bfs_safety_trace.json", bfs_trace_to_dict(trace))

    print("\nHeating Liveness Checks")
    trace = bfs_model_check(initial_state(), generate_inputs_for_heating_liveness, max_depth=7)
    if trace:
        export_trace("bfs_heating_trace.json", bfs_trace_to_dict(trace))

    print("\nCooling Liveness Checks")
    trace = bfs_model_check(initial_state(), generate_inputs_for_cooling_liveness, max_depth=7)
    if trace:
        export_trace("bfs_cooling_trace.json", bfs_trace_to_dict(trace))


# MAIN EXECUTION =======================================================================================================

def main():
    """
    Runs all predefined scenarios, exports their traces, and performs model checking.
    """
    normal_heat_trace = run_simulation("Normal Heating Scenario", normal_heating_scenario())
    normal_cool_trace = run_simulation("Normal Cooling Scenario", normal_cooling_scenario())
    timer_trace = run_simulation("Timer Scenario", timer_scenario())
    setpoint_jump_trace = run_simulation("Fault: Setpoint Jump Scenario", fault_setpoint_jump_scenario())
    unstable_ambient_trace = run_simulation("Fault: Unstable Ambient Temperature Scenario", fault_unstable_ambient_scenario())
    mode_switch_trace = run_simulation("Mode Switch From Heating to Cooling Scenario", mode_switch_heat_to_cool_scenario())
    user_turns_off_trace = run_simulation("User Turns Off Scenario", user_turns_off_scenario())

    export_trace("normal_heat_trace.json", normal_heat_trace)
    export_trace("normal_cool_trace.json", normal_cool_trace)
    export_trace("timer_trace.json", timer_trace)
    export_trace("setpoint_jump_trace.json", setpoint_jump_trace)
    export_trace("unstable_ambient_trace.json", unstable_ambient_trace)
    export_trace("mode_switch_trace.json", mode_switch_trace)
    export_trace("user_turns_off_trace.json", user_turns_off_trace)

    run_model_check()


if __name__ == "__main__":
    main()