from Parser import ScenarioSchema, Read_file
from Build_Road import RoadNetwork
from Build_Scenario import ScenarioBuild
import json
from Run import run_esmini

if __name__ == "__main__":
    raw = Read_file("Config.JSON")
    scenario = ScenarioSchema.model_validate(raw)

    xodr_path = "outputs/aeb_ccrs_basic.xodr"
    xosc_path = "outputs/aeb_ccrs_basic.xosc"
    esmini_exe = r"D:/esmini/bin/esmini.exe"

    RoadNetwork(scenario, xodr_path)
    ScenarioBuild(scenario, xodr_path, xosc_path)
    run_esmini(esmini_exe, xosc_path)

    print(f"Generated: {xodr_path} and {xosc_path} for '{scenario.Scenario_Name}'")
    print(f"Full pipeline complete for '{scenario.Scenario_Name}'")
   