import json
from pydantic import BaseModel, Field 
from pathlib import Path
from enum import Enum # for String constraint 
from typing import Union # to allow function to accept multiple paramerters 


#....define Enum class 

class ToF_Day(str,Enum) :
    DAYLIGHT = "Daylight"

class Weather(str,Enum):
    DRY = "Dry"

#..Define Sub-Models 

class EnvironmentModel(BaseModel):
    time_of_day: ToF_Day = Field(...,alias="Time_Of_day")
    weather: Weather = Field(...,alias="Weather")

class RoadModel(BaseModel):
    length: float = Field(...,alias="Length",gt=0)
    lane: int = Field(...,alias="Lane",ge=1)
    lane_width: float = Field(...,alias="Lane width",gt = 2)
    friction: float = Field(...,alias="friction",gt = 0,le=1)

class EgoVehicleModel(BaseModel):
    start_x: float = Field(...,alias="Start_x")
    start_lane: int = Field(...,alias="Start_Lane")
    velocity : float = Field(...,alias="Velocity",gt=0.0)   

class TrafficModel(BaseModel):
    start_x: float = Field(...,alias="Start_x")
    start_lane: int = Field(...,alias="Start_lane")
    velocity: float = Field(...,alias="Velocity",ge=0.0)   

class SimModel(BaseModel):
    time: float = Field(...,alias="Time",gt=0)

class MetricsModel(BaseModel):
    ttc_threshold: float = Field(..., alias="TTc_Threshold", gt=0)
    max_dacc: float = Field(..., alias="Max_Dacc", ge=0.0)

#...define the Main Base Model 

class ScenarioSchema(BaseModel):
    Scenario_Name: str = Field(...,alias="Scenario_Name")
    Environment: EnvironmentModel = Field(...,alias="Environment")
    Road: RoadModel = Field(...,alias="Road")
    Ego: EgoVehicleModel = Field(...,alias="Ego")
    Traffic: TrafficModel = Field(...,alias="Traffic")
    Sim: SimModel = Field(...,alias="Sim")
    Metrics: MetricsModel = Field(...,alias="Metrics")


def Read_file(file_name: str ) -> dict :
    file = Path(__file__).parent / file_name 

    with open(file, "r") as f:
        data = json.load(f)
        return data



if __name__ == "__main__" :
    read_raw = Read_file("Config.JSON")
    print(ScenarioSchema.model_validate(read_raw))
