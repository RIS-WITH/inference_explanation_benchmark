from data.questions import QuestionInstance

# ====================== canGrasp ===================

explanation_robot_capa = [
                           "pepper|Type|Robot",
                           "Robot|SubClassOf|Agent",
                           "pepper|hasCapability|pepper_capa"
                         ]

explanation_object_disp = [
                            "mug_3|Type|Mug",
                            "Mug|SubClassOf|Object",
                            "mug_3|hasDisposition|mug_3_disp"
                          ]

explanation_width = [
                    "pepper_left_gripper|Type|Gripper",
                    "Gripper|SubClassOf|EndEffector",
                    "pepper|hasComponent|pepper_left_gripper",
                    "pepper_left_gripper|hasOpeningWidth|integer#2",
                    "mug_3|hasWidth|integer#1",
                    "greaterThan(integer#2,integer#1)"
                    ]

# =============== Explanations why the class GraspableDisposition is inferred =============
graspable_easy = "GraspableDisposition|EquivalentTo|isDispositionOf some (hasPart some GraspablePart)"
graspable_medium= "GraspableDisposition|EquivalentTo|(isDispositionOf some ((hasPart some GraspablePart) and (isATouchableObject value boolean#true)))"
graspable_hard = "GraspableDisposition|EquivalentTo|(isDispositionOf some ((hasPart some (GraspablePart and (IsAlreadyInUse value boolean#false)) and (isATouchableObject value boolean#true)))"

explanations_graspable_easy= [
                                graspable_easy,
                                "mug_3_disp|isDispositionOf|mug_3",
                                "mug_3|hasPart|handle_3",
                                "handle_3|Type|HandGrip",
                                "HandGrip|SubClassOf|GraspablePart"
                                ]

explanations_graspable_medium = [
                                graspable_medium,
                                "mug_3_disp|isDispositionOf|mug_3",
                                "mug_3|hasPart|handle_3",
                                "handle_3|Type|HandGrip",
                                "HandGrip|SubClassOf|GraspablePart",
                                "mug_3|isATouchableObject|boolean#true",
                                ]

explanations_graspable_hard = [
                                graspable_hard,
                                "mug_3_disp|isDispositionOf|mug_3",
                                "mug_3|hasPart|handle_3",
                                "handle_3|Type|HandGrip",
                                "HandGrip|SubClassOf|GraspablePart",
                                "handle_3|IsAlreadyInUse|boolean#false",
                                "mug_3|isATouchableObject|boolean#true",
                                ]

# =============== Explanations why the class GraspingCapability is inferred =============
grasping_easy = "GraspingCapability|EquivalentTo|(isCapabilityOf some (hasComponent some Gripper)"
grasping_medium= "GraspingCapability|EquivalentTo|(isCapabilityOf some ((hasComponent some Gripper) and (hasComponent some MotionPlanningAlgo))"
grasping_hard = "GraspingCapability|EquivalentTo|(isCapabilityOf some ((hasComponent some (Gripper and (holdsSomething value boolean#false)) and (hasComponent some MotionPlanningAlgo))"

explanations_grasping_easy= [
                                grasping_easy,
                                "pepper_capa|isCapabilityOf|pepper",
                                "pepper|hasComponent|pepper_left_gripper",
                                "pepper_left_gripper|Type|MechanicalHand",
                                "MechanicalHand|SubClassOf|Gripper"
                                ]

explanations_grasping_medium = [
                                grasping_medium,
                                "pepper_capa|isCapabilityOf|pepper",
                                "pepper|hasComponent|pepper_left_gripper",
                                "pepper_left_gripper|Type|MechanicalHand",
                                "MechanicalHand|SubClassOf|Gripper",
                                "pepper|hasComponent|move_it",
                                "move_it|Type|MotionPlanningAlgo",
                                ]

explanations_grasping_hard = [
                                grasping_hard,
                                "pepper_capa|isCapabilityOf|pepper",
                                "pepper|hasComponent|pepper_left_gripper",
                                "pepper_left_gripper|Type|MechanicalHand",
                                "MechanicalHand|SubClassOf|Gripper",
                                "pepper_left_gripper|holdsSomething|boolean#false",
                                "pepper|hasComponent|move_it",
                                "move_it|Type|MotionPlanningAlgo",
                                ]

