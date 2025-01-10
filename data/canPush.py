from data.questions import QuestionInstance

# ====================== canPush ===================
explanation_robot_capa = [
                           "pepper|Type|Robot",
                           "Robot|SubClassOf|Agent",
                           "pepper|hasCapability|pepper_capa"
                         ]

explanation_object_disp = [
                            "chair_1|Type|Chair",
                            "Chair|SubClassOf|Object",
                            "chair_1|hasDisposition|chair_1_disp"
                          ]

explanation_force = [
                    "pepper_left_gripper|Type|Gripper",
                    "Gripper|SubClassOf|EndEffector",
                    "pepper|hasComponent|pepper_left_gripper",
                    "pepper_left_gripper|hasApplicableForce|integer#1",
                    "chair_1|requiresForce|integer#1",
                    "equal(integer#1,integer#1)"
                    ]

# =============== Explanations why the class PushableDisposition is inferred =============
pushable_easy = "PushableDisposition|EquivalentTo|(isDispositionOf some (hasPart some RollablePart))"
pushable_medium= "PushableDisposition|EquivalentTo|(isDispositionOf some (hasPart some (RollablePart and (isOnRollableSurface value boolean#true)))"
pushable_hard = "PushableDisposition|EquivalentTo|(isDispositionOf some (hasPart some (RollablePart and (isOnRollableSurface value boolean#true) and (isBlockedBySomething value boolean#false)))"

explanations_pushable_easy= [
                                pushable_easy,
                                "chair_1_disp|isDispositionOf|chair_1",
                                "chair_1|hasPart|wheel_1",
                                "wheel_1|Type|Roller",
                                "Roller|SubClassOf|RollablePart"
                                ]

explanations_pushable_medium = [
                                pushable_medium,
                                "chair_1_disp|isDispositionOf|chair_1",
                                "chair_1|hasPart|wheel_1",
                                "wheel_1|Type|Roller",
                                "Roller|SubClassOf|RollablePart",
                                "wheel_1|isOnRollableSurface|boolean#true"
                                ]

explanations_pushable_hard = [
                                pushable_hard,
                                "chair_1_disp|isDispositionOf|chair_1",
                                "chair_1|hasPart|wheel_1",
                                "wheel_1|Type|Roller",
                                "Roller|SubClassOf|RollablePart",
                                "wheel_1|isOnRollableSurface|boolean#true",
                                "wheel_1|isBlockedBySomething|boolean#false"
                            ]

# =============== Explanations why the class PushingCapability is inferred =============
pushing_easy = "PushingCapability|EquivalentTo|(isCapabilityOf some (hasGripper min 1 Gripper)"
pushing_medium= "PushingCapability|EquivalentTo|(isCapabilityOf some (hasGripper min 1 (Gripper and (holdsSomething value boolean#false))"
pushing_hard = "PushingCapability|EquivalentTo|(isCapabilityOf some (hasGripper min 1 (Gripper and (holdsSomething value boolean#false) and RigidEndEffector))"

explanations_pushing_easy= [
                                pushing_easy,
                                "pepper_capa|isCapabilityOf|pepper",
                                "pepper|hasGripper|pepper_left_gripper",
                                "pepper_left_gripper|Type|MechanicalHand",
                                "MechanicalHand|SubClassOf|Gripper"
                                ]

explanations_pushing_medium = [
                                pushing_medium,
                                "pepper_capa|isCapabilityOf|pepper",
                                "pepper|hasGripper|pepper_left_gripper",
                                "pepper_left_gripper|Type|MechanicalHand",
                                "MechanicalHand|SubClassOf|Gripper",
                                "pepper_left_gripper|holdsSomething|boolean#false"
                                ]

explanations_pushing_hard = [
                                pushing_hard,
                                "pepper_capa|isCapabilityOf|pepper",
                                "pepper|hasGripper|pepper_left_gripper",
                                "pepper_left_gripper|Type|MechanicalHand",
                                "MechanicalHand|SubClassOf|Gripper",
                                "pepper_left_gripper|holdsSomething|boolean#false",
                                "pepper_left_gripper|Type|RigidEndEffector"
                                ]

