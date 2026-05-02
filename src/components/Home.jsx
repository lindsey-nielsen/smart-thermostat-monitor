import ScenarioSelector from "./ScenarioSelector";
import TickControls from "./TickControls";
import InputPanel from "./InputPanel";
import StatePanel from "./StatePanel";
import OutputPanel from "./OutputPanel";
import SafetyChecksPanel from "./SafetyChecksPanel";
import LivenessChecksPanel from "./LivenessChecksPanel";
import ThermostatGraphic from "./ThermostatGraphic";
import TraceTable from "./TraceTable";

/**
 * Home component for the runtime monitor dashboard.
 *
 * Responsible for:
 * - Managing the main layout of the UI
 * - Connecting control components (scenario + tick navigation)
 * - Rendering the current simulation step
 * - Displaying state, inputs, outputs, and property checks
 * - Showing the full trace table
 *
 * This acts as the central view for stepping through traces
 * and observing system behavior over time.
 */

const Home = ({
  modelName,
  selectedScenario,
  setSelectedScenario,
  tick,
  setTick,
  currentTrace,
  currentTick,
}) => {
  return (
    <main className="dashboard">
      <div className="sticky-top">
        <header className="dashboard-header">
          <h1>Runtime Monitor</h1>
          <p>
            <b>{modelName}</b>: Step through simulation traces and monitor
            safety/liveness properties.
          </p>
        </header>

        <section className="control-card">
          <ScenarioSelector
            selectedScenario={selectedScenario}
            setSelectedScenario={setSelectedScenario}
            setTick={setTick}
          />

          <TickControls
            tick={tick}
            setTick={setTick}
            traceLength={currentTrace.length}
          />
        </section>
      </div>
      <div className="content">
        {currentTick && (
          <>
            <section className="top-grid">
              <ThermostatGraphic
                state={currentTick.state}
                input={currentTick.input}
              />
              <OutputPanel outputs={currentTick.outputs} />
            </section>

            <section className="dashboard-grid">
              <StatePanel title="Current State" state={currentTick.state} />
              <InputPanel input={currentTick.input} />
              <StatePanel title="Next State" state={currentTick.next_state} />
            </section>

            <section className="check-grid">
              <SafetyChecksPanel checks={currentTick.safety_checks} />
              <LivenessChecksPanel checks={currentTick.liveness_checks} />
            </section>

            <section className="trace">
              <TraceTable trace={currentTrace} currentTickIndex={tick} />
            </section>
          </>
        )}
      </div>
    </main>
  );
};

export default Home;