# =============== Explanations why the property isReachable exists =============
object_grasp_available_easy = "isReachableBy" 
object_grasp_available_medium = "(isContainedIn o isWithinGraspRangeOf)|SubPropertyOf|isReachableBy" 
object_grasp_available_hard = "(isContainedIn o isLocatedInArea o isWithinGraspRangeOf)|SubPropertyOf|isReachableBy"

explanations_object_grasp_easy = ["mug_3|isReachableBy|pepper"]

explanations_object_grasp_medium = [
                                object_grasp_available_medium,
                                "mug_3|isContainedIn|cupboard_1",
                                "cupboard_1|isWithinGraspRangeOf|pepper"
                                ]

explanations_object_grasp_hard = [
                                object_grasp_available_hard,
                                "mug_3|isContainedIn|cupboard_1",
                                "cupboard_1|isLocatedInArea|storage_room",
                                "storage_room|isWithinGraspRangeOf|pepper"
                                ]

# Concatenate the explanations according to the complexity level (easy, medium, hard)
explanations_grasp_easy = explanation_robot_capa + explanations_grasping_easy + explanation_object_disp + explanations_graspable_easy + explanations_object_grasp_easy + explanation_width
explanations_grasp_medium = explanation_robot_capa + explanations_grasping_medium + explanation_object_disp + explanations_graspable_medium + explanations_object_grasp_medium + explanation_width
explanations_grasp_hard= explanation_robot_capa + explanations_grasping_hard + explanation_object_disp + explanations_graspable_hard + explanations_object_grasp_hard + explanation_width

# print("easy : ", explanations_grasp_easy)
# print("medium : ", explanations_grasp_medium)
# print("hard : ", explanations_grasp_hard)

fact_grasp = "pepper|canGrasp|mug_3"

template_dict_grasp = {
                      'pepper': '__var0__',  
                      'mug_3': '__var1__',
                      'mug_3_disp': '__var2__',
                      'pepper_capa': '__var3__',
                      'pepper_left_gripper' : '__var4__',
                      'handle_3' : '__var5__',
                      'cupboard_1' : '__var6__',
                      'storage_room' : '__var7__',
                      'move_it' : '__var8__',
                      'Robot': '__agent__',
                      'MechanicalHand': '__component__',
                      'Mug': '__object__',
                      'HandGrip': '__part__'
                      }

new_objects = ["Hammer"," Toy Bucket", "Suitcase", "Shovel", "Mug", "CookingPot", "Lunchbox"]
new_parts = ["Grip", "Hold", "HandGrip", "Handle"]

class VariableConcept:
  def __init__(self, concept, label):
    self.concept_ = concept
    self.label_ = label

object_list = [
              VariableConcept('Mug', 'mug'), 
              VariableConcept('Hammer', 'hammer'), 
              VariableConcept('ToyBucket', 'toy bucket'), 
              VariableConcept('Suitcase', 'suitcase'), 
              VariableConcept('Shovel', 'shovel'), 
              VariableConcept('CookingPot', 'cooking pot'),
              VariableConcept('Lunchbox', 'lunchbox')
              ]

part_list = [
              VariableConcept('Handle', 'handle'), 
              VariableConcept('HandGrip', 'hand grip'), 
              VariableConcept('Grip', 'grip'), 
              VariableConcept('Hold', 'hold')
              ]

agent_list = [
              VariableConcept('Robot', 'robot'), 
              VariableConcept('Pr2', 'pr2'), 
              VariableConcept('Pepper', 'pepper'), 
              VariableConcept('Tiago', 'tiago')
              ]

component_list = [
              VariableConcept('MechanicalHand', 'mechanical hand'), 
              VariableConcept('Claw', 'claw'), 
              VariableConcept('TwoFingerClaw', 'two-finger claw'), 
              VariableConcept('Manipulator', 'manipulator')
              ]

class_variables_final_grasp = {
                            "__object__" : object_list,
                            "__part__" :  part_list,
                            "__agent__" :   agent_list,
                            "__component__" : component_list
                              }

grasp_rule = "-Rule : Agent(?a), hasCapability(?a, ?c), GraspingCapability(?c), Object(?o), hasDisposition(?o, ?d), GraspableDisposition(?d),\
               isReachableBy(?o,?a), EndEffector(?g), hasComponent(?a,?g), hasOpeningWidth(?g,?w1), hasWidth(?o,?w2), greaterThan(?w1,?w2) -> canGrasp(?a, ?o)."

