/**
 * OutputPanel component for the runtime monitor.
 *
 * Displays the system's output signals at the current tick,
 * specifically whether heating or cooling is active.
 */

const OutputPanel = ({ outputs }) => {
  return (
    <section>
      <h2 className="panel-title">System Output</h2>

      <div className="stat-row">
        <span className="stat-label">Heating Active</span>
        <span className="stat-value">{outputs.heat_on ? "Yes" : "No"}</span>
      </div>

      <div className="stat-row">
        <span className="stat-label">Cooling Active</span>
        <span className="stat-value">{outputs.cool_on ? "Yes" : "No"}</span>
      </div>
    </section>
  );
};

export default OutputPanel;
