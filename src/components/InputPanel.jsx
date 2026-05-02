/**
 * InputPanel component for the runtime monitor.
 *
 * Responsible for displaying all user-provided inputs at the current tick,
 * including mode changes, setpoint updates, timer values, and ambient temperature.
 * Also formats visual styling for mode values using helper logic.
 */

/**
 * Displays all user inputs applied at the current tick.
 * Includes mode changes, setpoint updates, timer, and ambient temp.
 */
const getModeClass = (mode) => {
  if (!mode || mode === "None") {
    return "mode-badge mode-none";
  }

  return `mode-badge mode-${mode.toLowerCase()}`;
};

/**
 * Displays all user inputs applied at the current tick.
 * Includes mode changes, setpoint updates, timer, and ambient temp.
 */
const InputPanel = ({ input }) => {
  return (
    <section>
      <h2 className="panel-title">User Input</h2>

      <div className="stat-row">
        <span className="stat-label">Mode Change</span>
        <span className={getModeClass(input.new_mode_cmd)}>
          {input.new_mode_cmd ?? "None"}
        </span>
      </div>
      <div className="stat-row">
        <span className="stat-label">Set Temperature</span>
        <span className="stat-value">
          {input.new_setpoint ? `${input.new_setpoint}°F` : "None"}
        </span>
      </div>

      <div className="stat-row">
        <span className="stat-label">Set Timer</span>
        <span className="stat-value">{input.timer_set ?? "None"}</span>
      </div>

      <div className="stat-row">
        <span className="stat-label">Ambient Temperature</span>
        <span className="stat-value">{input.ambient_temp}°F</span>
      </div>
    </section>
  );
};

export default InputPanel;
