/**
 * TickControls component for the runtime monitor.
 *
 * Allows navigation through the simulation trace.
 * Provides previous/next controls and prevents
 * stepping outside valid tick bounds.
 */

/**
 * Handles stepping backward and forward through ticks.
 */
const TickControls = ({ tick, setTick, traceLength }) => {
  const goPrevious = () => {
    setTick((prev) => Math.max(0, prev - 1));
  };

  const goNext = () => {
    setTick((prev) => Math.min(traceLength - 1, prev + 1));
  };

  return (
    <div>
      <button onClick={goPrevious} disabled={tick === 0}>
        Previous
      </button>

      <span> Tick {tick} </span>

      <button onClick={goNext} disabled={tick >= traceLength - 1}>
        Next
      </button>
    </div>
  );
};

export default TickControls;