concepts_rule = ['grasping', 'graspable', 'reach', 'opening', 'object_width', 'can grasp']


concept_easy = {
                'rule' : ['can grasp', '__robot__', '__component__', '__object__', '__part__'],
                'disp' : ['graspable disposition', "1GraspablePart"], 
                'capa': ['grasping capability', '1gripper'], 
                'property' : ['reachable'],
                'constraint' : ['opening width', 'object_width']
                }

concept_medium = {
                'rule' : ['can grasp', '__robot__', '__component__', '__object__', '__part__'],
                'disp' : ['graspable disposition', "1GraspablePart", "touchable_object"], 
                'capa': ['grasping capability', '1gripper', 'motion_planing_algo'], 
                'property' : ['reachable', 'is_contained_in', 'within_grasping_range'],
                'constraint' : ['opening width', 'object_width']
                }

concept_hard = {
                'rule' : ['can grasp', '__robot__', '__component__', '__object__', '__part__'],
                'disp' : ['graspable disposition',"1GraspablePart", "touchable_object", 'object_not_already_used'],
                'capa': ['grasping capability', '1gripper', 'motion_planing_algo', 'empty_hand' ], 
                'property' : ['reachable', 'is_contained_in', 'container_in_area', 'within_grasping_range'],
                'constraint' : ['opening width', 'object_width']
                }

# easy
# "concepts" : [
#   "can grasp", 
#   "graspable disposition", "1GraspablePart",
#   "grasping capability", "1gripper", 
#   "reachable", 
#   "opening width", "object_width"  
# ]

# medium
# "concepts" : [
#   "can grasp", 
#   "graspable disposition", "1GraspablePart", "touchable_object",
#   "grasping capability", "1gripper", "motion_planing_algo",
#   "reachable", "is_contained_in", "within_grasping_range",
#   "opening width", "object_width"    
# ]

# hard
# "concepts" : [
#   "can grasp", 
#   "graspable disposition", "1GraspablePart", "touchable_object", "object_not_already_used",
#   "grasping capability", "1gripper", "motion_planing_algo", "empty_gripper",
#   "reachable", "is_contained_in", "container_in_area", "within_grasping_range",
#   "opening width", "object_width"   
# ]

# gt_grasp_easy = "The __agent__ can grasp the __object__ because on one hand it has the grasping capability through its __component__ which is a gripper. \
#                  On the other hand, the __object__ has the disposition of being graspable because it has a __part__. \
#                  Moreover the __object__ is reachable by the __agent__."

# gt_grasp_medium = "The __agent__ can grasp the __object__ because on one hand it has the grasping capability through its __component__ which is a gripper, \
#                   and being equipped with a motion planning algorithm. On the other hand, the __object__ has the disposition of being graspable \
#                   because it has a __part__ and is a touchable object. Moreover the __object__ is reachable by the __agent__ because \
#                   it is contained in something which is within the grasping range of the __agent__."
                 
# gt_grasp_hard = "The __agent__ can grasp the __object__ because on one hand it has the grasping capability through its __component__ which is a gripper, \
#                   not currently holding something, and being equipped with a motion planning algorithm. On the other hand, the __object__ has the disposition \
#                   of being graspable because it is a touchable object, and has a __part__ which is not already in use by someone. \
#                   Moreover the __object__ is reachable by the __agent__ because it is contained in something which is located in an area within the \
#                   grasping range of the __agent__."
                           
question_grasp_easy = QuestionInstance(name="q_grasp_easy", fact=fact_grasp, explanations=explanations_grasp_easy, rule=grasp_rule, 
                                       classes_var=class_variables_final_grasp, template_dict=template_dict_grasp, ground_truth_sentence=None, 
                                       concept_rule=concepts_rule)

question_grasp_medium= QuestionInstance(name="q_grasp_medium", fact=fact_grasp, explanations=explanations_grasp_medium, rule=grasp_rule, 
                                        classes_var=class_variables_final_grasp, template_dict=template_dict_grasp, ground_truth_sentence=None,
                                        concept_rule=concepts_rule)

question_grasp_hard = QuestionInstance(name="q_grasp_hard", fact=fact_grasp, explanations=explanations_grasp_hard, rule=grasp_rule, 
                                       classes_var=class_variables_final_grasp, template_dict=template_dict_grasp, ground_truth_sentence=None,
                                       concept_rule=concepts_rule)

