
# =============== EXAMPLES ===================

# ======================== Example 0 =============================

example_question_0 = "-Inference : xhz|hasBrother|okm / Justifications : xhz|isA|Human, xhz|hasSilbing|okm, okm|isA|Man."
example_rule_0 = "\n -Rule : Human(?a), hasSilbing(?a,?b), Man(?b) -> hasBrother(?a, ?b)."
example_answer_0 =  "Let's translate. translation is okm is xhz's brother because he is a man and his sibling."
example_0 = (example_question_0, example_answer_0, example_rule_0)

# ======================== Example 1 =============================

example_question_1 = "-Inference : prth|canSpeakWith|dzkl \n -Justifications : prth|isA|Robot, prth|hasCapability|stkl, stkl|isA|VerbalCommunicationCapability, dzkl|isA|Human, dzkl|hasDisposition|szom, szom|isA|VerbalCommunicationDisposition, prth|isNear|dzkl, dzkl|isInFrontOf|prth, dzkl|isAvailable|boolean#true."
                    
example_rule_1 = "\n -Rule : Robot(?r), hasCapability(?r,?c), VerbalCommunicationCapability(?c), Human(?a), hasDisposition(?a, ?d), VerbalCommunicationDisposition(?d), isNear(?r,?a), isInFrontOf(?a,?r), isAvailable(?a, boolean#true) -> canSpeakWith(?r, ?a)."
                  
example_answer_1=  "Let's translate. translation is the robot can speak with the human because it has the capability to communicate verbally, the human has the disposition for verbal communication, and both agents are close to each other."
example_1 = (example_question_1, example_answer_1, example_rule_1)

# ======================== Question 2 =============================
example_question_2 = "-Inference : car_1|canBeTowedBy|truck_1 \n -Justifications : truck_1|Type|Vehicle, truck_1|hasCapability|truck_tow_capa, truck_tow_capa|Type|TowingCapability, car_1|Type|Car, Car|SubClassOf|Towable, Towable|SubClassOf|(isTowableBy some Vehicle), car_1|hasWeight|integer#2000, truck_1|hasTowingCapacity|integer#3000, greaterThan(integer#3000, integer#2000)."
                    
example_rule_2 = "\n -Rule : Vehicle(?v), hasCapability(?v, ?c), TowingCapability(?c), Towable(?o), hasWeight(?o, ?w1), hasTowingCapacity(?v, ?w2), greaterThan(?w2, ?w1) -> canBeTowedBy(?o, ?v)"
                  
example_answer_2=  "Let's translate. translation is the truck can tow the car because it has a towing capability with sufficient capacity, and the car is a towable object with a weight within the truck's towing capacity."
example_2 = (example_question_2, example_answer_2, example_rule_2)


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