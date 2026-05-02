/**
 * StatePanel component for the runtime monitor.
 *
 * Displays the system state at a given tick, including mode,
 * temperature, setpoint, and timer values. Also visualizes
 * temperature using a progress bar.
 */

/**
 * Returns the CSS class for displaying a mode badge.
 */
const getModeClass = (mode) => {
  return `mode-badge mode-${mode.toLowerCase()}`;
};

/**
 * Renders a labeled view of the current or next system state.
 */
const StatePanel = ({ title, state }) => {
  const tempPercent = Math.min(100, Math.max(0, state.temp));

  return (
    <section>
      <h2 className="panel-title">{title}</h2>

      <div className="stat-row">
        <span className="stat-label">Current Mode</span>
        <span className={getModeClass(state.mode)}>{state.mode}</span>
      </div>

      <div className="stat-row">
        <span className="stat-label">User Mode</span>
        <span className={getModeClass(state.selected_mode)}>
          {state.selected_mode}
        </span>
      </div>

      <div className="stat-row">
        <span className="stat-label">Current Temperature</span>
        <span className="stat-value">{state.temp}°F</span>
      </div>

      <div className="temp-bar">
        <div className="temp-fill" style={{ width: `${tempPercent}%` }} />
      </div>

      <div className="stat-row">
        <span className="stat-label">Target Temperature</span>
        <span className="stat-value">{state.setpoint}°F</span>
      </div>

      <div className="stat-row">
        <span className="stat-label">Timer Remaining</span>
        <span className="stat-value">{state.timer}</span>
      </div>

      <div className="stat-row">
        <span className="stat-label">Timer Active</span>
        <span className="stat-value">{state.timer_active ? "Yes" : "No"}</span>
      </div>
    </section>
  );
};

export default StatePanel;
