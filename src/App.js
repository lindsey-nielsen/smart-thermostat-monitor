import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import "./App.css";
import Home from "./components/Home";
import Navbar from "./components/Navbar";

/**
 * App component for the runtime monitor.
 *
 * Loads trace files based on the selected model route,
 * manages the selected scenario and tick state, and passes
 * the current trace data into the main dashboard view.
 */

/**
 * Loads all scenario trace files for the current model route.
 */
const loadTraces = async (path) => {
  let folder = "correct_behavior";

  if (path === "/buggy-temp") folder = "buggy_temp";
  if (path === "/buggy-mode") folder = "buggy_mode";

  const files = {
    normal_heat: `/${folder}/normal_heat_trace.json`,
    normal_cooling: `/${folder}/normal_cool_trace.json`,
    timer: `/${folder}/timer_trace.json`,
    setpoint_fault: `/${folder}/setpoint_jump_trace.json`,
    ambient_fault: `/${folder}/unstable_ambient_trace.json`,
    heat_to_cool: `/${folder}/mode_switch_trace.json`,
    user_turn_off: `/${folder}/user_turns_off_trace.json`,
  };

  const results = await Promise.all(
    Object.entries(files).map(async ([key, path]) => {
      const res = await fetch(path);
      const text = await res.text();
      const data = JSON.parse(text);
      return [key, data];
    }),
  );

  return Object.fromEntries(results);
};

/**
 * Returns the display name for the current model route.
 */
const getModelName = () => {
  const path = window.location.pathname;

  if (path === "/buggy-temp") {
    return "Buggy Temperature Model";
  }

  if (path === "/buggy-mode") {
    return "Buggy Mode/Timer Model";
  }

  return "Correct Model";
};

/**
 * Manages trace loading, selected scenario, and current tick state.
 */
function App() {
  const [traces, setTraces] = useState({});
  const [selectedScenario, setSelectedScenario] = useState("normal_heat");
  const [tick, setTick] = useState(0);
  const location = useLocation();

  useEffect(() => {
    setTick(0);
    setSelectedScenario("normal_heat");

    loadTraces(location.pathname).then(setTraces);
  }, [location.pathname]);

  const currentTrace = traces[selectedScenario] || [];
  const currentTick = currentTrace[tick] || null;

  console.log("Current tick:", currentTick);
  console.log("Liveness checks:", currentTick?.liveness_checks);

  return (
    <>
      <Navbar />
      <Home
        modelName={getModelName()}
        selectedScenario={selectedScenario}
        setSelectedScenario={setSelectedScenario}
        tick={tick}
        setTick={setTick}
        currentTrace={currentTrace}
        currentTick={currentTick}
      />
    </>
  );
}

export default App;
