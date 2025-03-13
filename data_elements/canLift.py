from data_elements.questions import QuestionInstance
# ====================== canLift ===================

explanation_robot_capa = [
                           "pepper|Type|Robot",
                           "Robot|SubClassOf|Agent",
                           "pepper|hasCapability|pepper_capa"
                         ]

explanation_object_disp = [
                            "box_2|Type|Box",
                            "Box|SubClassOf|Object",
                            "box_2|hasDisposition|box_2_disp"
                          ]

explanation_weight = [
                    "pepper_left_gripper|Type|Gripper",
                    "Gripper|SubClassOf|EndEffector",
                    "pepper|hasComponent|pepper_left_gripper",
                    "pepper_left_gripper|hasWeightLimit|integer#2",
                    "box_2|hasWeight|integer#1",
                    "lesserThan(integer#1,integer#2)"
                    ]

# =============== Explanations why the class LiftableDisposition is inferred =============
liftable_easy = "LiftableDisposition|EquivalentTo|(isDispositionOf some (hasPart min 2 HoldablePart))"
liftable_medium= "LiftableDisposition|EquivalentTo|(isDispositionOf some ((hasPart min 2 HoldablePart) and (canBeUsed value boolean#true)))"
liftable_hard = "LiftableDisposition|EquivalentTo|(isDispositionOf some ((hasPart min 2 (HoldablePart and (isAttachedToSomething value boolean#false))) and (canBeUsed value boolean#true)))"

explanations_liftable_easy= [
                                liftable_easy,
                                "box_2_disp|isDispositionOf|box_2",
                                "box_2|hasPart|handle_1",
                                "handle_1|Type|Handle",
                                "Handle|SubClassOf|HoldablePart",
                                "box_2|hasPart|handle_2",
                                "handle_2|Type|Handle",
                                "Handle|SubClassOf|HoldablePart"
                                ]

explanations_liftable_medium = [
                                liftable_medium,
                                "box_2_disp|isDispositionOf|box_2",
                                "box_2|hasPart|handle_1",
                                "handle_1|Type|Handle",
                                "Handle|SubClassOf|HoldablePart",
                                "box_2|hasPart|handle_2",
                                "handle_2|Type|Handle",
                                "Handle|SubClassOf|HoldablePart",
                                "box_2|canBeUsed|boolean#true"
                                ]

explanations_liftable_hard = [
                                liftable_hard,
                                "box_2_disp|isDispositionOf|box_2",
                                "box_2|hasPart|handle_1",
                                "handle_1|Type|Handle",
                                "Handle|SubClassOf|HoldablePart",
                                "handle_1|isAttachedToSomething|boolean#false",
                                "box_2|hasPart|handle_2",
                                "handle_2|Type|Handle",
                                "Handle|SubClassOf|HoldablePart",
                                "handle_2|isAttachedToSomething|boolean#false",
                                "box_2|canBeUsed|boolean#true"
                            ]

# =============== Explanations why the class LiftingCapability is inferred =============
lifting_easy = "LiftingCapability|EquivalentTo|(isCapabilityOf some (hasComponent min 2 Gripper)"
lifting_medium= "LiftingCapability|EquivalentTo|(isCapabilityOf some ((hasComponent min 2 Gripper) and (hasComponent some MotionPlanningAlgo))"
lifting_hard = "LiftingCapability|EquivalentTo|(isCapabilityOf some ((hasComponent min 2 Gripper) and (hasComponent some MotionPlanningAlgo) and (hasSomethingInHands value boolean#false))"

explanations_lifting_easy= [
                                lifting_easy,
                                "pepper_capa|isCapabilityOf|pepper",
                                "pepper|hasComponent|pepper_left_gripper",
                                "pepper_left_gripper|Type|MechanicalHand",
                                "MechanicalHand|SubClassOf|Gripper",
                                "pepper|hasComponent|pepper_right_gripper",
                                "pepper_right_gripper|Type|MechanicalHand",
                                "MechanicalHand|SubClassOf|Gripper"
                                ]

explanations_lifting_medium = [
                                lifting_medium,
                                "pepper_capa|isCapabilityOf|pepper",
                                "pepper|hasComponent|pepper_left_gripper",
                                "pepper_left_gripper|Type|MechanicalHand",
                                "MechanicalHand|SubClassOf|Gripper",
                                "pepper|hasComponent|pepper_right_gripper",
                                "pepper_right_gripper|Type|MechanicalHand",
                                "MechanicalHand|SubClassOf|Gripper",
                                "pepper|hasComponent|move_it",
                                "move_it|Type|MotionPlanningAlgo"
                                ]

