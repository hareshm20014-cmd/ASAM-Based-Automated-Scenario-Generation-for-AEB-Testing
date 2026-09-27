# ASAM-Based Automated Scenario Generation for ADAS Feature

## 🎯 Aim
To build a complete Python pipeline that converts a JSON-defined concrete scenario parameter file into a structured, **ASAM OpenSCENARIO-compliant XML file** for automated scenario-based testing (SBT). The pipeline is designed around an **Autonomous Emergency Braking (AEB)** feature in accordance with **Euro NCAP** guidelines, evaluating specific test metrics within a scenario-based testing workflow.

---

## 🚀 Objectives
* **Data Processing:** Parse, validate, and structure abstract JSON data using Python type-hinting as a concrete scenario input parameter.
* **Architecture Mapping:** Deeply understand and systematically apply the ASAM OpenSCENARIO structural hierarchy: `Storyboard` ➔ `Story` ➔ `Act` ➔ `Maneuver` ➔ `Event` ➔ `Action`.
* **Simulation Design:** Program an open-loop simulation configuration mirroring the Euro NCAP Car-to-Car Rear Stationary (CCRs) scenario profile.
* **DevOps Workflows:** Utilize robust Git-based version control practices for maintaining source scripts.

---

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Core Library:** `scenariogeneration` (Programmatic OpenSCENARIO/OpenDRIVE XML synthesis)
* **Data Layer:** `pydantic` (Data parsing and JSON schema validation models)
* **Simulation Player:** `esmini` (Open-source OpenSCENARIO toolchain used for execution player and data visualization)

---

## 📁 Project Structure
```text
ASAM OpenSCENARIO Project/
├── src/
│   ├── Config.JSON            # Scenario input parameters (speeds, conditions, constraints)
│   ├── main.py                # Core runtime script orchestrating the full pipeline execution
│   ├── parser.py              # Schema ingestion engine featuring Pydantic verification
│   ├── build_road.py          # Abstract geometry builder exporting .xodr maps
│   ├── build_scenario.py      # Actor lifecycle generator exporting .xosc timelines
│   └── run_esmini.py          # Wrapper utility invoking the esmini simulator binary
├── outputs/
│   ├── aeb_ccrs_basic.xodr    # Validated OpenDRIVE geometric road network output
│   └── aeb_ccrs_basic.xosc    # Validated OpenSCENARIO behavior control output
├── image.png                  # ODD definition diagram 
├── image-1.png                # OpenSCENARIO hierarchical storyboard layout
├── esmini--oscaeb_ccrs_basic.xosc....gif  # Recorded esmini simulation runtime loop
├── requirements.txt           # Declared system and Python environment package lists
└── README.md                  # System instruction documentation
```

---

## 🚘 ADAS Scenario Context (Euro NCAP CCRs)
An **Advanced Emergency Braking (AEB)** feature was selected to explore code-driven OpenSCENARIO creation workflows. The system maps out the exact **Operational Design Domain (ODD)** configurations defining a *Car-to-Car Rear Stationary (CCRs)* collision case following standardized testing protocol blueprints published by Euro NCAP.

![ODD Definition Diagram](./image.png)

*The exact environmental variables and threshold velocities are dynamically ingested from the `src/Config.JSON` configuration schema.*

---

## 📐 ASAM OpenSCENARIO Framework Integration
The OpenSCENARIO standard dictates a strict `Storyboard` structure to programmatically govern actor interactions during runtime testing sweeps. The pipeline implements the architectural paradigm pioneered during the **PEGASUS** project:

![OpenSCENARIO Storyboard Structure](./image-1.png)

### Workflow Lifecycle
1. **Geometric Foundations:** The system generates a high-fidelity static road map matching `OpenDRIVE (.xodr)` format expectations using `Build_Road.py`.
2. **Dynamic Behavior Engines:** The programmatic modules in `Build_Scenario.py` assemble behavioral parameters (`storyboard`, `story`, `act`, `maneuver`, `event`, `action`) to script real-time actor speeds and locations, mapping them directly onto the road.
3. **Validation & Pipeline Ingestion:** The `parser.py` program analyzes, extracts, and maps the static inputs out of `Config.JSON`. While this structure models isolated concrete simulation parameters, it provides standard logic boundaries to scale into randomized programmatic parameter space sweeps using constraint randomization or Bayesian optimization techniques.
4. **Execution & Simulation:** The final pipeline script (`main.py`) ties all separate formatting subsystems together, passing synthesized programmatic payloads directly to `run_esmini.py` for headless or windowed physics playback.

---

## 📊 Results & Evaluation
![Recorded esmini Simulation Run](./esmini--oscaeb_ccrs_basic.xosc....gif)

The simulation engine assesses whether a programmatic braking profile, triggered at a specified **Time-to-Collision (TTC)** value, holds sufficient kinetic force to safely stop the vehicle ahead of obstacles under given speeds and surface friction boundaries. This open-loop setup isolates performance tracking on basic vehicular kinematics rather than processing sensory noise or camera perception models.

* **Simulation Initialization:** The Ego vehicle and the target Traffic node spawn at defined structural coordinates.
* **Ego Velocity Profile:** The platform kicks off initial vehicle dynamics with a baseline velocity of **50 km/h**.
* **Safety Verification:** Emergency braking kinematics actuate precisely when system conditions pass a threshold condition of TTC ≤ 1.5 seconds, decelerating the vehicle safely to rest.

---

## 🔮 Future Scope
* **Multi-Actor Scaling:** Scale environment complexity by adding dynamic pedestrian actors, vulnerable road users (VRUs), and multi-car cut-in traffic logic.
* **Pipeline Automation:** Incorporate CI/CD batch testing automation arrays to programmatically execute continuous massive matrix test generation parameter sweeps.

---

## 📑 Acknowledgments & References
* [ASAM OpenSCENARIO & OpenDRIVE Industry Standards](https://asam.net)
* [esmini OpenSCENARIO Player Repository](https://github.com)
* [scenariogeneration Python Utility documentation](https://github.com)
* [Euro NCAP Official AEB Car-to-Car Testing Guidelines](https://euroncap.com)
