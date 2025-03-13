
# =============== EXAMPLES ===================

# ======================== Example 0 =============================

# example_question_0 = "-Inference : xhz|hasBrother|okm / Justifications : xhz|isA|Human, xhz|hasSilbing|okm, okm|isA|Man."
# example_rule_0 = "\n -Rule : Human(?a), hasSilbing(?a,?b), Man(?b) -> hasBrother(?a, ?b)."
# example_answer_0 =  "Let's translate. translation is the human is xhz's brother because he is a man and his sibling."
# example_0 = (example_question_0, example_answer_0, example_rule_0)

# ======================== Example 1 =============================

example_question_1 = "-Inference : prth|canSpeakWith|dzkl \n -Justifications : prth|Type|Robot, prth|hasCapability|stkl, stkl|Type|VerbalCommunicationCapability, dzkl|Type|Human, dzkl|hasDisposition|szom, szom|Type|VerbalCommunicationDisposition, (isInFrontOf o hasAgentSeatedOn)|SubPropertyOf|isFacing, prth|isInFrontOf|hoilgq, hoilgq|hasAgentSeatedOn|dzkl, dzkl|isAvailable|boolean#true."                    
example_rule_1 = "\n -Rule : Robot(?r), hasCapability(?r,?c), VerbalCommunicationCapability(?c), Human(?a), hasDisposition(?a, ?d), VerbalCommunicationDisposition(?d), isFacing(?r,?a), isAvailable(?a, boolean#true) -> canSpeakWith(?r, ?a)."
example_answer_1=  "Let's translate. translation is the robot can speak with the human because it has a verbal communication capability, the human is available and has a reciprocal disposition for verbal communication. Additionally, the robot is in front of an object that has the human seated on it, ensuring that it is facing the human."
example_1 = (example_question_1, example_answer_1, example_rule_1)

# ======================== Question 2 =============================
#example_question_2 = "-Inference : car_1|canBeTowedBy|truck_1 \n -Justifications : truck_1|Type|Vehicle, truck_1|hasCapability|truck_1_capa, truck_1_capa|Type|TowingCapability, car_1|Type|Car, Car|SubClassOf|Towable, Towable|EquivalentTo|(isTowableBy some Vehicle), car_1|hasWeight|integer#2000, truck_1|hasTowingCapacity|integer#3000."
example_question_2 = "-Inference : idkle|canBeTowedBy|dowz \n -Justifications : dowz|Type|Vehicle, dowz|hasCapability|plmea, plmea|Type|TowingCapability, idkle|Type|Car, Car|SubClassOf|Towable, Towable|EquivalentTo|(isTowableBy some Vehicle), idkle|hasWeight|integer#2000, dowz|hasTowingCapacity|integer#3000."
example_rule_2 = "\n -Rule : Vehicle(?v), hasCapability(?v,?c), TowingCapability(?c), Towable(?o), hasWeight(?o,?w1), hasTowingCapacity(?v,?w2), greaterThan(?w2,?w1) -> canBeTowedBy(?o,?v)"
example_answer_2=  "Let's translate. translation is the truck can tow the car because it has a towing capability with sufficient capacity, and the car is a towable object with a weight within the truck's towing capacity."
example_2 = (example_question_2, example_answer_2, example_rule_2)

