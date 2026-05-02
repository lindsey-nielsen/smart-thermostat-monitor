/**
 * LivenessChecksPanel component for the runtime monitor.
 *
 * Displays liveness property results for the current tick.
 * Maps each check ID (L1–L6) to a readable label and shows
 * whether the property is satisfied (pass/fail).
 */

/**
 * Maps liveness property IDs to descriptive labels.
 */
const livenessLabels = {
  L1: "Heating Activates When Needed",
  L2: "Cooling Activates When Needed",
  L3: "Heating Raises Temperature",
  L4: "Cooling Lowers Temperature",
  L5: "Eventually Reaches Target",
  L6: "System Matches User Mode",
};

/**
 * Renders liveness check results with pass/fail indicators.
 */
const LivenessChecksPanel = ({ checks }) => {
  return (
    <section>
      <h2 className="panel-title">System Behavior Checks</h2>

      {Object.entries(checks || {}).map(([key, passed]) => (
        <div className="check-row" key={key}>
          <span className={`check-icon ${passed ? "pass" : "fail"}`}>
            {passed ? "✓" : "✕"}
          </span>
          <span>{livenessLabels[key] || key}</span>
        </div>
      ))}
    </section>
  );
};

export default LivenessChecksPanel;
