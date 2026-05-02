from thermostat import Mode, Input

"""
Defines test scenarios for the smart thermostat.

Each scenario is a sequence of inputs representing different behaviors,
including normal operation and fault conditions. These are used to test
the system and observe safety and liveness properties over time.
"""


# NORMAL OPERATION =====================================================================================================

def normal_heating_scenario():
    """
    Normal heating: system is set to HEAT and should increase temperature toward the setpoint.
    """
    return [
        Input(new_mode_cmd=Mode.HEAT, new_setpoint=72, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
    ]


def normal_cooling_scenario():
    """
    Normal cooling: system is set to COOL and should decrease temperature toward the setpoint.
    """
    return [
        Input(new_mode_cmd=Mode.COOL, new_setpoint=68, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
    ]


def timer_scenario():
    """
    Timer behavior: heating is activated with a timer and should turn off when the timer expires.
    """
    return [
        Input(new_mode_cmd=Mode.HEAT, new_setpoint=75, timer_set=3, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
    ]


# FAULT SCENARIOS ======================================================================================================

def fault_setpoint_jump_scenario():
    """
    Fault scenario: setpoint suddenly increases while heating, testing response to large changes.
    """
    return [
        Input(new_mode_cmd=Mode.HEAT, new_setpoint=70, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=90, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
    ]


def fault_unstable_ambient_scenario():
    """
    Fault scenario: ambient temperature fluctuates rapidly, testing system stability.
    """
    return [
        Input(new_mode_cmd=Mode.HEAT, new_setpoint=72, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=80),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=60),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=85),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=60),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=85),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=60),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=85),
    ]


# USER / MODE CHANGE SCENARIOS =========================================================================================

def mode_switch_heat_to_cool_scenario():
    """
    Mode switch: system transitions from heating to cooling and should update behavior correctly.
    """
    return [
        Input(new_mode_cmd=Mode.HEAT, new_setpoint=72, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=Mode.COOL, new_setpoint=68, timer_set=None, ambient_temp=75),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=75),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=75),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=75),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=75),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=75),
    ]


def user_turns_off_scenario():
    """
    User turns off: system is turned OFF during heating and should stop all activity.
    """
    return [
        Input(new_mode_cmd=Mode.HEAT, new_setpoint=72, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=Mode.OFF, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
        Input(new_mode_cmd=None, new_setpoint=None, timer_set=None, ambient_temp=65),
    ]