# =============== Explanations why the property isApproachableBy exists =============
object_push_available_easy = "isApproachableBy" # chair isApproachableBy agent
object_push_available_medium = "(isOnTable o isWithinMovingRangeOf)|SubPropertyOf|isApproachableBy" # box isOnTable table isWithinMovingRangeOf agent
object_push_available_hard = "(isOnTable o isInSafeArea o isWithinMovingRangeOf)|SubPropertyOf|isApproachableBy" # box isOnTable table isInSafeArea kitchen isWithinMovingRangeOf agent

explanations_object_push_easy = ["chair_1|isApproachableBy|pepper"]

explanations_object_push_medium = [
                                object_push_available_medium,
                                "chair_1|isOnTable|table_1",
                                "table_1|isWithinMovingRangeOf|pepper"
                                ]

explanations_object_push_hard = [
                                object_push_available_hard,
                                "chair_1|isOnTable|table_1",
                                "table_1|isInSafeArea|kitchen",
                                "kitchen|isWithinMovingRangeOf|pepper"
                                ]

# Concatenate the explanations according to the complexity level (easy, medium, hard)
explanations_push_easy = explanation_robot_capa + explanations_pushing_easy + explanation_object_disp + explanations_pushable_easy + explanations_object_push_easy + explanation_force
explanations_push_medium = explanation_robot_capa + explanations_pushing_medium + explanation_object_disp + explanations_pushable_medium + explanations_object_push_medium + explanation_force
explanations_push_hard= explanation_robot_capa + explanations_pushing_hard + explanation_object_disp + explanations_pushable_hard + explanations_object_push_hard + explanation_force

# print("easy : ", explanations_push_easy)
# print("medium : ", explanations_push_medium)
# print("hard : ", explanations_push_hard)

fact_push = "pepper|canPush|chair_1"

template_dict_push = {'pepper': '__var0__',  
                    'chair_1': '__var1__',
                    'chair_1_disp': '__var2__',
                    'pepper_capa': '__var3__',
                    'pepper_left_gripper' : '__var4__',
                    'wheel_1' : '__var5__',
                    'table_1' : '__var6__',
                    'kitchen' : '__var7__',
                    'Robot': '__agent__',
                    'MechanicalHand': '__component__',
                    'Chair': '__object__',
                    'Roller': '__part__'
                    }


class VariableConcept:
  def __init__(self, concept, label):
    self.concept_ = concept
    self.label_ = label

object_list = [
              VariableConcept('ToyWagon', 'toy wagon'), 
              VariableConcept('RemoteControlledCar', 'remote controlled car'), 
              VariableConcept('MiniShoppingCart', 'shopping cart'), 
              VariableConcept('OfficeChair', 'office chair'), 
              VariableConcept('RoombaRobot', 'roomba')
              ]

