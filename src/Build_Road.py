from scenariogeneration import xodr
from Parser import ScenarioSchema  # ...only needeed for type hinting.

def RoadNetwork(Scenario: ScenarioSchema, output_path: str) -> None :
    planview = xodr.PlanView() #...............Represents 2D centerline segments as geometries 
    planview.add_geometry(xodr.Line(Scenario.Road.length))

    Lanes = xodr.Lanes() #.....................Container for Lanes 
    Lane_section = xodr.LaneSection(0,xodr.standard_lane(Scenario.Road.lane_width))
    for i in range(Scenario.Road.lane):
        Lane_section.add_right_lane(xodr.standard_lane(Scenario.Road.lane_width))
    Lanes.add_lanesection(Lane_section)
    road = xodr.Road(1, planview, Lanes)    #............Bundles all into Road , Road iD =1 

    #.....Assembly of OPENDrive components....

    odr = xodr.OpenDrive(Scenario.Scenario_Name)  #....initialize the opendrive
    odr.add_road(road)
    odr.adjust_roads_and_lanes()  #....Auto computes geometry maths for linking 

    odr.write_xml(output_path)    #...Writing to the file 