explanations_lifting_hard = [
                                lifting_hard,
                                "pepper_capa|isCapabilityOf|pepper",
                                "pepper|hasComponent|pepper_left_gripper",
                                "pepper_left_gripper|Type|MechanicalHand",
                                "MechanicalHand|SubClassOf|Gripper",
                                "pepper|hasComponent|pepper_right_gripper",
                                "pepper_right_gripper|Type|MechanicalHand",
                                "MechanicalHand|SubClassOf|Gripper",
                                "pepper|hasComponent|move_it",
                                "move_it|Type|MotionPlanningAlgo",
                                "pepper|hasSomethingInHands|boolean#false"
                                ]

# =============== Explanations why the property isTouchableBy exists =============
object_lift_available_easy = "isTouchableBy" # box isTouchableBy agent
object_lift_available_medium = "(isOnTouchableSupport o isWithinMovingRangeOf)|SubPropertyOf|isTouchableBy" 
object_lift_available_hard = "(isOnTouchableSupport o isInAccessibleArea o isWithinMovingRangeOf)|SubPropertyOf|isTouchableBy"

explanations_object_lift_easy = ["box_2|isTouchableBy|pepper"]

explanations_object_lift_medium = [
                                object_lift_available_medium,
                                "box_2|isOnTouchableSupport|table_1",
                                "table_1|isWithinMovingRangeOf|pepper"
                                ]

explanations_object_lift_hard = [
                                object_lift_available_hard,
                                "box_2|isOnTouchableSupport|table_1",
                                "table_1|isInAccessibleArea|locker_room",
                                "locker_room|isWithinMovingRangeOf|pepper"
                                ]

# Concatenate the explanations according to the complexity level (easy, medium, hard)
explanations_lift_easy = explanation_robot_capa + explanations_lifting_easy + explanation_object_disp + explanations_liftable_easy + explanations_object_lift_easy + explanation_weight
explanations_lift_medium = explanation_robot_capa + explanations_lifting_medium + explanation_object_disp + explanations_liftable_medium + explanations_object_lift_medium + explanation_weight
explanations_lift_hard= explanation_robot_capa + explanations_lifting_hard + explanation_object_disp + explanations_liftable_hard + explanations_object_lift_hard + explanation_weight

# print("easy : ", explanations_lift_easy)
# print("medium : ", explanations_lift_medium)
# print("hard : ", explanations_lift_hard)

fact_lift = "pepper|canLift|box_2"

template_dict_lift = {'pepper': '__var0__',  
                    'box_2': '__var1__',
                    'box_2_disp': '__var2__',
                    'pepper_capa': '__var3__',
                    'pepper_left_gripper' : '__var4__',
                    'pepper_right_gripper' : '__var5__',
                    'handle_1' : '__var6__',
                    'handle_2' : '__var7__',
                    'table_1' : '__var8__',
                    'locker_room' : '__var9__',
                    'move_it' : '__var10__',
                    'Robot': '__agent__',
                    'MechanicalHand': '__component__',
                    'Box': '__object__',
                    'Handle': '__part__'
                    }
class VariableConcept:
  def __init__(self, concept, label):
    self.concept_ = concept
    self.label_ = label