part_list = [
              VariableConcept('Wheel', 'wheel'), 
              VariableConcept('Roller', 'roller'), 
              VariableConcept('Caster', 'caster'), 
              VariableConcept('PivotRoller', 'pivot roller'),
              VariableConcept('PivotWheel', 'pivot wheel')
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

class_variables_final_push = { 
                            "__object__" : object_list,
                            "__part__" :   part_list,
                            "__agent__" :   agent_list,
                            "__component__" : component_list
                             }

push_rule = "-Rule : Agent(?a), hasCapability(?a, ?c), PushingCapability(?c), Object(?o), hasDisposition(?o, ?d), PushableDisposition(?d),\
               isApproachableBy(?o,?a), EndEffector(?g), hasComponent(?a,?g), hasApplicableForce(?g,?w1), requiresForce(?o,?w2), equal(?w2,?w1) -> canPush(?a, ?o)."

concepts_rule = ['pushing', 'pushable', 'approachable', 'applicable_force', 'required_force', 'can push']

concept_easy = {
                'rule' : ['can push', '__robot__', '__component__', '__object__', '__rollable_part__'],
                'disp' : ['pushable disposition', "min1rollable_part"], 
                'capa': ['pushing capability', 'min1gripper'], 
                'property' : ['approachable'],
                'constraint' : ['applicable force', 'required_force']
                }


concept_medium = {
                'rule' : ['can push', '__robot__', '__component__', '__object__', '__rollable_part__'],
                'disp' : ['pushable disposition', "min1rollable_part", "rollable_part_on_rollable_surface"], 
                'capa': ['pushing capability', 'min1gripper', 'empty_hand'], 
                'property' : ['approachable', 'object_on_table', 'table_in_moving_range_robot'],
                'constraint' : ['applicable force', 'required_force']
                }

concept_hard = {
                'rule' : ['can push', '__robot__', '__component__', '__object__', '__rollable_part__'],
                'disp' : ['pushable disposition', "min1rollable_part", "rollable_part_on_rollable_surface", 'rollable_part_unblocked'],
                'capa': ['pushing capability', 'min1gripper', 'empty_hand', 'rigid' ], 
                'property' : ['approachable', 'object_on_table', 'table_in_safe_area', 'table_in_moving_range_robot'],
                'constraint' : ['applicable force', 'required_force']
                }

#easy
# "concepts" : [
#   "can push", 
#   "pushable disposition", "min1rollable_part",
#   "pushing capability", "min1gripper", 
#   "approachable", 
#   "applicable force", "required_force"  
# ]

# medium
# "concepts" : [
#   "can push", 
#   "pushable disposition", "min1rollable_part", "rollable_part_on_rollable_surface",
#   "pushing capability", "min1gripper", "empty_hand",
#   "approachable", "object_on_table", "table_in_moving_range_robot",
#   "applicable force", "required_force"   
# ]

# hard
# "concepts" : [
#   "can push", 
#   "pushable disposition", "min1rollable_part", "rollable_part_on_rollable_surface", "rollable_part_unblocked",
#   "pushing capability", "min1gripper", "empty_hand", "rigid",
#   "approachable", "object_on_table", "table_in_safe_area", "table_in_moving_range_robot",
#   "applicable force", "required_force"     
# ]

# gt_push_easy = "The __agent__ can push the __object__ because on one hand it has the pushing capability through having at least one gripper, \
#                 thanks to its __component__. On the other hand, the __object__ has the disposition of being pushable because it has some __part__ which is a wheel. \
#                 Moreover the __object__ is approachable by the __agent__."
                
# gt_push_medium = "The __agent__ can push the __object__ because on one hand it has the pushing capability through having at least one gripper which\
#                 doesn't hold anything, thanks to its __component__. On the other hand, the __object__ has the disposition of being pushable because it has\
#                 some __part__ which is a wheel and on a rollable surface. \
#                 Moreover the __object__ is approachable by the __agent__ because it is on a table that is within the moving range of the __agent__."
                 
# gt_push_hard = "The __agent__ can push the __object__ because on one hand it has the pushing capability through having at least one gripper which \
#                   is also a rigid end effector and that doesn't hold anything, thanks to its __component__. On the other hand, the __object__ has the \
#                   disposition of being pushable because it has some __part__ which is a wheel, on a rollable surface and unblocked. \
#                   Moreover the __object__ is approachable by the __agent__ because it is on a table that is in a safe area, which is within the moving range of the __agent__."
                              
question_push_easy = QuestionInstance(name="q_push_easy", fact=fact_push, explanations=explanations_push_easy, rule=push_rule, 
                                      classes_var=class_variables_final_push, template_dict=template_dict_push, ground_truth_sentence=None,
                                      concept_rule=concepts_rule)

question_push_medium= QuestionInstance(name="q_push_medium", fact=fact_push, explanations=explanations_push_medium, rule=push_rule, 
                                       classes_var=class_variables_final_push, template_dict=template_dict_push, ground_truth_sentence=None,
                                      concept_rule=concepts_rule)

question_push_hard = QuestionInstance(name="q_push_hard", fact=fact_push, explanations=explanations_push_hard, rule=push_rule, 
                                      classes_var=class_variables_final_push, template_dict=template_dict_push, ground_truth_sentence=None,
                                      concept_rule=concepts_rule)