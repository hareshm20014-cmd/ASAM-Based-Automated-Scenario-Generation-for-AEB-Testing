from scenariogeneration import xosc
from Parser import ScenarioSchema 
from scenariogeneration import prettyprint

def ScenarioBuild(Scenario: ScenarioSchema, xodr_path: str ,outputpath: str)-> None :
    
    road_network = xosc.RoadNetwork(roadfile=xodr_path)  #....Linking the xodr file to xosc 

    bb = xosc.BoundingBox(2.0, 5.0, 1.8, 2.0, 0.0, 0.9) #...bounding box 
    fa = xosc.Axle(0.523, 0.8, 1.68, 2.98, 0.4)
    ba = xosc.Axle(0.523, 0.8, 1.68, 0.0, 0.4)
    Ego_Vehicle = xosc.Vehicle('car_white', xosc.VehicleCategory.car, bb, fa, ba, 20, 10, 10,model3d='car_white.osgb' )

    Traffic_Vehicle = xosc.Vehicle('car_red', xosc.VehicleCategory.car, bb, fa, ba, 20, 10, 10,model3d='car_red.osgb' )


    entities = xosc.Entities()    #....Entities in the scneario ( Container)
    entities.add_scenario_object('Ego', Ego_Vehicle)
    entities.add_scenario_object('Traffic', Traffic_Vehicle)

    #......Initial condition for Ego Vehicle .....
    init = xosc.Init()  
    ego_speed = xosc.AbsoluteSpeedAction(
        Scenario.Ego.velocity,
        xosc.TransitionDynamics(xosc.DynamicsShapes.step, xosc.DynamicsDimension.time, 1.0)
    )
    ego_pos = xosc.TeleportAction(
        xosc.LanePosition(Scenario.Ego.start_x, 0, Scenario.Ego.start_lane, 1)
    )
    init.add_init_action('Ego', ego_speed)
    init.add_init_action('Ego', ego_pos)

    #......Initial condition for Traffic Object 
    traffic_speed = xosc.AbsoluteSpeedAction(
        Scenario.Traffic.velocity,
        xosc.TransitionDynamics(xosc.DynamicsShapes.step, xosc.DynamicsDimension.time, 1.0)
    )
    traffic_pos = xosc.TeleportAction(
        xosc.LanePosition(Scenario.Traffic.start_x, 0, Scenario.Traffic.start_lane, 1)
    )
    init.add_init_action('Traffic', traffic_speed)
    init.add_init_action('Traffic', traffic_pos)

    #...Event Trigger 

    ttc_condition = xosc.TimeToCollisionCondition(
        value=Scenario.Metrics.ttc_threshold,
        rule=xosc.Rule.lessThan,
        freespace=True,
        entity='Traffic'
    )
    
    start_trigger = xosc.EntityTrigger(
    'ttc_trigger',            # name
    0,                        # delay
    xosc.ConditionEdge.rising,# conditionedge
    ttc_condition,            # entitycondition
    triggerentity='Ego',      # which entity's state is evaluated against the condition
    triggeringpoint='start'   # optional, defaults to 'start' anyway
)
    
    

    #...defining driving dynamics of the Ego when event triggered....

    brake_action = xosc.AbsoluteSpeedAction(
        0.0,
        xosc.TransitionDynamics(xosc.DynamicsShapes.linear, xosc.DynamicsDimension.rate, Scenario.Metrics.max_dacc)
    )

    event = xosc.Event('brake_event', xosc.Priority.overwrite)
    event.add_trigger(start_trigger)
    event.add_action('brake_action', brake_action)

    #...adding Event to Manuever and Manuever group 
    maneuver = xosc.Maneuver('aeb_maneuver')
    maneuver.add_event(event)

    mangroup = xosc.ManeuverGroup('aeb_mangroup')
    mangroup.add_actor('Ego')   #...Maneuver applied to ego entitiy 
    mangroup.add_maneuver(maneuver)

    #....Act, Story and storyboard 
    act_start = xosc.ValueTrigger('act_start', 0, xosc.ConditionEdge.rising,
                                   xosc.SimulationTimeCondition(0, xosc.Rule.greaterThan))
    act = xosc.Act('aeb_act', act_start)
    act.add_maneuver_group(mangroup)

    story = xosc.Story('aeb_story')
    story.add_act(act)

    #....Simulation time trigger for Storyboard overall...
    stop_trigger = xosc.ValueTrigger(
        'stop_trigger', 0, xosc.ConditionEdge.rising,
        xosc.SimulationTimeCondition(Scenario.Sim.time, xosc.Rule.greaterThan),
        triggeringpoint='stop'
    )

    storyboard = xosc.StoryBoard(init, stop_trigger)
    storyboard.add_story(story)

    full_scenario = xosc.Scenario(
        Scenario.Scenario_Name, 'Haresh', xosc.ParameterDeclarations(),
        entities=entities, storyboard=storyboard,
        roadnetwork=road_network, catalog=xosc.Catalog()
    )
    full_scenario.write_xml(outputpath)