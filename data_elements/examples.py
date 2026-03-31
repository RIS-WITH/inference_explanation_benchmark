from data_elements.Example import SubQuestionExample, QuestionExample
# =============== EXAMPLES ===================

# ======================== Example 1 =============================
sub_question_1 = SubQuestionExample(infered_fact="__robot__|isFacing|__human__",
                                    rule="(isInFrontOf o hasAgentSeatedOn)|SubPropertyOf|isFacing",
                                    explanation="__robot__|isInFrontOf|__object__, __object__|hasAgentSeatedOn|__human__",
                                    translation="the robot is in front of an object that has the human seated on it")

question_1 = QuestionExample(infered_fact="__robot__|canSpeakWith|__human__",
                             rule="Robot(?r), hasCapability(?r,?c), VerbalCommunicationCapability(?c), Human(?a),\
                                   hasDisposition(?a, ?d), VerbalCommunicationDisposition(?d), isFacing(?r,?a),\
                                   isAvailable(?a, boolean#true) -> canSpeakWith(?r, ?a)",
                              explanation='''__robot__|Type|Robot, __robot__|hasCapability|__robot_capa__, __robot_capa__|Type|VerbalCommunicationCapability,\ 
                                          __human__|Type|Human, __human__|hasDisposition|__human_disp__, __human_disp__|Type|VerbalCommunicationDisposition,\
                                          __robot__|isFacing|__human__, __human__|isAvailable|boolean#true''',
                              translation="the robot can speak with the human because it has a verbal communication capability, the human is available and has a \
                                           reciprocal disposition for verbal communication. Additionally, the robot is in front of an object that has the human \
                                           seated on it, ensuring that it is facing the human",
                              sub_questions=[sub_question_1])

# ======================== Question 2 =============================
question_2 = QuestionExample(infered_fact="__car__|canBeTowedBy|__vehicule__",
                             rule="Vehicle(?v), hasCapability(?v,?c), TowingCapability(?c), Towable(?o), hasWeight(?o,?w1),\
                                   hasTowingCapacity(?v,?w2), greaterThan(?w2,?w1) -> canBeTowedBy(?o,?v)",
                              explanation='''__vehicule__|Type|Vehicle, __vehicule__|hasCapability|__vehicule_capa__, __vehicule_capa__|Type|TowingCapability, \
                                          __car__|Type|Car, Car|SubClassOf|Towable, \
                                          __car__|hasWeight|integer#2000, __vehicule__|hasTowingCapacity|integer#3000.''',
                              translation="the vehicle can tow the car because it has a towing capability with sufficient capacity, and the car is a towable \
                                           object with a weight within the vehicle's towing capacity",
                              sub_questions=[])

# ======================== Question 3 =============================
sub_question_3 = SubQuestionExample(infered_fact="__drone_capa__|Type|AerialInspectionCapability",
                                    rule="AerialInspectionCapability|EquivalentTo|((isCapabilityOf some (hasCamera min 1 SecurityCamera)) and FlyingCapability)",
                                    explanation="__drone_capa__|isCapabilityOf|__drone__, __drone__|hasCamera|__camera__,\
                                                 __camera__|Type|SecurityCamera, __drone_capa__|Type|FlyingCapability",
                                    translation="the drone's capability for aerial inspection comes from the fact that it owns\
                                                 at least one security camera and it has the capability to fly.")

question_3 = QuestionExample(infered_fact="__drone__|canInspect|__bridge__",
                            rule="Drone(?d), hasCapability(?d,?c), AerialInspectionCapability(?c), Inspectable(?o), hasHeight(?o,?h1),\
                                  hasMaxInspectionHeight(?d,?h2), greaterThan(?h2,?h1) -> canInspect(?d,?o)",
                            explanation='''__drone__|Type|Drone, __drone__|hasCapability|__drone_capa__, __drone_capa__|Type|AerialInspectionCapability,\
                                           __bridge__|Type|Bridge, Bridge|SubClassOf|Inspectable,\
                                          __bridge__|hasHeight|integer#100, __drone__|hasMaxInspectionHeight|integer#200''',
                            translation="the drone can inspect the bridge because it has an aerial inspection capability based on having at least\
                                          one security camera and the capability to fly. The bridge is considered inspectable, and the drone's maximum\
                                          inspection height is greater than the height of the bridge",
                            sub_questions=[sub_question_3])


# ======================== Question 4 =============================
sub_question_4 = SubQuestionExample(infered_fact="__robot_capa__|Type|ChargingCapability",
                                    rule="ChargingCapability|EquivalentTo|(isCapabilityOf some (hasComponent exactly 1 ChargingConnector))",
                                    explanation="__robot_capa__|isCapabilityOf|__robot__, __robot__|hasComponent|__robot_part__, __robot_part__|Type|ChargingConnector",
                                    translation="the robot's capability for charging comes from the fact that it owns exactly one charging connector")

question_4 = QuestionExample(infered_fact="__robot__|canChargeAt|__charging_station__",
                              rule="DeliveryRobot(?r), hasCapability(?r,?c), ChargingCapability(?c), ChargingStation(?s), \
                                    hasPort(?s,?p), ChargingConnector(?p), isPowered(?s,boolean#true), hasBatteryLevel(?r,?b1), \
                                    hasBatteryThresholdForCharging(?r,?b2), lesserThan(?b1,?b2), hasChargingConnector(?r,?c1), \
                                    hasType(?c1,?t1), hasType(?p,?t2), equal(?t1,?t2) -> canChargeAt(?r,?s)",
                              explanation='''__robot__|Type|DeliveryRobot, __robot__|hasCapability|__robot_capa__, __robot_capa__|Type|ChargingCapability, \
                                            __charging_station__|Type|ChargingStation, __charging_station__|hasPort|__station_port__, __station_port__|Type|ChargingConnector, \
                                            __charging_station__|isPowered|boolean#true, __robot__|hasBatteryLevel|integer#15, __robot__|hasBatteryThresholdForCharging|integer#20), \
                                            __robot__|hasChargingConnector|__robot_part__, __robot_part__|hasType|string#USB_TypeC, __station_port__|hasType|string#USB_TypeC''',
                              translation="the delivery robot can charge at the station because it has a charging capability thanks to its single charging \
                                           connector which is compatible with the station's port as they both are usb C types, the station being powered, \
                                           and the robot's battery level being below its charging threshold",
                              sub_questions=[sub_question_4])