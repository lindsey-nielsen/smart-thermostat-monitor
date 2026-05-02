/**
 * TraceTable component for the runtime monitor.
 *
 * Displays the full simulation trace in tabular form.
 * Highlights the currently selected tick and shows
 * key state and output values for each step.
 */

const TraceTable = ({ trace, currentTickIndex }) => {
  if (!trace || trace.length === 0) {
    return <p>No trace available</p>;
  }

  return (
    <section>
      <h2 className="panel-title">Trace Table</h2>

      <table className="trace-table">
        <thead>
          <tr>
            <th>Tick</th>
            <th>Mode</th>
            <th>Temp</th>
            <th>Setpoint</th>
            <th>Heat</th>
            <th>Cool</th>
          </tr>
        </thead>

        <tbody>
          {trace.map((step, index) => (
            <tr
              key={index}
              className={index === currentTickIndex ? "active-row" : ""}
            >
              <td>{index}</td>
              <td>{step.state.mode}</td>
              <td>{step.state.temp}°F</td>
              <td>{step.state.setpoint}°F</td>
              <td>{step.outputs.heat_on ? "Yes" : "No"}</td>
              <td>{step.outputs.cool_on ? "Yes" : "No"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
};

export default TraceTable;
