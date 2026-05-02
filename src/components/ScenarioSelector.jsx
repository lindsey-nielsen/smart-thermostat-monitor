/**
 * ScenarioSelector component for the runtime monitor.
 *
 * Allows the user to choose a simulation scenario.
 * Updates the selected scenario and resets the tick
 * to the beginning of the trace when changed.
 */

/**
 * Handles scenario selection and resets simulation progress.
 */
const ScenarioSelector = ({
  selectedScenario,
  setSelectedScenario,
  setTick,
}) => {
  const handleChange = (e) => {
    setSelectedScenario(e.target.value);
    setTick(0);
  };

  return (
    <label>
      Select a scenario:
      <span className="select-wrapper">
        <select value={selectedScenario} onChange={handleChange}>
          <option value="normal_heat">Normal Heating</option>
          <option value="normal_cooling">Normal Cooling</option>
          <option value="timer">Timer</option>
          <option value="setpoint_fault">Setpoint Fault</option>
          <option value="ambient_fault">Ambient Temperature Fault</option>
          <option value="heat_to_cool">Heating to Cooling</option>
          <option value="user_turn_off">User Turns Off</option>
        </select>
      </span>
    </label>
  );
};

export default ScenarioSelector;