# ======================== Question 3 =============================
#example_question_3 = "-Inference : drone_1|canInspect|bridge_1 \n -Justifications : drone_1|Type|Drone, drone_1|hasCapability|drone_1_capa, AerialInspectionCapability|EquivalentTo|((hasCamera min 1 SecurityCamera) and (hasCapability some FlyingCapability)), drone_1|hasCamera|cam_1, cam_1|Type|SecurityCamera, drone_1_capa|Type|FlyingCapability, bridge_1|Type|Bridge, Bridge|SubClassOf|Inspectable, bridge_1|hasHeight|integer#100, drone_1|hasMaxInspectionHeight|integer#200" #, greaterThan(integer#200, integer#100)."
example_question_3 = "-Inference : tlws|canInspect|sqkj \n -Justifications : tlws|Type|Drone, tlws|hasCapability|qsab, AerialInspectionCapability|EquivalentTo|((hasCamera max 2 SecurityCamera) and (hasCapability some FlyingCapability)), tlws|hasCamera|mq, mq|Type|SecurityCamera, qsab|Type|FlyingCapability, sqkj|Type|Bridge, Bridge|SubClassOf|Inspectable, sqkj|hasHeight|integer#100, tlws|hasMaxInspectionHeight|integer#200."
example_rule_3 = "\n -Rule : Drone(?d), hasCapability(?d,?c), AerialInspectionCapability(?c), Inspectable(?o), hasHeight(?o,?h1), hasMaxInspectionHeight(?d,?h2), greaterThan(?h2,?h1) -> canInspect(?d,?o)"
example_answer_3=  "Let's translate. translation is the the drone can inspect the bridge because it has an aerial inspection capability based on having at least one security camera and the capability to fly. The bridge is considered inspectable, and the drone's maximum inspection height is greater than the height of the bridge."
example_3 = (example_question_3, example_answer_3, example_rule_3)

# ======================== Question 4 =============================
#example_question_4 = "-Inference : robot_3|canChargeAt|station_1 \n -Justifications : robot_3|Type|DeliveryRobot, robot_3|hasCapability|robot_3_capa, robot_3_capa|EquivalentTo|(isCapabilityOf some (hasComponent some ChargingConnector), station_1|Type|ChargingStation, station_1|hasPort|port_1, port_1|Type|ChargingConnector, station_1|isPowered|boolean#true, robot_3|hasBatteryLevel|integer#15, robot_3|hasBatteryThresholdForCharging|integer#20), robot_3|hasChargingConnector|charging_connector_3, charging_connector_3|hasType|string#USB-Type-C, port_1|hasType|string#USB-Type-C."
example_question_4 = "-Inference : flordlk|canChargeAt|deljyom \n -Justifications : flordlk|Type|DeliveryRobot, flordlk|hasCapability|dmpolszf, dmpolszf|EquivalentTo|(isCapabilityOf some (hasComponent exactly 1 ChargingConnector), deljyom|Type|ChargingStation, deljyom|hasPort|szeo, szeo|Type|ChargingConnector, deljyom|isPowered|boolean#true, flordlk|hasBatteryLevel|integer#15, flordlk|hasBatteryThresholdForCharging|integer#20), flordlk|hasChargingConnector|duipm, duipm|hasType|string#USB-Type-C, szeo|hasType|string#USB-Type-C."                     
example_rule_4 = "\n -Rule : DeliveryRobot(?r), hasCapability(?r,?c), ChargingCapability(?c), ChargingStation(?s), hasPort(?s,?p), ChargingConnector(?p), isPowered(?s,boolean#true), hasBatteryLevel(?r,?b1), hasBatteryThresholdForCharging(?r,?b2), lesserThan(?b1,?b2), hasChargingConnector(?r,?c1), hasType(?c1,?t1), hasType(?p,?t2), equal(?t1,?t2) -> canChargeAt(?r,?s)."
example_answer_4=  "Let's translate. translation is the delivery robot can charge at the station because it has a charging capability thanks to its charging connector which is compatible with the station's port, the station being powered, and the robot's battery level being below its charging threshold."
example_4 = (example_question_4, example_answer_4, example_rule_4)


# example_question_2 = "S: inference = pepper|canSpeakWith|agent_0 / Justifications = pepper|isA|Robot, pepper|hasCapability|pepper_capa, \
#                     pepper_capa|isA|VerbalCommunicationCapability, agent_0|isA|Human, agent_0|hasDisposition|agent_0_disp,\
#                     agent_0_disp|isA|VerbalCommunicationDisposition, pepper|isNear|agent_0, agent_0|isInFrontOf|pepper, agent_0|isAvailable|boolean#true."
                    
