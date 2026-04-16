from data_elements.QuestionManager import QuestionRule, QuestionManager
from data_elements.VariableManager import VariableManager
from data_elements.Explanation import AffordanceBase, ClassExpression, ClassExpressionExplanation

# ====================== Rule ===================

lift_rule = QuestionRule(property = "canLift",
                         rule = "Agent(?a), hasCapability(?a, ?c), LiftingCapability(?c),\
                                 Object(?o), hasDisposition(?o, ?d), LiftableDisposition(?d),\
                                 isTouchableBy(?o,?a), EndEffector(?g), hasComponent(?a,?g),\
                                 hasWeightLimit(?g,?w1), hasWeight(?o,?w2), lesserThan(?w2,?w1)\
                                 -> canLift(?a, ?o)",
                         concepts = ['lifting', 'liftable', 'touchable', 'weight limit', 'object_weight', 'can lift'])

# ====================== Variables ===================

variable_manager = VariableManager()
variable_manager.addClassVariable('__Object__',
                                  {'Toolbox' : 'tool box',
                                   'Bucket' : 'bucket',
                                   'LaundryBasket' : 'laundry basket',
                                   'CookingPot' : 'cooking pot',
                                   'Suitcase' : 'suitcase',
                                   'OvenTray' : 'oven tray'})

# ====================== Affordance ===================

affordance = AffordanceBase(capa=None, # Use the default capability
                            disp=None, # Use the default disposition
                            match=[
                                  "__gripper_1__|Type|Gripper",
                                  "Gripper|SubClassOf|EndEffector",
                                  "__agent__|hasComponent|__gripper_1__",
                                  "__gripper_1__|hasWeightLimit|integer#2",
                                  "__object__|hasWeight|integer#1",
                                  "lesserThan(integer#1,integer#2)"
                                  ])

# =============== Disposition Capability =============
disposition_expression = ClassExpression(easy= "LiftableDisposition|EquivalentTo|(isDispositionOf some (hasPart min 2 HoldablePart))",
                                         medium= "LiftableDisposition|EquivalentTo|(isDispositionOf some ((hasPart min 2 HoldablePart) and (canBeUsed value boolean#true)))",
                                         hard="LiftableDisposition|EquivalentTo|(isDispositionOf some ((hasPart min 2 (HoldablePart and (isAttachedToSomething value boolean#false))) and (canBeUsed value boolean#true)))")

diposition_explanation = ClassExpressionExplanation(disposition_expression,
                                                    easy=["__object_disp__|isDispositionOf|__object__",
                                                          "__object__|hasPart|__handle_1__",
                                                          "__handle_1__|Type|__Handle__",
                                                          "__Handle__|SubClassOf|HoldablePart",
                                                          "__object__|hasPart|__handle_2__",
                                                          "__handle_2__|Type|__Handle__",
                                                          "__Handle__|SubClassOf|HoldablePart"],
                                                    medium=["__object__|canBeUsed|boolean#true"],
                                                    hard=["__handle_2__|isAttachedToSomething|boolean#false",
                                                          "__object__|canBeUsed|boolean#true"],
                                                    concatenate=False) # Hard will not be concatenated with Medium

# =============== Capability Expression =============
capability_expression = ClassExpression(easy= "LiftingCapability|EquivalentTo|(isCapabilityOf some (hasComponent min 2 Gripper)",
                                        medium= "LiftingCapability|EquivalentTo|(isCapabilityOf some ((hasComponent min 2 Gripper) and (hasComponent some MotionPlanningAlgo))",
                                        hard= "LiftingCapability|EquivalentTo|(isCapabilityOf some ((hasComponent min 2 Gripper) and (hasComponent some MotionPlanningAlgo) and (hasSomethingInHands value boolean#false))")

capability_explanation = ClassExpressionExplanation(capability_expression,
                                                    easy=["__agent_capa__|isCapabilityOf|__agent__",
                                                          "__agent__|hasComponent|__gripper_1__",
                                                          "__gripper_1__|Type|__Gripper__",
                                                          "__Gripper__|SubClassOf|Gripper",
                                                          "__agent__|hasComponent|__gripper_2__",
                                                          "__gripper_2__|Type|__Gripper__",
                                                          "__Gripper__|SubClassOf|Gripper"],
                                                    medium=["__agent__|hasComponent|__algo__",
                                                            "__algo__|Type|MotionPlanningAlgo"],
                                                    hard=["__agent__|hasSomethingInHands|boolean#false"],
                                                    concatenate=True)

# =============== Property Explanation =============
property_expression = ClassExpression(easy = "", # box isTouchableBy agent
                                      medium = "(isOnTouchableSupport o isWithinMovingRangeOf)|SubPropertyOf|isTouchableBy", 
                                      hard = "(isOnTouchableSupport o isInAccessibleArea o isWithinMovingRangeOf)|SubPropertyOf|isTouchableBy")

property_explanation = ClassExpressionExplanation(property_expression,
                                                  easy= ["__object__|isTouchableBy|__agent__"],
                                                  medium= [],
                                                  hard=[],
                                                  concatenate = True)

property_explanation.medium = ["__object__|isOnTouchableSupport|__table__",
                               "__table__|isWithinMovingRangeOf|__agent__"]

property_explanation.hard = ["__object__|isOnTouchableSupport|__table__",
                             "__table__|isInAccessibleArea|__room__",
                             "__room__|isWithinMovingRangeOf|__agent__"]

# =============== QuestionManager =============

lift_manager = QuestionManager(lift_rule,
                               variable_manager,
                               affordance,
                               capability_explanation,
                               diposition_explanation,
                               property_explanation)

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

# gt_lift_easy = "The __Agent__ can lift the __Object__ because on one hand it has the lifting capability through its two __Gripper__s which are grippers. \
#                  On the other hand, the __Object__ has the disposition of being liftable because it has two __Handle__s, which are graspable parts. \
#                  Moreover the __Object__ is touchable by the __Agent__."

# gt_lift_medium = "The __Agent__ can lift the __Object__ because on one hand it has the grasping capability through its two __Gripper__s which are grippers \
#                   and being equipped with a motion planning algorithm. On the other hand, the __Object__ has the disposition of being liftable \
#                   because it can be used and has two __Handle__s, which are graspable parts. Moreover the __Object__ is touchable by the __Agent__ because \
#                   it is on a touchable support which is within the moving range of the __Agent__."
                 
# gt_lift_hard = "The __Agent__ can lift the __Object__ because on one hand it has the grasping capability through its two __Gripper__s which are grippers \
#                 , being equipped with a motion planning algorithm and not having anything in its hands. On the other hand, the __Object__ has the disposition \
#                 of being liftable because it can be used, has two __Handle__s, which are graspable parts, and that are not attached to something. \
#                 Moreover the __Object__ is touchable by the __Agent__ because it is on a touchable support which is in an accessible area, \
#                 within the moving range of the __Agent__."