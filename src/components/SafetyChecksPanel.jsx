/**
 * SafetyChecksPanel component for the runtime monitor.
 *
 * Displays safety property results for the current tick.
 * Maps each safety check ID (S1–S6) to a readable label and
 * indicates whether the property is satisfied (pass/fail).
 */

/**
 * Maps safety property IDs to descriptive labels.
 */
const safetyLabels = {
  S1: "No Simultaneous Heating and Cooling",
  S2: "Off Means No Heating or Cooling",
  S3: "Timer Forces Shutdown",
  "S4/S5": "Stops at Target Temperature",
  S6: "Selected Mode Matches User Command",
};

/**
 * Renders safety check results with pass/fail indicators.
 */
const SafetyChecksPanel = ({ checks }) => {
  return (
    <section>
      <h2 className="panel-title">Safety Checks</h2>

      {Object.entries(checks || {}).map(([key, passed]) => (
        <div className="check-row" key={key}>
          <span className={`check-icon ${passed ? "pass" : "fail"}`}>
            {passed ? "✓" : "✕"}
          </span>
          <span>{safetyLabels[key] || key}</span>
        </div>
      ))}
    </section>
  );
};

export default SafetyChecksPanel;
