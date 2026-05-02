/**
 * ThermostatGraphic component for the runtime monitor.
 *
 * Provides a visual representation of the thermostat state,
 * including current temperature, target setpoint, ambient temperature,
 * and active mode (heating, cooling, or off).
 */

/**
 * Returns a simplified mode class for styling the thermostat.
 */
const ThermostatGraphic = ({ state, input }) => {
  const temp = state.temp;
  const setpoint = state.setpoint;
  const mode = state.mode;
  const ambientTemp = input?.ambient_temp;

  const getModeClass = (mode) => {
    const m = (mode || "off").toLowerCase();

    if (m === "heat") return "heat";
    if (m === "cool") return "cool";

    return "off";
  };

  const modeClass = getModeClass(mode);

  return (
    <section className={`thermostat-card ${modeClass}`}>
      <h2>Thermostat</h2>

      <div className="thermostat-circle">
        <div className="temp">{temp}°F</div>
        <div className="setpoint">Target: {setpoint}°F</div>
        <div className="ambient">Ambient: {ambientTemp}°F</div>
      </div>

      <div className="mode-pill">
        {mode === "HEAT" && "🔥 Heating"}
        {mode === "COOL" && "❄️ Cooling"}
        {mode === "OFF" && "⏸ Off"}
      </div>
    </section>
  );
};

export default ThermostatGraphic;