object_list = [
              VariableConcept('Toolbox', 'tool box'), 
              VariableConcept('Bucket', 'bucket'), 
              VariableConcept('LaundryBasket', 'laundry basket'), 
              VariableConcept('CookingPot', 'cooking pot'), 
              VariableConcept('Suitcase', 'suitcase'),
              VariableConcept('OvenTray', 'oven tray'),
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


concept_easy = {
                'rule' : ['can lift', '__robot__', '__component__', '__object__', '__part__'],
                'disp' : ['liftable disposition', "min2holdable_part"], 
                'capa': ['lifting capability', 'min2gripper'], 
                'property' : ['touchable'],
                'constraint' : ['weight limit', 'object_weight']
                }


concept_medium = {
                'rule' : ['can lift', '__robot__', '__component__', '__object__', '__part__'],
                'disp' : ['liftable disposition',"min2holdable_part", "can_be_used"], 
                'capa': ['lifting capability', 'min2gripper', 'motion_planing_algo'], 
                'property' : ['touchable', 'on_touchable_support', 'moving_range_robot'],
                'constraint' : ['weight limit', 'object_weight']
                }

concept_hard = {
                'rule' : ['can lift', '__robot__', '__component__', '__object__', '__part__'],
                'disp' : ['liftable disposition', "min2holdable_part", "can_be_used", 'holding_parts_not_attached'],
                'capa': ['lifting capability', 'min2gripper', 'motion_planing_algo', 'empty_hands' ], 
                'property' : ['touchable', 'on_touchable_support', 'in_accessible_area', 'moving_range_robot'],
                'constraint' : ['weight limit', 'object_weight']
                }
# easy
# "concepts" : [
#   "can lift", 
#   "liftable disposition", "min2holdable_part",
#   "lifting capability", "min2gripper", 
#   "touchable", 
#   "weight limit", "object_weight"  
# ]

# medium
# "concepts" : [
#   "can lift", 
#   "liftable disposition", "min2holdable_part", "can_be_used",
#   "lifting capability", "min2gripper", "motion_planing_algo",
#   "touchable", "on_touchable_support", "moving_range_robot",
#   "weight limit", "object_weight"  
# ]

# hard
# "concepts" : [
#   "can lift", 
#   "liftable disposition", "min2holdable_part", "can_be_used", "holding_parts_not_attached",
#   "lifting capability", "min2gripper", "motion_planing_algo", "empty_hands",
#   "touchable", "on_touchable_support", "in_accessible_area", "moving_range_robot",
#   "weight limit", "object_weight"  
# ]

class_variables_final_lift = { 
                    "__object__" : object_list,
                    "__part__" :  part_list,
                    "__agent__" :   agent_list,
                    "__component__" : component_list
                    }


lift_rule = "-Rule : Agent(?a), hasCapability(?a, ?c), LiftingCapability(?c), Object(?o), hasDisposition(?o, ?d), LiftableDisposition(?d),\
               isTouchableBy(?o,?a), EndEffector(?g), hasComponent(?a,?g), hasWeightLimit(?g,?w1), hasWeight(?o,?w2), lesserThan(?w2,?w1) -> canLift(?a, ?o)."

concepts_rule = ['lifting', 'liftable', 'touchable', 'weight limit', 'object_weight', 'can lift']

# gt_lift_easy = "The __agent__ can lift the __object__ because on one hand it has the lifting capability through its two __component__s which are grippers. \
#                  On the other hand, the __object__ has the disposition of being liftable because it has two __part__s, which are graspable parts. \
#                  Moreover the __object__ is touchable by the __agent__."

# gt_lift_medium = "The __agent__ can lift the __object__ because on one hand it has the grasping capability through its two __component__s which are grippers \
#                   and being equipped with a motion planning algorithm. On the other hand, the __object__ has the disposition of being liftable \
#                   because it can be used and has two __part__s, which are graspable parts. Moreover the __object__ is touchable by the __agent__ because \
#                   it is on a touchable support which is within the moving range of the __agent__."
                 
# gt_lift_hard = "The __agent__ can lift the __object__ because on one hand it has the grasping capability through its two __component__s which are grippers \
#                 , being equipped with a motion planning algorithm and not having anything in its hands. On the other hand, the __object__ has the disposition \
#                 of being liftable because it can be used, has two __part__s, which are graspable parts, and that are not attached to something. \
#                 Moreover the __object__ is touchable by the __agent__ because it is on a touchable support which is in an accessible area, \
#                 within the moving range of the __agent__."
                
question_lift_easy = QuestionInstance(name="q_lift_easy", fact=fact_lift, explanations=explanations_lift_easy, rule=lift_rule, 
                                      classes_var=class_variables_final_lift, template_dict=template_dict_lift, ground_truth_sentence=None,
                                      concept_rule=concepts_rule)

question_lift_medium= QuestionInstance(name="q_lift_medium", fact=fact_lift, explanations=explanations_lift_medium, rule=lift_rule, 
                                      classes_var=class_variables_final_lift, template_dict=template_dict_lift, ground_truth_sentence=None,
                                      concept_rule=concepts_rule)

question_lift_hard = QuestionInstance(name="q_lift_hard", fact=fact_lift, explanations=explanations_lift_hard, rule=lift_rule, 
                                      classes_var=class_variables_final_lift, template_dict=template_dict_lift, ground_truth_sentence=None,
                                      concept_rule=concepts_rule)