# example_rule_2 = "The used rule was : Robot(?r), hasCapability(?r,?c), VerbalCommunicationCapability(?c), Human(?a), hasDisposition(?a, ?d), \
#                   VerbalCommunicationDisposition(?d), isNear(?r,?a), isInFrontOf(?a,?r), isAvailable(?a, boolean#true)  -> canSpeakWith(?r, ?a)."
                  
# example_answer_2=  "A: Let's translate. translation is pepper can speak with agent_0 because it has the capability to communicate verbally and agent_0\
#                     has the disposition for verbal communication, and both agents are close to each other."
# example_2 = (example_question_2.replace('\t', ''), example_answer_2.replace('\t', ''), example_rule_2.replace('\t', ''))

example_rdf_question_1 = "Inference : pepper|hasGraspingAffordance|mug_1_handle / Justifications : Handle|SubClassOf|Object, mug_1_handle_disp|Type|Graspable, \
                        pepper_left_gripper|hasOpeningWidth|30, pepper_capa|Type|Graspable, pepper|hasGripper|pepper_left_gripper, Robot|SubClassOf|Agent \
                        mug_1_handle|hasWidth|5, pepper|Type|Robot, pepper|hasCapability|pepper_capa, mug_1_handle|Type|Handle, mug_1_handle|hasDisposition|mug_1_handle_disp."
                    
example_rdf_rule_1 = "\n-Rule : Agent(?a), Object(?o), hasCapability(?a, ?c), Grasping(?c), hasDisposition(?o, ?d), Graspable(?d), hasGripper(?a, ?g), hasOpeningWidth(?g, ?w1), hasWidth(?o, ?w2), greaterThan(?w1, ?w2) -> hasGraspingAffordance(?a, ?o)."
                  
#example_answer_1=  "A: Let's translate. translation is prth can speak with dzkl because it has the capability to communicate verbally and dzkl has the disposition for verbal communication, and both agents are close to each other."
example_rdf_answer_1=  "A: Let's translate. translation is the pepper robot has a grasping affordance towards mug_1's handle because it is graspable, its width fits pepper's gripper opening width, and it has a grasping capability.."
example_rdf_1= (example_rdf_question_1, example_rdf_answer_1, example_rdf_rule_1)

example_onto_question_1 = "S: inference = pepper|hasGraspingAffordance|mug_1_handle / Justifications = Handle|isA|Object, mug_1_handle_disp|isA|Graspable, \
                        pepper_left_gripper|hasOpeningWidth|30, pepper_capa|isA|Graspable, pepper|hasGripper|pepper_left_gripper, Robot|isA|Agent \
                        mug_1_handle|hasWidth|5, pepper|isA|Robot, pepper|hasCapability|pepper_capa, mug_1_handle|isA|Handle, mug_1_handle|hasDisposition|mug_1_handle_disp."
                    
example_onto_rule_1 = "\n-Rule : Agent(?a), hasCapability(?a, ?c), Grasping(?c), hasGripper(?a, ?g), hasOpeningWidth(?g, ?w1), Object(?o), hasDisposition(?o, ?d), Graspable(?d), hasWidth(?o, ?w2), greaterThan(?w1, ?w2) -> hasGraspingAffordance(?a, ?o)."
                  
#example_answer_1=  "A: Let's translate. translation is prth can speak with dzkl because it has the capability to communicate verbally and dzkl has the disposition for verbal communication, and both agents are close to each other."
example_onto_answer_1=  "A: Let's translate. translation is the pepper robot has a grasping affordance towards mug_1's handle because it is graspable, its width fits pepper's gripper opening width, and it has a grasping capability.."
example_onto_1= (example_rdf_question_1, example_rdf_answer_1, example_rdf_rule_1)