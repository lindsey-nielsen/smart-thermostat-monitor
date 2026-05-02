# Smart Thermostat Runtime Monitor
Interactive dashboard for visualizing smart thermostat behavior through simulation traces and verifying safety and liveness properties.

## Overview & Purpose
This project models a smart thermostat as a cyber-physical system and provides a React-based dashboard to step through its execution. You can explore how inputs affect system state over time, compare correct and faulty behaviors, and identify when properties pass or fail. This project demonstrates runtime monitoring and verification of a cyber-physical system by making system behavior visible and easy to analyze.

## Deployment
This application is deployed on GitHub Pages and can be accessed at: 
https://lindsey-nielsen.github.io/smart-thermostat-monitor/

## Features
- Step through simulation traces tick-by-tick
- Multiple scenarios (normal + faulty behavior)
- Visual thermostat display (temperature, mode, setpoint)
- Safety and liveness property checks with pass/fail indicators
- Trace table with highlighted current step

## Navigation
The navigation bar at the top of the application allows you to switch between different system models:
- Correct → Displays the expected, fully working thermostat behavior
- Buggy Temp → Shows a model with temperature-related faults
- Buggy Mode → Shows a model with issues in mode switching or timer logic

When you switch between these views:
- The application loads a different set of simulation traces
- Resets scenario and tick to the start
- Highlights the active view

## Python Model (Generating Traces)
The `python/` folder contains the system model, monitors, and scenarios used to generate the trace files.

To switch between correct and buggy behavior:
- Update the system logic in `thermostat.py`. The `step` function controls how the system evolves, and you can introduce faults by adjusting parameters to call buggy variants of the logic.
- In `main.py`, set the `folder` variable in `export_trace` to choose where the generated traces will be saved.
- Run `main.py` to regenerate traces, which will be exported as JSON files to the selected folder.

Example:
```
cd python
python main.py
```

## Project Structure
```
public/
  correct_behavior/   # normal traces
  buggy_temp/         # temperature faults
  buggy_mode/         # mode/timer faults

python/               # system model + trace generation
  main.py
  thermostat.py
  monitors.py
  scenarios.py

src/
  components/         # UI panels (state, input, output, checks)
  App.js              # main app logic

```

## Running the App
```
npm install
npm start
```
